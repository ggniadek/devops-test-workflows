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
    
    
    meta, data = bootstrap.fromCookieToken(param_cpauth_token)
    cpauth.init_by(data.auth)
    
    
    plot_files = []
    for dobj_pid in dobj_list:
        dobj = Dobj(dobj_pid)
        unit = dobj.variables[dobj.variables.name == param_variable].unit.values[0]
        name = dobj.station['org']['name']
        uri = dobj.station['org']['self']['uri']
        title = f"{name} \n {uri}"
        plot = dobj.data.plot(x='TIMESTAMP', y=param_variable, grid=True, title=title)
        plot.set(ylabel=unit)
        filename = f'/tmp/data/{slugify.slugify(dobj_pid)}.pdf'
        plt.savefig(filename)
        plot_files.append(filename)
        plt.show()
    
    plot_files
