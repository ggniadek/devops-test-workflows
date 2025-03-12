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
    
    
    stations = station.getIdList()
    stations = stations[stations.siteType == param_ecosystem_type]
    stations_id_list = list(stations.id)
    
    stations_id_list
