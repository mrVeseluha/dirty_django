import datetime


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

    result = dict()
    method = environ['REQUEST_METHOD']
    if method == 'GET':
        value = parse_input_data(environ['QUERY_STRING'])
    if method == 'POST':
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        value = parse_input_data(data.decode(encoding='utf-8'))
    if method:
        result[method] = value

    data = environ.get('CONTENT_LENGTH')
    print(data)

    return result
