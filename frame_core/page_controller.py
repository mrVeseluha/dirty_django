from pprint import pprint
import datetime

def request_datetime(environ):
    return {'requested_datetime': datetime.datetime.now()}
