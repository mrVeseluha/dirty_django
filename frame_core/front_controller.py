import datetime
import urllib.parse


def request_datetime(environ):
    return {'requested_datetime': datetime.datetime.now()}


def base_middleware(environ):
    def parse_input_data(data: str):
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    result = {'URL': environ['PATH_INFO'],
              'QUERY_STRING': environ['QUERY_STRING']}
    method = environ['REQUEST_METHOD']
    if method == 'GET':
        value = parse_input_data(environ['QUERY_STRING'])
    if method == 'POST':
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length).decode('utf-8') if content_length > 0 else ''
        data = urllib.parse.parse_qs(data, keep_blank_values=True)
        data = dict((key, val if len(val) > 1 else val[0]) for key, val in data.items())
        value = data
    if method:
        result[method] = value
    result['REQUEST_METHOD'] = method

    data = environ.get('CONTENT_LENGTH')

    return result
