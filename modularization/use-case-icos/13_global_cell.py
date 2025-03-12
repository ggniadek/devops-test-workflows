import os
from icoscp_core.icos import bootstrap
import warnings
from icoscp.cpb.dobj import Dobj
from icoscp import cpauth
from icoscp.station import station
import pandas as pd
from minio import Minio
import matplotlib.pyplot as plt
import slugify

def lambda_handler(event, context):
    
    param_s3_server = "scruffy.lab.uvalight.net:9000"
    param_s3_bucket = "naa-vre-user-data"
    
    param_s3_user_prefix = ""
    param_s3_access_key = ""
    param_s3_secret_key = ""
