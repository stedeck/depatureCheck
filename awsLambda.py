import requests
import xml.etree.ElementTree as ET

BASE_URL = 'http://openservice-test.vrr.de/static02/XML_DM_REQUEST'
STOP_ID = '20021986'
LINE_NAME = 'U76'
LINE_DIRECTION = 'Düsseldorf Hbf'

def lambda_handler(event, context):
    r = requests.get(
        '{url}?sessionID=0&requestID=0&language=DE&locationServerActive=1&name_dm={stop_id}&type_dm=stopId&useRealtime=1&mode=direct&limit=1&line=rbg:70076::H'
            .format(url=BASE_URL, stop_id=STOP_ID))
    root = ET.fromstring(r.text)

    next_depature = root.find('itdDepartureMonitorRequest/itdDepartureList')[0]
    next_depature_time = next_depature.find('itdDateTime/itdTime').attrib

    next_depature_rt = None
    if next_depature.find('itdRTDateTime') is not None:
        next_depature_rt = next_depature.find('itdRTDateTime/itdTime').attrib

    delay = int(next_depature.find('itdServingLine/itdNoTrain').attrib['delay'])

    text = 'Das kann ich dir leider noch nicht sagen, nerd'
    if delay == -9999:
        text = 'Die nächste Bahn fällt aus. Planmäßige Abfahrt wäre {h} Uhr {m} gewesen'\
            .format(h=next_depature_time['hour'], m=next_depature_time['minute'])
    if delay == 0:
        text = 'Die nächste Bahn fährt planmäßig um {h} Uhr {m}'\
            .format(h=next_depature_time['hour'], m=next_depature_time['minute'])
    if delay >0:
        text = 'Die nächste Bahn fährt um {h_rt} Uhr {m_rt}. Planmäßige Abfahrt wäre {h} Uhr {m} gewesen'.format(
            h=next_depature_time['hour'], m=next_depature_time['minute'],
            h_rt=next_depature_time['hour'], m_rt=next_depature_rt['minute']
        )

    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': text
            }
        },
        'shouldEndSession': True
    }

    return response
