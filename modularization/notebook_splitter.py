import os
import nbformat

import lambda_archiver
# Folder, which stores the modularized code
folder_name = "build"


def create_cell_file(notebook_dir: str, cell_name: str, code_lines_only: list[str], id: int) -> str:
    """
    Creates a python file for one cell in the notebook
    """

    file_name = f"{notebook_dir}/{id}_{cell_name}.py"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write('\n'.join(code_lines_only) + '\n')

    print(f"Created {id}_{cell_name}.py")
    return file_name


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


def extract_package_name(import_string: str) -> str:
    package = import_string.split(' ')[1]
    root_package = package.split('.')[0]
    return root_package

def get_imports(notebook_path):
    """
    Extracts a set of import statements from all code cells in the notebook.
    """
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    imports = set() # Used a set to avoid duplicates
    for cell in nb.cells:
        if cell.cell_type == "code":
            for line in cell.source.splitlines():
                stripped = line.strip()
                if stripped.startswith("import ") or stripped.startswith("from "):
                    package_name = extract_package_name(stripped)
                    imports.add(package_name)
    return list(imports)


# Creates metadata file for each cell
# def build_metadata_file(notebook_name: str, metadata: list[str]) -> None:
#     # Remove '#' from comments and join metadata lines
#     cleaned_metadata = "\n".join(line.lstrip("# ").strip() for line in metadata)
#
#     # Save directly as a YAML file
#     yaml_filename = f"modularization/{notebook_name}/metadata.yaml"
#     try:
#         with open(yaml_filename, "w", encoding="utf-8") as yaml_file:
#             yaml_file.write(cleaned_metadata)
#         print(f"Extracted metadata saved as YAML: {yaml_filename}")
#     except Exception as e:
#         print(f"Error saving YAML file for {notebook_name}: {e}")


def split_notebook(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # The name of the primary notebook file
    notebook_name = os.path.splitext(notebook_path)[0].split("/")[-1]
    # Ensure the target directory exists
    notebook_dir = f"{folder_name}/{notebook_name}"
    os.makedirs(notebook_dir, exist_ok=True)

    cells = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
            # Check if metadata exists in the cell
        if not metadata_check(cell):
            continue
        cell_lines = cell.source.split("\n")
        cell_name = cell_lines[0].lstrip("# ").strip()
        # Separate the code lines & metadata
        # code_lines = []
        # for line in cell_lines:
        #     if not line or line.lstrip()[0] != "#":
        #         code_lines.append(line)
        cells.append({
            "name": cell_name,
            "code": cell.source
        })
    return cells

if __name__ == "__main__":
    with open("modified_notebooks.txt", "r", encoding="utf-8") as f:
        notebooks = f.read().splitlines()

    for nb_file in notebooks:
        if os.path.exists(nb_file):
            notebook_name = os.path.splitext(nb_file)[0].split("/")[-1]
            root_dir = f'build/{notebook_name}'
            cells = split_notebook(nb_file)
            for cell in cells:
                lambda_archiver.make_lambda_archive(cell['name'], cell['code'], root_dir)

            layer_name = f"{notebook_name}-layer"
            imports = [x for x in get_imports(nb_file) if x != 'os' and x != 'warnings']
            lambda_archiver.make_layer_archive(layer_name, imports, root_dir)
        else:
            print(f"Warning: {nb_file} does not exist.")