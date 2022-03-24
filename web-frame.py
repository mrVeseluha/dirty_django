from wsgiref.simple_server import make_server

from frame_core.urls import ROUTES
from frame_core.middleware import MIDDLEWARE
from settings import INSTALLED_APPS

import importlib

# Сначала я экспериментировал с прописыванием пользовательского приложения в ручную
# import my_app.urls
# ROUTES.update(my_app.urls.ROUTES)

# Позже я решил позаимствовать решение из Django и прописать пользовательские приложения в settings.py
for app in INSTALLED_APPS:
    # с начала я не знал, как преобразовать строковое название пользовательского приложения в оъект Python
    # поэтому я попробовал команды исполняющие выражения в строках
    # exec(f'import {app}.urls')
    # exec(f'ROUTES.update({app}.urls.ROUTES)')
    # но я знал, что это "плохая практика" и изучив матчасть открыл для себя модуль importlib
    # try:
    app = importlib.import_module(app + '.urls')
    # except:
    #     raise Exception(f'Error during attempt to import "{app}" user-application')
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

    # Except error
    if 'error' in environ['PATH_INFO'].lower():
        raise Exception('Detect "error" in URL path')
    # считываем значение URL из переменной environ и переводим его в нижний регистр
    path = environ['PATH_INFO'].lower()
    # проверяем наличие закрывающего бэкслэша и если его нет то добавляем
    path = path if path[-1] == '/' else path + '/'
    # получаем view функцию из списка ROUTES или None если его нет
    view_class = ROUTES.get(path)
    # если функция существует, то вызываем её и записываем результаты в code и body
    if view_class:
        code, body = view_class(request).get_page()
    else:
        code, body = '404 WHAT', [b'404 PAGE Not Found']
    start_response(code, [('Content-Type', 'text/html')])
    return body

with make_server('', 9999, application) as httpd:
    print("Webserver is running at http://localhost:9999")
    httpd.serve_forever()
