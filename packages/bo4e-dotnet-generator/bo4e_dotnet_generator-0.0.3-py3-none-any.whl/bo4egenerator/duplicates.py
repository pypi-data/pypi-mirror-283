"""
Remove duplicate class and enum definitions from the generated files.
"""

import os
import re
from pathlib import Path


def find_classes_and_enums_in_file(file_path: Path) -> tuple[list[str], list[str]]:
    """
    Find all partial class and enum definitions in a given file.

    Args:
        file_path (str): The path to the file.

    Returns:
        tuple: Two lists containing class names and enum names found in the file.
    """
    class_pattern = re.compile(r"\bpublic\s+partial\s+class\s+(\w+)")
    enum_pattern = re.compile(r"\bpublic\s+enum\s+(\w+)")
    classes: list[str] = []
    enums: list[str] = []

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        class_matches = class_pattern.findall(content)
        enum_matches = enum_pattern.findall(content)
        classes.extend(class_matches)
        enums.extend(enum_matches)

    return classes, enums


def remove_definitions(  # pylint: disable=too-many-locals, too-many-branches
    file_path: Path, main_class_name: str, classes_to_remove: list[str], enums_to_remove: list[str]
) -> None:
    """
    Remove specified class and enum definitions from a file, keeping the main class intact.

    Args:
        file_path (str): The path to the file.
        main_class_name (str): The main class to keep intact.
        classes_to_remove (list): List of class names to remove.
        enums_to_remove (list): List of enum names to remove.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except (PermissionError, OSError) as e:
        print(f"Error reading file {file_path}: {e}")
        return

    in_definition = False
    definitions = {}
    current_definition = None
    definition_start_index = 0
    comment_block_start_index = None

    def find_comment_block_start(index: int) -> int:
        """Find the start index of the comment block preceding the definition."""
        while index > 0 and re.match(r"\s*///", lines[index - 1]):
            index -= 1
        return index

    # Read the file line by line and identify class and enum definitions
    for index, line in enumerate(lines):
        if re.match(r"\s*///", line) and not in_definition:
            if comment_block_start_index is None:
                comment_block_start_index = index
            continue
        if comment_block_start_index is not None and not re.match(r"\s*///", line):
            comment_block_start_index = None

        if re.match(r"\s*public\s+partial\s+class\s+\w+", line):
            class_name = re.findall(r"\bpublic\s+partial\s+class\s+(\w+)", line)[0]
            if class_name == main_class_name:
                current_definition = None
                in_definition = False
                continue
            current_definition = class_name
            in_definition = True
            definition_start_index = find_comment_block_start(index) if comment_block_start_index is not None else index
        elif re.match(r"\s*public\s+enum\s+\w+", line):
            enum_name = re.findall(r"\bpublic\s+enum\s+(\w+)", line)[0]
            current_definition = enum_name
            in_definition = True
            definition_start_index = find_comment_block_start(index) if comment_block_start_index is not None else index

        if in_definition:
            if re.match(r"\s*\}", line):
                definitions[current_definition] = (definition_start_index, index)
                in_definition = False
                current_definition = None

    # Remove classes and enums to remove from the lines
    for name in classes_to_remove + enums_to_remove:
        if name in definitions:
            start, end = definitions[name]
            # Check for leading empty lines and comments
            while start > 0 and re.match(r"^\s*$", lines[start - 1]):
                start -= 1
            while start > 0 and re.match(r"\s*///", lines[start - 1]):
                start -= 1
            lines[start : end + 1] = []

    # Write the cleaned content back to the file
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)
    except (PermissionError, OSError) as e:
        print(f"Error writing to file {file_path}: {e}")


def process_directory(directory_path: Path) -> None:
    """
    Process all files in the directory to remove duplicate class and enum definitions.
    Args:
        directory_path (Path): The path to the directory.
    """
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(".cs"):
                file_path = Path(root) / filename
                class_name_from_filename = file_path.stem
                classes_in_file, enums_in_file = find_classes_and_enums_in_file(file_path)

                # Exclude the main class that matches the filename
                classes_to_remove = [
                    class_name for class_name in classes_in_file if class_name != class_name_from_filename
                ]
                enums_to_remove = list(enums_in_file)

                for class_name in classes_to_remove:
                    class_file_path_bo = directory_path / "bo" / f"{class_name}.cs"
                    class_file_path_com = directory_path / "com" / f"{class_name}.cs"

                    if class_file_path_bo.exists() or class_file_path_com.exists():
                        print(f"Removing class {class_name} from {file_path}")
                        remove_definitions(file_path, class_name_from_filename, [class_name], [])

                for enum_name in enums_to_remove:
                    enum_file_path = directory_path / "enum" / f"{enum_name}.cs"

                    if enum_file_path.exists():
                        print(f"Removing enum {enum_name} from {file_path}")
                        remove_definitions(file_path, class_name_from_filename, [], [enum_name])

                print(f"Processed {file_path}")
