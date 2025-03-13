from pathlib import Path
import boto3

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

def upload_notebook_zips(zips: list[Path]):
    for zip in zips:
        s3.upload_file(zip, Bucket = BUCKET_NAME, Key = str(zip))

def upload_zips():
    test = Path('.').iterdir()
    for t in test:
        print(t)
    if not BUILD_DIR_PATH.exists():
        print("No build directory detected, exiting")
        return
    notebooks = [path for path in BUILD_DIR_PATH.iterdir() if path.is_dir()]
    for notebook in notebooks:
        zips = list_zips(notebook)
        upload_notebook_zips(zips)