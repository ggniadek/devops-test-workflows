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
    
    param_cpauth_token = ''
    
    param_ecosystem_type = 'Wetland'
    param_data_type = 'ETC L2 Fluxes'
    param_variable = 'CO2'
