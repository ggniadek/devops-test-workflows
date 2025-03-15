import os
import nbformat
import ast

import lambda_archiver
import s3_uploader
import get_import_modules

# Folder, which stores the modularized code
folder_name = "build"
essential_imports = "import os\n"
env_home = "os.environ['HOME'] = '/tmp'\n"

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

def handle_import_modules_injection(body, notebook_path) -> str:
    delimiter = 'or k.startswith("context")'
    parts = body.split(delimiter, 2)
    pre = delimiter.join(parts[:2])
    post = parts[2]
    modules = get_import_modules(notebook_path)
    code_lines = []
    for module in modules:
        code_lines.append(f'or k.startswith("{module}")')
        
    # Indentation is needed as cell code will be placed inside of a function
    indented_code_lines = [f"    {line}" for line in code_lines]

    return pre + "\n".join(indented_code_lines) + post

def split_skeleton_wrapper_file() -> (str, str):
    """
    Splits the skeleton wrapper file into two parts: pre and post main code body

    skeleton_wrapper.py has the structure required by AWS lamdba and allows
    for passing variables between lambdas inside of step functions.
    """

    with open("modularization/wrapper_skeleton.py", "r", encoding="utf-8") as f:
        skeleton = f.read()
        pre, post = skeleton.split("# Main body function")

    return pre, post_injected


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


def extract_package_names(import_statement: str) -> [str]:
    """
    Extracts the package names from an import statements list
    """
    stripped_imports = import_statement.replace("!pip install ", "").split()
    libraries = [imp.split("==")[0] for imp in stripped_imports]

    return libraries


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

    # imports.remove("import os")
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

    # Gather import statements from the notebook
    import_code = construct_import_code(notebook_path)
    # Divide the skeleton wrapper file (Goncalo) into two parts
    pre_wrapper, post_wrapper = split_skeleton_wrapper_file()
    
    post_injected = handle_import_modules_injection(post_wrapper, notebook_path)

    cells = []
    packages = []
    import_modules = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            try:
                tree = ast.parse(cell.source)
            except Exception as e:
                # Skip cells that can't be parsed
                continue
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    # For "import module [as alias]" statements
                    for alias in node.names:
                        # alias.name gives you the module (or package) name
                        import_modules.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    # For "from module import something" statements
                    if node.module:
                        import_modules.add(node.module)
                        

        # Check if metadata exists in the cell
        cell_lines = cell.source.split("\n")
        if not metadata_check(cell):
            # Type A: Installation cell
            if cell_lines[0].startswith("!pip install "):
                packages = extract_package_names(cell.source)
                continue
            # Type B: Global variables definition cell (without a name)
            cell_name = f"global_{i}"
        # Type C: Standard cells
        else:
            cell_name = cell_lines[0].lstrip("# ").strip()
        code_lines = filter_code_from_imports(cell.source)
        new_source = essential_imports + env_home + import_code \
            + "\n\n" + pre_wrapper + \
            "\n" + code_lines + "\n" + post_wrapper

        cells.append({
            "name": cell_name,
            "code": new_source
        })
    return cells, packages, import_modules


if __name__ == "__main__":
    print(os.getcwd())

    with open("modified_notebooks.txt", "r", encoding="utf-8") as f:
        notebooks = f.read().splitlines()

    for nb_file in notebooks:
        if os.path.exists(nb_file):
            notebook_name = os.path.splitext(nb_file)[0].split("/")[-1]
            root_dir = f'build/{notebook_name}'
            cells, packages, import_modules = split_notebook(nb_file)
            for cell in cells:
                lambda_archiver.make_lambda_archive(cell['name'], cell['code'], root_dir)

            layer_name = f"{notebook_name}-layer"
            lambda_archiver.make_layer_archive(layer_name, packages, root_dir)
        else:
            print(f"Warning: {nb_file} does not exist.")

    s3_uploader.upload_zips()
