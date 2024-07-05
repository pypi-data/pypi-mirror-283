"""Stores all sorts of Dataclasses, Enums or Factories to help with the
CasadiBackend."""
import os
import random
import subprocess
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, List, NamedTuple

import casadi as ca
from enum import Enum
from pydantic import ConfigDict, Field, BaseModel

from agentlib_mpc.data_structures import mpc_datamodels


CaFuncInputs = Union[ca.MX, ca.SX, ca.Sparsity, ca.DM, float, int]
DiscreteVars = List[bool]
GUESS_PREFIX = "guess_"
LB_PREFIX = "lb_"
UB_PREFIX = "ub_"

# Casadi Matrices specifying the input of all different types
# of optimization parameters. Matrices consist of different variable rows
# and have a column for each time step in the discretization.
# There are separate matrices for each input type (as defined in the
# System), and also for the upper and lower boundaries of variables
# respectively.
# Example:
# {"x": [[1, 2], [0, 2]],
# "lb_x": [[0, 0], [0, 0]],
# "ub_x": [[0, 0], [0, 0]],
# "d": [[2, 1], [1, 1]]
# }
MPCInputs = dict[str, ca.DM]


class DiscretizationMethod(str, Enum):
    collocation = "collocation"
    multiple_shooting = "multiple_shooting"


class CollocationMethod(str, Enum):
    radau = "radau"
    legendre = "legendre"


class Solvers(str, Enum):
    ipopt = "ipopt"
    qpoases = "qpoases"
    sqpmethod = "sqpmethod"
    gurobi = "gurobi"
    bonmin = "bonmin"


class Integrators(str, Enum):
    cvodes = "cvodes"
    rk = "rk"  # runge-kutta


class CasadiDiscretizationOptions(mpc_datamodels.DiscretizationOptions):
    model_config = ConfigDict(extra="forbid")

    method: DiscretizationMethod = DiscretizationMethod.collocation
    collocation_order: int = Field(default=3, ge=1, le=9)
    collocation_method: CollocationMethod = CollocationMethod.legendre
    integrator: Integrators = Integrators.cvodes


class SolverOptions(BaseModel):
    name: Solvers = "ipopt"
    options: dict = Field(default={})
    model_config = ConfigDict(extra="forbid")


@dataclass
class OptParMXContainer:
    """Stores the necessary MX variables created during discretization for
    OptimizationParameters."""

    var: List[ca.MX] = field(default_factory=list)  # res format
    grid: List[float] = field(default_factory=list)  # res format,  mpc inputs


@dataclass
class OptVarMXContainer(OptParMXContainer):
    """Stores the necessary MX variables created during discretization for
    OptimizationVariables."""

    lb: List[ca.MX] = field(default_factory=list)  # res format
    ub: List[ca.MX] = field(default_factory=list)  # res format
    guess: List[ca.MX] = field(default_factory=list)  # res format
    opt: ca.DM = None  # mpc inputs


@dataclass
class Constraint:
    function: ca.MX
    lb: ca.MX
    ub: ca.MX


class ModelConstraint(NamedTuple):
    lb: CaFuncInputs
    function: ca.MX
    ub: CaFuncInputs


