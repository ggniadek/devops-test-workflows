import os
import nbformat

# Folder, which stores the modularized code
folder_name = "modularization"


# Creates python files for each cell
def create_cell_files(notebook_dir: str, cell_name: str, code_lines_only: list[str], id: int) -> None:

    with open(f"{notebook_dir}/{id}_{cell_name}.py", "w", encoding="utf-8") as f:
        f.write('\n'.join(code_lines_only) + '\n')

    print(f"Created {cell_name}.py")


# Checks if metadata was provided for the cell
def metadata_check(cell: str) -> bool:
    metadata_identifiers = ["# NaaVRE:", "#  cell:"]
    cell_text = cell.source.split("\n")  # Convert to a list of lines

    # Check if required metadata identifiers exist in the cell
    if all(any(identifier in line for line in cell_text) for identifier in
           metadata_identifiers):
        return True
    else:
        return False


# Creates metadata file for each cell
def build_metadata_file(notebook_name: str, metadata: list[str]) -> None:
    # Remove '#' from comments and join metadata lines
    cleaned_metadata = "\n".join(line.lstrip("# ").strip() for line in metadata)

    # Save directly as a YAML file
    yaml_filename = f"modularization/{notebook_name}/metadata.yaml"
    try:
        with open(yaml_filename, "w", encoding="utf-8") as yaml_file:
            yaml_file.write(cleaned_metadata)
        print(f"Extracted metadata saved as YAML: {yaml_filename}")
    except Exception as e:
        print(f"Error saving YAML file for {notebook_name}: {e}")


def split_notebook(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # The name of the primary notebook file
    notebook_name = os.path.splitext(notebook_path)[0].split("/")[0]
    # Ensure the target directory exists
    notebook_dir = f"{folder_name}/{notebook_name}"
    os.makedirs(notebook_dir, exist_ok=True)

    metadata = []

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code":
            # Check if metadata exists in the cell
            if metadata_check(cell):
                # Separate the code lines & metadata
                code_lines = []
                cell_lines = cell.source.split("\n")
                cell_name = (cell_lines[0].split("# ")[1])
                for line in cell_lines:
                    if line.lstrip()[0] != "#":
                        code_lines.append(line)
                    else:
                        metadata.append(line)
                create_cell_files(notebook_dir, cell_name, code_lines, i)
    build_metadata_file(notebook_name, metadata)


if __name__ == "__main__":
    with open("modified_notebooks.txt", "r", encoding="utf-8") as f:
        notebooks = f.read().splitlines()

    for nb_file in notebooks:
        if os.path.exists(nb_file):
            split_notebook(nb_file)
        else:
            print(f"Warning: {nb_file} does not exist.")