import os
import nbformat

# Folder, which stores the modularized code
folder_name = "modularization"

# Create a new notebook with the cell
def create_cell_files(notebook_dir: str, cell_name: str, code_lines_only: list[str], id: int) -> None:

    with open(f"{notebook_dir}/{id}_{cell_name}.py", "w", encoding="utf-8") as f:
        f.write('\n'.join(code_lines_only) + '\n')

    print(f"Created {cell_name}.py")


# Metadata file is saved as json
def build_metadata_file(notebook_name: str, metadata: list[str]) -> None:
    # print(notebook_name)
    # print(metadata)
    return None


def split_notebook(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # The name of the primary notebook file
    notebook_name = os.path.splitext(notebook_path)[0].split("/")[0]
    # Ensure the target directory exists
    notebook_dir = f"{folder_name}/{notebook_name}"
    os.makedirs(notebook_dir, exist_ok=True)

    for i, cell in enumerate(nb.cells):
        # Separate the code lines & metadata
        code_lines_only, metadata = [], []
        cell_lines = cell.source.split("\n")
        cell_name = (cell_lines[0].split("# ")[1])
        for line in cell_lines:
            # This is a very sketchy way to do it, think of sth better later
            if line[0] != "#":
                code_lines_only.append(line)
            else:
                metadata.append(line)

        create_cell_files(notebook_dir, cell_name, code_lines_only, i)
        build_metadata_file(notebook_name, metadata)


if __name__ == "__main__":
    with open("modified_notebooks.txt", "r", encoding="utf-8") as f:
        notebooks = f.read().splitlines()

    for nb_file in notebooks:
        if os.path.exists(nb_file):
            split_notebook(nb_file)
        else:
            print(f"Warning: {nb_file} does not exist.")