"""
It generates C# classes from the BO4E schema files with help od Quicktype npm package.
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path


def generate_csharp_classes(  # pylint: disable=too-many-locals
    project_root: Path, schemas_dir: Path, output_dir: Path, quicktype_executable: str
) -> None:
    """
    Generate C# classes from the BO4E schema files with help of Quicktype npm package.
    Args:
        project_root (Path): root path of the project
        schemas_dir (Path): path to the directory containing the BO4E schema files
        output_dir (Path): path to the directory where the generated C# BO classes will be saved
        quicktype_executable (str): path to the Quicktype executable
    """
    print("Starting C# class generation...")
    assert project_root.exists() and project_root.is_dir()
    assert schemas_dir.exists() and schemas_dir.is_dir()
    # assert output_dir.exists() and output_dir.is_dir() ?? todo @hamid

    # Get the current date to include in the log file name
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"error_log_{current_date}.txt"

    # Change to the root directory of the project
    os.chdir(project_root)

    # Open a log file for writing error messages
    with open(log_file_name, "w", encoding="utf-8") as log_file:
        # Walk through the schema directory
        for root, _, files in os.walk(schemas_dir):
            for file in files:
                if file.endswith(".json"):
                    # Construct the full path to the schema file
                    schema_file = os.path.join(root, file)

                    # Determine the relative path to preserve subfolder structure
                    relative_path = os.path.relpath(root, schemas_dir)

                    # Create corresponding subdirectory in the output directory
                    output_subdir = os.path.join(output_dir, relative_path)
                    if not os.path.exists(output_subdir):
                        os.makedirs(output_subdir)

                    # Determine the output file path
                    class_name = os.path.splitext(file)[0]
                    output_file = os.path.join(output_subdir, f"{class_name}.cs")

                    # Normalize paths to ensure correct format
                    schema_file = os.path.normpath(schema_file)
                    output_file = os.path.normpath(output_file)

                    # Construct the quicktype command
                    command = [
                        quicktype_executable,
                        "--src",
                        schema_file,
                        "--src-lang",
                        "schema",
                        "--out",
                        output_file,
                        "--lang",
                        "cs",
                        "--namespace",
                        "BO4EDotNet",
                    ]

                    # Debugging: Print the command to be executed
                    print(f"Running command: {' '.join(command)}")

                    try:
                        # Execute the command
                        result = subprocess.run(command, cwd=root, check=True, capture_output=True, text=True)
                        print(result.stdout)
                    except subprocess.CalledProcessError as e:
                        # Log the error and continue with the next file
                        log_file.write(f"Error running command: {' '.join(command)}\n")
                        log_file.write(f"Error message: {e}\n")
                        log_file.write(f"Standard Error Output: {e.stderr}\n\n")
                        print("Error encountered. Logged and continuing with the next file.")

    print(f"C# classes generation completed. Check {log_file_name} for any issues encountered.")
