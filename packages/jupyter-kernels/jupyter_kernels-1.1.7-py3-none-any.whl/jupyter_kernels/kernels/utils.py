from datetime import datetime, timezone

from rich.console import Console
from rich.table import Table


def timestamp_to_local_date(timestamp: str) -> str:
    return (
        datetime.fromtimestamp(float(timestamp), timezone.utc).astimezone().isoformat()
    )


def new_kernel_table(title="Jupyter Kernel"):
    table = Table(title=title)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Server name", style="magenta", no_wrap=True)
    table.add_column("Environment", style="green", no_wrap=True)
    table.add_column("Expired At", style="red", no_wrap=True)
    return table


def add_kernel_to_table(table, kernel):
    expired_at = kernel.get("expired_at")
    table.add_row(
        kernel["kernel_given_name"],
        kernel["jupyter_pod_name"],
        kernel["environment_name"],
        "Never" if expired_at is None else timestamp_to_local_date(expired_at),
    )


def display_kernels(kernels: list) -> None:
    """Display a list of kernels in the console."""
    table = new_kernel_table(title="Jupyter Kernels")
    for kernel in kernels:
        add_kernel_to_table(table, kernel)
    console = Console()
    console.print(table)
