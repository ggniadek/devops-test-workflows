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
        dependencies: list[str],
        root_dir: str
):
    code_dir_path = Path(root_dir, archive_name)
    if not os.path.exists(code_dir_path):
        os.makedirs(code_dir_path)
    try:
        lambda_file_path = Path(code_dir_path, LAMBDA_FILE)
        with open(lambda_file_path, 'w+') as f:
            f.write(code)
        for dependency in dependencies:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--target", code_dir_path, dependency]
            )
        archive_path = Path(root_dir, archive_name)
        return shutil.make_archive(str(archive_path), ARCHIVE_FORMAT, code_dir_path)
    finally:
        shutil.rmtree(code_dir_path)