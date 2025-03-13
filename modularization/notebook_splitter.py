import os
import nbformat

import lambda_archiver
# Folder, which stores the modularized code
folder_name = "build"


def create_cell_file(notebook_dir: str, cell_name: str,
                     code_lines_only: list[str], id: int) -> str:
    """
    Creates a python file for one cell in the notebook
    """

    file_name = f"{notebook_dir}/{id}_{cell_name}.py"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write('\n'.join(code_lines_only) + '\n')

    print(f"Created {id}_{cell_name}.py")
    return file_name


def split_skeleton_wrapper_file() -> (str, str):
    """
    Splits the skeleton wrapper file into two parts: pre and post main code body

    skeleton_wrapper.py has the structure required by AWS lamdba and allows
    for passing variables between lambdas inside of step functions.
    """

    with open("modularization/wrapper_skeleton.py", "r", encoding="utf-8") as f:
        skeleton = f.read()
        pre, post = skeleton.split("# Main body function")

    return pre, post


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


def extract_package_names(import_statements: list[str]) -> [str]:
    """
    Extracts the package names from an import statements list
    """
    root_packages = set()
    for import_string in import_statements:
        package = import_string.split(' ')[1]
        root_package = package.split('.')[0]
        root_packages.add(root_package)
    return list(root_packages)


def get_imports(notebook_path):
    """
    Get a set of import statements from all code cells in the notebook.
    """
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    imports = set()  # Used a set to avoid duplicates
    for cell in nb.cells:
        if cell.cell_type == "code":
            for line in cell.source.splitlines():
                stripped = line.strip()
                if stripped.startswith("import ") or stripped.startswith("from "):
                    imports.add(stripped)

    return list(imports)


def filter_code_from_imports(code: str) -> str:
    """
    Filters out import statements from the code
    """
    code_lines = code.split("\n")
    code_lines = [line for line in code_lines
                  if not line.strip().startswith("import ")
                  and not line.strip().startswith("from ")]

    # Indentation is needed as cell code will be placed inside of a function
    indented_code_lines = [f"    {line}" for line in code_lines]

    return "\n".join(indented_code_lines)


def construct_import_code(notebook_path: str) -> str:
    """
    Aggregates import statements from the whole file and returns as a string
    """

    import_codelines = get_imports(notebook_path)
    return "\n".join(import_codelines)


def split_notebook(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # The name of the primary notebook file
    notebook_name = os.path.splitext(notebook_path)[0].split("/")[-1]
    # Ensure the target directory exists
    notebook_dir = f"{folder_name}/{notebook_name}"
    os.makedirs(notebook_dir, exist_ok=True)

    import_code = construct_import_code(notebook_path)
    pre_wrapper, post_wrapper = split_skeleton_wrapper_file()

    cells = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        # Check if metadata exists in the cell
        if not metadata_check(cell):
            cell_name = f"global_{i}"
        else:
            cell_lines = cell.source.split("\n")
            cell_name = cell_lines[0].lstrip("# ").strip()
        code_lines = filter_code_from_imports(cell.source)
        new_source = import_code + pre_wrapper + \
            "\n\n" + code_lines + post_wrapper

        cells.append({
            "name": cell_name,
            "code": new_source
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
            packages = extract_package_names(get_imports(nb_file))
            imports = [x for x in packages if x != 'os' and x != 'warnings']
            # imports = [x for x in get_imports(nb_file) if x != 'os' and x != 'warnings']
            lambda_archiver.make_layer_archive(layer_name, imports, root_dir)
        else:
            print(f"Warning: {nb_file} does not exist.")