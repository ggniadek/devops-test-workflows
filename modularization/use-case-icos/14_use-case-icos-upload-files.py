
import os
from minio import Minio

minio_client = Minio(param_s3_server, access_key=param_s3_access_key, secret_key=param_s3_secret_key, secure=True)

for plot_file  in plot_files:
    print("Uploading", plot_file)
    object_name = f'{param_s3_user_prefix}/vl-openlab/icos-naavre-demo/{os.path.basename(plot_file)}'
    minio_client.fput_object(param_s3_bucket, object_name=object_name, file_path=plot_file)
