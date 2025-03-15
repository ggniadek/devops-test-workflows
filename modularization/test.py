import os
os.environ['HOME'] = '/tmp'

from icoscp_core.icos import bootstrap
import slugify
from icoscp import cpauth
from icoscp.station import station
import warnings
from icoscp.cpb.dobj import Dobj
import matplotlib.pyplot as plt
import pandas as pd

vars_dict = {}


def lambda_handler(event, context):
    # Handling ingestion of previously defined variables
    # Allows for the variables to be used.
    if "metadata" in event:
        metadata = event["metadata"]
        for key, value in metadata.items():
            globals()[key] = value

    #########
    
    # (Do not containerize, NaaVRE workflow parameters cell)
    
    param_cpauth_token = 'cpauthToken=WzE3NDIwNjY1OTU3NTQsImdvbmNhbG9qZmVycmVpcmE5MkBnbWFpbC5jb20iLCJQYXNzd29yZCJdHjBkAjBU/GTjQu1KMdGJOFs2sq1C+WThwrVJ35fG147h0ZJ7vHGbGZF2S8S8TDuKlLjsfKoCMBQuB+PJqU41YDCh8ay1HsWYolRvCjyHpIs+H333f9k39zHxXhQI8cEVb+diaaaCdQ=='
    
    param_ecosystem_type = 'Wetland'
    param_data_type = 'ETC L2 Fluxes'
    param_variable = 'CO2'

    #########

    local_vars = locals()
    local_vars_dict_curr = {
        k: v
        for k, v in local_vars.items()
        if not (
            k.startswith("key")
            or k.startswith("value")
            or k.startswith("event")
            or k.startswith("metadata")
            or k.startswith("context")
        )
    }

    # Handling export of current and previously defined variables
    # Exporting variables (both from current and previous workflows)
    var_list = globals()

    vars_dict_curr = {
        k: v
        for k, v in var_list.items()
        if not (
            k.startswith("__")
            or k.startswith("json")
            or k.startswith("lambda_handler")
            or k.startswith("vars_dict")
            or k.startswith("context")
            ### Add this to the code
            or k.startswith('os')
            or k.startswith('bootstrap')
            or k.startswith('slugify')
            or k.startswith('cpauth')
            or k.startswith('station')
            or k.startswith('warnings')
            or k.startswith('Dobj')
            or k.startswith('pd')
            or k.startswith('plt')
        )
    }

    for key, value in vars_dict_curr.items():
        if key == "event":
            # Ensure that there's no overwritten data
            if vars_dict.get(key) is None:
                if "metadata" in value:
                    vars_dict.update(value["metadata"])
        else:
            vars_dict.update({key: value})

    for key, value in local_vars_dict_curr.items():
        vars_dict.update({key: value})

    return {
        "metadata": vars_dict
    }
