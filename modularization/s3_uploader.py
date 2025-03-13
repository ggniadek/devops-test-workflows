from pathlib import Path
import boto3

BUILD_DIR = Path('modularization/build')
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

def upload_zips(zips: list[Path]):
    for zip in zips:
        s3.upload_file(zip, Bucket = BUCKET_NAME, Key = str(zip))

def main():
    notebooks = [path for path in BUILD_DIR.iterdir() if path.is_dir()]
    for notebook in notebooks:
        zips = list_zips(notebook)
        upload_zips(zips)

if __name__ == '__main__':
    main()