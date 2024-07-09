# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining commands in the 'qbraid jobs' namespace.

"""
from pathlib import Path

import typer
from qbraid_core.services.environments.kernels import add_kernels, list_kernels, remove_kernels
from rich.console import Console

from qbraid_cli.handlers import handle_error

kernels_app = typer.Typer(help="Manage qBraid kernels.")


@kernels_app.command(name="list")
def kernels_list():
    """List all available kernels."""
    console = Console()
    # Get the list of kernelspecs
    kernelspecs = list_kernels()

    if len(kernelspecs) == 0:
        console.print("No qBraid kernels are active.")
        console.print("\nUse 'qbraid kernels add' to add a new kernel.")
        return

    longest_kernel_name = max(len(kernel_name) for kernel_name in kernelspecs)
    spacing = longest_kernel_name + 10

    console.print("# qbraid kernels:\n#\n")

    # Ensure 'python3' kernel is printed first if it exists
    default_kernel_name = "python3"
    python3_kernel_info = kernelspecs.pop(default_kernel_name, None)
    if python3_kernel_info:
        console.print(f"{default_kernel_name.ljust(spacing)}{python3_kernel_info['resource_dir']}")
    # print rest of the kernels
    for kernel_name, kernel_info in sorted(kernelspecs.items()):
        console.print(f"{kernel_name.ljust(spacing)}{kernel_info['resource_dir']}")


@kernels_app.command(name="add")
def kernels_add(
    environment: str = typer.Argument(
        ..., help="Name of environment for which to add ipykernel. Values from 'qbraid envs list'."
    )
):
    """Add a kernel."""

    try:
        add_kernels(environment)
    except ValueError as e:
        handle_error(
            message=e,
            include_traceback=False,
        )
        return


@kernels_app.command(name="remove")
def kernels_remove(
    environment: str = typer.Argument(
        ...,
        help=("Name of environment for which to remove ipykernel. Values from 'qbraid envs list'."),
    )
):
    """Remove a kernel."""
    try:
        remove_kernels(environment)
    except ValueError:
        handle_error(message=f"Environment '{environment}' not found.", include_traceback=False)
        return


if __name__ == "__main__":
    kernels_app()
