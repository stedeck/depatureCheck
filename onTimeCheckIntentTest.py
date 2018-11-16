import unittest
from awsLambda import lambda_handler

class OnTimeCheckIntentTest(unittest.TestCase):
    def testIntent(self):
        request = open('sampleIntentRequest.json', 'r')
        response = lambda_handler(request, None)
        print(response)
