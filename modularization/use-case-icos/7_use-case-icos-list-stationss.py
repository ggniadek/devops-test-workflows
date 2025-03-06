
from icoscp.station import station

stations = station.getIdList()
stations = stations[stations.siteType == param_ecosystem_type]
stations_id_list = list(stations.id)

stations_id_list
