from wsgiref.simple_server import make_server

from frame_core.urls import ROUTES
from frame_core.middleware import MIDDLEWARE
from settings import INSTALLED_APPS, SERVER_PORT, STATIC_ROOT, STATIC_URL

import importlib
import mimetypes
import os
from http import cookies

# Сначала я экспериментировал с прописыванием пользовательского приложения вручную
# import my_app.urls
# ROUTES.update(my_app.urls.ROUTES)

# Позже я решил позаимствовать решение из Django и прописать пользовательские приложения в settings.py
for app in INSTALLED_APPS:
    # я не знал, как преобразовать строковое название пользовательского приложения в оъект Python
    # поэтому я попробовал команды исполняющие выражения в строках
    # exec(f'import {app}.urls')
    # exec(f'ROUTES.update({app}.urls.ROUTES)')
    # но я знал, что это "плохая практика" и изучив матчасть открыл для себя модуль importlib
    try:
        app = importlib.import_module(app + '.urls')
    except:
        raise Exception(f'Error during attempt to import "{app}" user-application')
    try:
        ROUTES.update(app.ROUTES)
    except:
        raise Exception(f'Error during load users urls from {app}.urls.py')


def application(environ, start_response):
    # объявим переменную request для view функций, как пустой словарь
    request = dict()
    # в цикле переберём все функции из MIDDLEWARE и сохраним результаты в request
    for func in MIDDLEWARE:
        request.update(func(environ))
    request['STATIC_PREFIX'] = STATIC_URL

    # считываем значение URL из переменной environ и переводим его в нижний регистр
    path = environ['PATH_INFO'].lower()

    # проверяем запрос на запрос файла, если начало url начинается с STATIC_URL то пришёл запрос на файл
    if path.startswith(STATIC_URL):
        # если файл существует
        if os.path.exists(STATIC_ROOT + path[len(STATIC_URL):]):
            # открываем его на чтение
            with open(STATIC_ROOT + path[len(STATIC_URL):], 'rb') as file:
                # читаем содержимое
                content = file.read()
            # при помощи стандартной библиотеки mimetypes определяем тип файла и формируем заголовок
            headers = [('content-type', mimetypes.guess_type(path)[0])]
            # возвращаем все данные в соответствии с PEP 3333
            start_response('200 OK', headers)
            return [content]

    # print(environ)
    C = cookies.SimpleCookie()
    if ('HTTP_COOKIE' in environ) and (path.replace('/', '_') in environ['HTTP_COOKIE']) and (
    not path.startswith(STATIC_URL)):
        C.load(environ['HTTP_COOKIE'])
        C[path.replace('/', '_')] = int(C[path.replace('/', '_')].value) + 1
        request['PAGE_ACCESS_COUNTER'] = C[path.replace('/', '_')].value
    else:
        if not path.startswith(STATIC_URL):
            C[path.replace('/', '_')] = 1
            request['PAGE_ACCESS_COUNTER'] = 1

    # проверяем наличие закрывающего бэкслэша и если его нет то добавляем
    path = path if path[-1] == '/' else path + '/'
    # получаем view функцию из списка ROUTES или None если его нет
    view_class = ROUTES.get(path)
    # если функция существует, то вызываем её и записываем результаты в code и body
    if view_class:
        code, body = view_class(request).get_page()
    else:
        code, body = '404 WHAT', [b'404 PAGE Not Found']
    headers = [('Content-Type', 'text/html\n' + C.output())]
    start_response(code, headers)
    return body


with make_server('', SERVER_PORT, application) as httpd:
    print(f"Webserver is running at http://localhost:{SERVER_PORT}")
    httpd.serve_forever()
