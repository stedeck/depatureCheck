import requests
import xml.etree.ElementTree as ET

BASE_URL = 'http://openservice-test.vrr.de/static02/XML_DM_REQUEST'


# TODO add date and time
def getDepatures(stop_id, line, direction, limit=1):
    r = requests.get(
        '{url}?sessionID=0&requestID=0&language=DE&locationServerActive=1&name_dm={stop_id}&type_dm=stopId&useRealtime=1&mode=direct&limit={limit}&line={line}'
            .format(url=BASE_URL, stop_id=stop_id, line=line, limit=limit))
    return responseToDepatureList(r.text)

def responseToDepatureList(response):
    root = ET.fromstring(response)

    depature_list = []
    for depature in root.find('itdDepartureMonitorRequest/itdDepartureList'):
        depature_date = depature.find('itdDateTime/itdDate').attrib
        depature_time = depature.find('itdDateTime/itdTime').attrib

        has_rt = False
        if depature.find('itdRTDateTime') is not None:
            has_rt = True
            depature_rt_date = depature.find('itdRTDateTime/itdDate').attrib
            depature_rt_time = depature.find('itdRTDateTime/itdTime').attrib

        delay = depature.find('itdServingLine/itdNoTrain').attrib['delay']

        list_entry = {'year': int(depature_date['year']), 'month': int(depature_date['month']), 'day': int(depature_date['day']),
                'hour': int(depature_time['hour']), 'minute': int(depature_time['minute']),
                'delay': int(delay)}
        if has_rt:
            list_entry['rt'] = {'year': int(depature_rt_date['year']), 'month': int(depature_rt_date['month']), 'day': int(depature_rt_date['day']),
                             'hour': int(depature_rt_time['hour']), 'minute': int(depature_rt_time['minute'])}
        depature_list.append(list_entry)
    return depature_list