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
    
    
    dobj_list = []
    for station_id in stations_id_list:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            s = station.get(station_id)
            datasets = s.data()
        if isinstance(d, str) and (d == 'no data available'):
            print(f'No datasets for station {station_id}')
            continue
        datasets = datasets[datasets.specLabel == param_data_type]
        dobj_list += list(datasets.dobj)
    
    dobj_list
