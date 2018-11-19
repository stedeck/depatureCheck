import unittest
import sys
sys.path.append('../source/openVRR')
import codecs

from depatureMonitor import responseToDepatureList

expected_depatures = [{
    'year': 2018, 'month': 11, 'day': 15, 'hour': 21, 'minute': 19,
    'delay': -9999
},{
    'year': 2018, 'month': 11, 'day': 15, 'hour': 21, 'minute': 29,
    'rt': {'year': 2018, 'month': 11, 'day': 15, 'hour': 21, 'minute': 29},
    'delay': 0
},{
    'year': 2018, 'month': 11, 'day': 15, 'hour': 21, 'minute': 47,
    'rt': {'year': 2018, 'month': 11, 'day': 15, 'hour': 21, 'minute': 48},
    'delay': 1
}]

class depatureMonitorTests(unittest.TestCase):
    def test_responseToDepatureList(self):
        with codecs.open('./dmResponse.xml', 'r', 'iso-8859-1') as response_file:
            response = response_file.read()
        depatures = responseToDepatureList(response)
        self.assertListEqual(depatures, expected_depatures)