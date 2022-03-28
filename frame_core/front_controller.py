import datetime
import urllib.parse


def request_datetime(environ):
    return {'requested_datetime': datetime.datetime.now()}


def base_middleware(environ):
    result = {'URL': environ['PATH_INFO'],
              'QUERY_STRING': environ['QUERY_STRING']}
    method = environ['REQUEST_METHOD']

    if method == 'GET':
        value = environ['QUERY_STRING']
        value = dict(urllib.parse.parse_qsl(value))

    if method == 'POST':
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length).decode('utf-8') if content_length > 0 else ''
        data = dict(urllib.parse.parse_qsl(data, keep_blank_values=True))
        value = data

    if method:
        result[method] = value

    result['REQUEST_METHOD'] = method

    return result
