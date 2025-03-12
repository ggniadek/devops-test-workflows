import os
from minio import Minio
from icoscp import cpauth
from icoscp.station import station
import pandas as pd
from icoscp.cpb.dobj import Dobj
import warnings
import slugify
import matplotlib.pyplot as plt
from icoscp_core.icos import bootstrap

def lambda_handler(event, context):
    
    
    stations = station.getIdList()
    stations = stations[stations.siteType == param_ecosystem_type]
    stations_id_list = list(stations.id)
    
    stations_id_list
