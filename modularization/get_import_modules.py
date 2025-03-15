import os
import nbformat
import ast

def get_import_modules(notebook_path):
    """
    Extract a set of module names from all import statements in the notebook.
    
    This function parses each code cell using ast to reliably extract modules from
    both 'import ...' and 'from ... import ...' statements.
    """
    print(notebook_path)
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    modules = set()
    for cell in nb.cells:
        if cell.cell_type == "code":
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
                        modules.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    # For "from module import something" statements
                    if node.module:
                        modules.add(node.module)
    return list(modules)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    notebook_path = os.path.join(current_dir, 'test.py')
    get_import_modules(notebook_path)