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
    !pip install icoscp==0.2.2 icoscp_core==0.3.9 matplotlib python-slugify
