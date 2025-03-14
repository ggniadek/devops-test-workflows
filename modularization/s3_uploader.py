import os
from pathlib import Path
import boto3
from unicodedata import normalize

BUILD_DIR_PATH = Path('build')
BUCKET_NAME = 'module-bucket-a60555b5-a452-46d5-8a9f-5248d2dc41a5'
s3 = boto3.client('s3')

def list_zips(notebook_dir: Path) -> list[Path]:
    paths = notebook_dir.iterdir()
    zips = []
    for path in paths:
        if not path.is_file():
            continue
        if path.suffix != '.zip':
            continue
        zips.append(path)
    return zips

def upload_notebook_zips(organization_name: str, notebook: Path, zips: list[Path]):
    for zip in zips:
        s3_key = f"{organization_name}/{notebook.name}/{zip.name}"
        s3.upload_file(zip, Bucket = BUCKET_NAME, Key = s3_key)

def upload_zips():
    if not BUILD_DIR_PATH.exists():
        print("No build directory detected, exiting")
        return

    organization_name = os.getenv("GITHUB_REPOSITORY_OWNER")
    print(f"Github repository owner determined as {organization_name}")

    notebooks = [path for path in BUILD_DIR_PATH.iterdir() if path.is_dir()]
    print(f"Found {len(notebooks)} notebooks")
    for notebook in notebooks:
        zips = list_zips(notebook)
        print(f"Uploading {notebook.name} to S3...")
        upload_notebook_zips(organization_name, notebook, zips)
        print(f"Uploaded {notebook.name} to S3")