"""
tooling module contains helper functions for the bo4e-generator.
"""

import datetime
import os
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
    Checks if schema files have been downloaded in the last 30 minutes.
    If not, runs the bost command to download the schema files.
    """

    def _bost_is_installed() -> bool:
        try:
            from bost import main  # pylint: disable=import-outside-toplevel, unused-import

            return True
        except ImportError:
            return False

    def _recent_files_exist(folder: str, minutes: int) -> bool:
        now = datetime.datetime.now()
        cutoff = now - datetime.timedelta(minutes=minutes)
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mtime > cutoff:
                    return True
        return False

    if _recent_files_exist(schema_path, 30):
        print(
            f"BO JSON schema files in '{schema_path}' have been already downloaded in the last 30 minutes."
            + "Skipping download."
        )
    else:
        if _bost_is_installed():
            print("BO4E-Schema-Tool is already installed.")
            cli_runner = CliRunner()
            _ = cli_runner.invoke(main_command_line, ["-o", schema_path])
        else:
            run_command(f"bost -o {schema_path}")
        print("BO4E-Schema-Tool installation and schema downloading completed.")
