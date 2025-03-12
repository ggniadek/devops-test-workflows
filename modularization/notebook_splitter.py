import os
import json
import nbformat
import yaml
import re

# Folder, which stores the modularized code
folder_name = "modularization"


def create_cell_files(notebook_dir: str, cell_name: str, code_lines: list[str],
                      cell_id: int, import_lines: list[str]) -> None:
    """
    Creates a python file for each cell in the notebook
    """
    filename = f"{notebook_dir}/{cell_id}_{cell_name}.py"
    with open(filename, "w", encoding="utf-8") as f:
        # Including each import statement in the cell file
        for imp_statement in import_lines:
            f.write(imp_statement + "\n")
        f.write("\n")
        # Lambda function wrapper
        f.write("def lambda_handler(event, context):\n")
        # Write the code lines
        for line in code_lines:
            # Indent code by 4 spaces (bc no it is inside of a function)
            f.write("    " + line + "\n")

    print(f"Created {filename}.py")


def metadata_check(cell: str) -> bool:
    """
    Checks if metadata was provided for the cell
    """

    metadata_identifiers = ["# NaaVRE:", "#  cell:"]
    cell_text = cell.source.split("\n")  # Convert to a list of lines

    # Check if required metadata identifiers exist in the cell
    if all(any(identifier in line for line in cell_text) for identifier in
           metadata_identifiers):
        return True
    else:
        return False


def build_metadata_file(notebook_name: str, metadata: list[str]) -> None:
    """
    Creates a JSON file based on the metadata list passed.
    Each metadata line is cleaned (removing the '#' and extra spaces) and stored as an item in a JSON array.
    """
    json_filename = f"{folder_name}/{notebook_name}/metadata.json"
    # Clean each metadata line
    cleaned_metadata = [line.lstrip("# ").strip() for line in metadata]
    try:
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(cleaned_metadata, json_file, indent=4)
        print(f"Extracted metadata saved as JSON: {json_filename}")
    except Exception as e:
        print(f"Error saving JSON file for {notebook_name}: {e}")


# def get_imports(nb):
#     """
#     Extracts a set of import statements from all code cells in the notebook.
#     """
#     imports = set()  # Used a set to avoid duplicates
#     library_names = set()
#     for cell in nb.cells:
#         if cell.cell_type == "code":
#             for line in cell.source.splitlines():
#                 stripped = line.strip()
#                 if stripped.startswith("import ") or stripped.startswith("from "):
#                     imports.add(stripped)

#                     # I let chatGTP write this conditions:
#                     if stripped.startswith("import "):
#                         # Remove the "import " prefix and split by commas (to handle multiple imports)
#                         rest = stripped[len("import "):].strip()
#                         parts = rest.split(',')
#                         for part in parts:
#                             # Remove alias if present (e.g., "numpy as np")
#                             part = part.strip()
#                             if " as " in part:
#                                 part = part.split(" as ")[0].strip()
#                             # Only keep the top-level module (e.g., "matplotlib" from "matplotlib.pyplot")
#                             top_level = part.split('.')[0]
#                             library_names.add(top_level)

#                     elif stripped.startswith("from "):
#                         # Extract the module after "from", e.g., "from pandas import DataFrame" -> "pandas"
#                         match = re.match(r'from\s+([^\s]+)', stripped)
#                         if match:
#                             module_name = match.group(1)
#                             top_level = module_name.split('.')[0]
#                             library_names.add(top_level)

#     print(f"Imported libraries: {library_names}")
#     return list(imports)


def get_imports(nb):
    """
    Extracts a set of import statements from all code cells in the notebook,
    and also prints the unique top-level library names found.
    """
    imports = set()  # Used a set to avoid duplicates
    library_names = set()
    for cell in nb.cells:
        if cell.cell_type == "code":
            for line in cell.source.splitlines():
                stripped = line.strip()
                if stripped.startswith("import ") or stripped.startswith("from "):
                    imports.add(stripped)
                    if stripped.startswith("import "):
                        rest = stripped[len("import "):].strip()
                        parts = rest.split(',')
                        for part in parts:
                            part = part.strip()
                            if " as " in part:
                                part = part.split(" as ")[0].strip()
                            top_level = part.split('.')[0]
                            library_names.add(top_level)
                    elif stripped.startswith("from "):
                        match = re.match(r'from\s+([^\s]+)', stripped)
                        if match:
                            module_name = match.group(1)
                            top_level = module_name.split('.')[0]
                            library_names.add(top_level)
    print(f"Imported libraries: {library_names}")
    return list(imports)


def split_notebook(notebook_path):
    """
    Splits .ipynb file into separate .py files
    Each cell file:
    - Include import statements (aggregated from the whole .ipynb)
    - Will be wrapped in lambda_handler function
    """

    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    import_lines = get_imports(nb)

    # Use the notebook filename as the folder name
    notebook_name = os.path.splitext(notebook_path)[0].split("/")[0]
    notebook_dir = f"{folder_name}/{notebook_name}"
    os.makedirs(notebook_dir, exist_ok=True)

    metadata = []

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            # Check if metadata exists in the cell
            if metadata_check(cell):
                cell_lines = cell.source.split("\n")
                # The first line contains a cell name
                cell_name = cell_lines[0].lstrip("# ").strip()
                code_lines = []
                # Separate metadata lines from code lines
                for line in cell_lines:
                    stripped = line.lstrip()
                    # Skipping import statements as they were already added
                    if stripped.startswith("import ") or stripped.startswith("from "):
                        continue
                    elif not line or line.lstrip()[0] != "#":
                        code_lines.append(line)
                    else:
                        metadata.append(line)
                create_cell_files(notebook_dir, cell_name,
                                  code_lines, i, import_lines)
    build_metadata_file(notebook_name, metadata)


if __name__ == "__main__":
    with open("modified_notebooks.txt", "r", encoding="utf-8") as f:
        notebooks = f.read().splitlines()

    for nb_file in notebooks:
        if os.path.exists(nb_file):
            split_notebook(nb_file)
        else:
            print(f"Warning: {nb_file} does not exist.")