@dataclass
class SolverFactory:
    """Creates a solver given an NLP and an options construct."""

    do_jit: bool
    bat_file: Path = None
    name: str = None
    options: SolverOptions = field(default_factory=SolverOptions)

    def create_solver(
        self,
        nlp: Union[dict, str],
        discrete: DiscreteVars = None,
    ) -> ca.Function:
        options = self.options.options
        solver_name = self.options.name.casefold()

        if solver_name == Solvers.ipopt:
            return self._create_ipopt_solver(nlp=nlp, options=options)
        if solver_name == Solvers.sqpmethod:
            return self._create_sqpmethod_solver(nlp=nlp, options=options)
        if solver_name == Solvers.qpoases:
            return self._create_qpoases_solver(nlp=nlp, options=options)
        if solver_name == Solvers.gurobi:
            return self._create_gurobi_solver(
                nlp=nlp, options=options, discrete=discrete
            )
        if solver_name == Solvers.bonmin:
            return self._create_bonmin_solver(
                nlp=nlp, options=options, discrete=discrete
            )
        raise ValueError(
            f'Solver "{solver_name}" not recognized. Currently '
            f"supported: {[s.value for s in Solvers]}"
        )

    def _create_ipopt_solver(self, nlp: dict, options: dict):
        default_opts = {
            "verbose": False,
            "print_time": False,
            "record_time": True,
            "ipopt": {
                "max_iter": 100,
                "tol": 1e-5,
                "acceptable_tol": 0.1,
                "acceptable_constr_viol_tol": 1,
                "acceptable_iter": 5,
                "acceptable_compl_inf_tol": 1,
                "print_level": 0,
            },
        }
        ipopt_ = options.pop("ipopt", {})
        opts = {**default_opts, **options}
        opts["ipopt"].update(ipopt_)
        solver = ca.nlpsol("mpc", "ipopt", nlp, opts)
        if not self.do_jit:
            return solver
        nlp = compile_ipopt_solver(
            bat_file=self.bat_file, optimizer=solver, name=self.name
        )
        return ca.nlpsol("mpc", "ipopt", nlp, opts)

    def _create_sqpmethod_solver(self, nlp: dict, options: dict):
        default_opts = {
            "qpsol": "qrqp",
            "qpsol_options": {"error_on_fail": False},
            "print_time": False,
            "max_iter": 20,
            "tol_du": 0.01,
            "tol_pr": 0.0001,
        }
        opts = {**default_opts, **options}
        return ca.nlpsol("mpc", "sqpmethod", nlp, opts)

    def _create_qpoases_solver(self, nlp: dict, options: dict):
        default_opts = {
            "verbose": False,
            "print_time": False,
            "record_time": True,
            "printLevel": "low",
        }
        opts = {**default_opts, **options}
        return ca.qpsol("mpc", "qpoases", nlp, opts)

    def _create_gurobi_solver(
        self, nlp: dict, options: dict, discrete: DiscreteVars = None
    ):
        default_opts = {}
        opts = {**default_opts, **options, "discrete": discrete}
        return ca.qpsol("mpc", "gurobi", nlp, opts)

    def _create_bonmin_solver(
        self, nlp: dict, options: dict, discrete: DiscreteVars = None
    ):
        default_opts = {
            "bonmin.bb_log_level": 0,
            "bonmin.bb_log_interval": 1000,
            "bonmin.nlp_log_level": 0,
        }
        opts = {**default_opts, **options, "discrete": discrete}
        return ca.nlpsol("mpc", "bonmin", nlp, opts)


@contextmanager
def temporary_directory(path):
    old_pwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_pwd)


def compile_ipopt_solver(bat_file: Path, name: str, optimizer: ca.Function) -> str:
    """
    Code-generates an ipopt solver and compiles it.
    Currently, only works on Windows! Requires a batch file that knows
    how to setup Visual Studio command line and compiles the source code.

    Returns:
        The Path to the .dll file for the compiled solver.

    Raises:
        TypeError
        FileNotFoundError
        RuntimeError
    """
    if not name:
        name = f"nlp_{random.randint(10, 1000)}"

    base_name = name
    file_name = f"{name}.c"
    file = Path(file_name)
    i = 0

    # "build_batch_bat": "D:/ses-tsp/masterarbeit-miocp/02_Work/agentlib_mpc_9_approximate_miocp/examples/prod_cons_nmpc/solver_lib/compile_nlp.bat",

    c_dir = Path(Path(bat_file).parent, "code_gen")
    c_dir.mkdir(exist_ok=True)
    batch = str(Path(bat_file).absolute())

    with temporary_directory(c_dir):
        while file.exists():
            name = f"{base_name}_{i}"
            file_name = f"{name}.c"
            file = Path(file_name)
            i = i + 1

    with temporary_directory(c_dir):
        optimizer.generate_dependencies(file_name)

    try:
        with temporary_directory(c_dir):
            ret = subprocess.call([batch, file_name])
    except TypeError as e:
        # no batch file was provided
        raise TypeError(
            "You need to provide a batch file to "
            "compile the solver in the backend config."
        ) from e
    except FileNotFoundError as e:
        # provided batch file does not exist
        raise FileNotFoundError from e
    if ret != 0:
        raise RuntimeError(
            "The provided batch file did not exit properly, please "
            "check it properly compiles the provided file."
        )
    solver_dll = Path(c_dir).joinpath(f"{name}.dll").absolute()
    return str(solver_dll)
