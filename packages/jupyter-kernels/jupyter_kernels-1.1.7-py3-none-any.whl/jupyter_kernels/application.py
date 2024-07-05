from pathlib import Path

from ._version import __version__
from .application_base import JupyterKernelsBaseApp

from .kernels.console.consoleapp import KernelConsoleApp
from .kernels.create.createapp import KernelCreateApp
from .kernels.execapp import KernelExecApp
from .kernels.list.listapp import KernelListApp
from .kernels.loginapp import KernelLoginApp
from .kernels.logoutapp import KernelLogoutApp
from .kernels.pause.pauseapp import KernelPauseApp
from .kernels.specs.specsapp import KernelSpecsApp
from .kernels.start.startapp import KernelStartApp
from .kernels.stop.stopapp import KernelStopApp
from .kernels.terminate.terminateapp import KernelTerminateApp


HERE = Path(__file__).parent


class JupyterKernelsApp(JupyterKernelsBaseApp):
    description = """
      The JupyterKernels application.
    """

    subcommands = {
        "console": (
            KernelConsoleApp,
            KernelConsoleApp.description.splitlines()[0],
        ),
        "create": (KernelCreateApp, KernelCreateApp.description.splitlines()[0]),
        "exec": (KernelExecApp, KernelExecApp.description.splitlines()[0]),
        "list": (KernelListApp, KernelListApp.description.splitlines()[0]),
        "login": (KernelLoginApp, KernelLoginApp.description.splitlines()[0]),
        "logout": (KernelLogoutApp, KernelLogoutApp.description.splitlines()[0]),
        "pause": (KernelPauseApp, KernelPauseApp.description.splitlines()[0]),
        "specs": (KernelSpecsApp, KernelSpecsApp.description.splitlines()[0]),
        "start": (KernelStartApp, KernelStartApp.description.splitlines()[0]),
        "stop": (KernelStopApp, KernelStopApp.description.splitlines()[0]),
        "terminate": (
            KernelTerminateApp,
            KernelTerminateApp.description.splitlines()[0],
        ),
    }


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = JupyterKernelsApp.launch_instance

if __name__ == "__main__":
    main()
