import subprocess
import sys
import shutil
import os
from pathlib import Path

LAMBDA_FILE = "lambda_function.py"
ARCHIVE_FORMAT = 'zip'

def make_lambda_archive(
    archive_name: str,
    code: str,
    root_dir: str
):
    code_dir_path = Path(root_dir, archive_name)
    if not os.path.exists(code_dir_path):
        os.makedirs(code_dir_path)
    lambda_file_path = Path(code_dir_path, LAMBDA_FILE)
    with open(lambda_file_path, 'w+') as f:
        f.write(code)
    archive_path = Path(root_dir, archive_name)
    return shutil.make_archive(str(archive_path), ARCHIVE_FORMAT, code_dir_path)

PYTHON_RUNTIME = 'python3.11'
DEPENDENCY_PATH = Path('python', 'lib', PYTHON_RUNTIME, 'site-packages')

def make_layer_archive(
    layer_name: str,
    dependencies: list[str],
    root_dir: str
):
    layer_dir_path = Path(root_dir, layer_name)
    dependency_dir_path = Path(layer_dir_path, DEPENDENCY_PATH)
    if not os.path.exists(dependency_dir_path):
        os.makedirs(dependency_dir_path)
    for dependency in dependencies:
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '--platform', 'manylinux2014_x86_64', '--target', dependency_dir_path, '--implementation', 'cp', '--python-version', '3.11', '--only-binary=:all:', dependency]
        )
    return shutil.make_archive(str(layer_dir_path), ARCHIVE_FORMAT, layer_dir_path, DEPENDENCY_PATH)

