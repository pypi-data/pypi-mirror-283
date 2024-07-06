"""
tooling module contains helper functions for the bo4e-generator.
"""

import subprocess
from pathlib import Path

from bost.__main__ import main_command_line
from click.testing import CliRunner


def run_command(command: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """
    Run a shell command and return the result.
    Args:
        command (str): command to run
        cwd (Path | None, optional): path. Defaults to None.

    Returns:
        subprocess.CompletedProcess[str]: _description_
    """
    result = subprocess.run(command, shell=True, cwd=cwd, text=True, capture_output=True, check=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        print(result.stderr)
    return result


def running_bo4e_schema_tool(schema_path: str) -> None:
    """
    the installation step of bost shall be done at this point, because bost is a dependency of this project
    """

    def _bost_is_installed() -> bool:
        try:
            from bost import main  # pylint: disable=import-outside-toplevel, unused-import

            return True
        except ImportError:
            return False

    if _bost_is_installed():
        print("BO4E-Schema-Tool is already installed.")
        cli_runner = CliRunner()
        _ = cli_runner.invoke(main_command_line, ["-o", schema_path])
    else:
        run_command(f"bost -o {schema_path}")
    print("BO4E-Schema-Tool installation and schema downloading completed.")
