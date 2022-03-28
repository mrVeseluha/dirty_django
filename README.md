# dirty_django
В ручную написаный wsgi web-фреймворк для быстрой разработки web-приложений.

Состоит из следующих компонентов:

web-frame.py - Основной файл фреймворка, который надо запускать после настройки клиентского приложения

(перед запуском необходимо выполнить команду "pip install -r requirements.txt" для установки зависимых библиотек)

frame_core - Пакет содержащий основные объекты фреймворка такие как:
- front_controller.py - файл содержит функции middleware патерна front-controller. На входе функция получает wsgi параметры environ, а в качестве результата возвращает словарь содержащий параметры для функции рендеринга.
- middleware.py - файл содержит переменную-список MIDDLEWARE содержащий функции из front_controller.py, которые используются для обработки запросов сервера.
- view.py - содержит классы "контроллеры", которые используются для рендеринга web-страниц. Паттерн page-controller.
- url.py - файл содержит словарь ROUTES, в котором в качестве ключа используется url-адресс, а значение это класс используемый для рендеринга. По умолчанию содержит только ссылку на домашнюю страницу '/', которая ссылается на класс IndexView, который отображает содержимое из файла-шаблона index.html

templates - Папка в которой хранятся шаблоны для отображения web-страниц. Шаблоны обрабатываются при помощи библиотеки Jinja2.

Реализация пользовательского web-приложения происходит следующим образом:
1) Создаётся Python-пакет с названием, которое будет иметь польлзовательское приложение.
2) В файле settings.py в переменную-список INSTALLED_APPS надо добавить название пользовательского приложения.
3) В ползовательском пакете надо создать файл urls.py в котором в словаре ROUTES надо сопоставить url-адреса и классы из пользовательского view.py
4) В пользовательском пакете надо добавить view.py, в котором прописать классы для рендеринга страниц. Классы можно наследовать от классов frame_core.view где прописаны некоторые view-классы дженерики.

Классы дженерики в frame_core.view:
- BaseView - базовый класс для рендеринга страниц. Что бы добавить параметры для шаблонизатора надо переопределить метод get_context который по умолчанию возвращает request. А для указания файла-шаблона надо переопределить переменную template.
- IndexView - класс наследник от BaseView с переопределённой переменной template, которая ссылается на index.html.
- PandasTableView - класс наследник от BaseView, который используется для отображения данных из дата-фреймов библиотеки Pandas. Содержит переменную df, которую надо переопределить и записать в неё объект pandas.DataFrame()

Пользовательское приложение my_app

В качестве примера уже инсталированно пользовательское приложение my_app, в котором можно отображать страницы по следующим url-адресам:
- /abc/ - обычная страница из файла-шаблона abc.html
- /pandas/ - страница использующая файл-шаблон pandas_view_example.html и класс-дженерик PandasTableView(). На странице показана таблица из классического набора данных Iris.

На всех страницах присутствует информация о точном времени, когда страница была запрошена. Это реализовано при помощи middleware контроллера.

TODO:
- Привести к единому стилю написание имён переменных (camelCase, PascalCase, snake_case)
- Дать возможность пользователю определять собственные методы middleware без изменения кода ядра фреймворка
- Получить пятёрку за домашку ;-)
