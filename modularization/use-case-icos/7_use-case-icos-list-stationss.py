from icoscp.station import station
import matplotlib.pyplot as plt
import os
from icoscp_core.icos import bootstrap
import warnings
import pandas as pd
from minio import Minio
from icoscp import cpauth
import slugify
from icoscp.cpb.dobj import Dobj

def lambda_handler(event, context):
    
    
    stations = station.getIdList()
    stations = stations[stations.siteType == param_ecosystem_type]
    stations_id_list = list(stations.id)
    
    stations_id_list
