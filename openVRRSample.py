import requests
import xml.etree.ElementTree as ET

r = requests.get('http://openservice-test.vrr.de/static02/XML_DM_REQUEST?sessionID=0&requestID=0&language=DE&locationServerActive=1&name_dm=20021986&type_dm=stopId&useRealtime=1&mode=direct&limit=1&line=rbg:70076::H') #&itdDate=20181115&itdDateDay=15&itdDateMonth=11&itdDateYear=2018&')
root = ET.fromstring(r.text)

next_depature = root.find('itdDepartureMonitorRequest/itdDepartureList')[0]
next_depature_time = next_depature.find('itdDateTime/itdTime').attrib

next_depature_rt = None
if next_depature.find('itdRTDateTime') is not None:
    next_depature_rt = next_depature.find('itdRTDateTime/itdTime').attrib

print('depature: {0}:{1}'.format(next_depature_time['hour'], next_depature_time['minute']))
if next_depature_rt is not None:
   print('depature: {0}:{1}'.format(next_depature_rt['hour'], next_depature_rt['minute']))

delay = next_depature.find('itdServingLine/itdNoTrain').attrib['delay']
print('delay: {0}'.format(delay))
