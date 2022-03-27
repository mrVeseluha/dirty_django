from jinja2 import Template, Environment, FileSystemLoader
import os


class BaseView():
    template = None

    def __init__(self, request):
        self.request = request

    def GET(self):
        if self.template:
            return self.render(**self.get_context())
        else:
            return b''

    def POST(self):
        return self.GET()

    def get_page(self):
        return self.getCode(), [getattr(self, self.request['REQUEST_METHOD'])()]

    def getCode(self):
        return '200 OK'

    def get_context(self):
        return self.request

    def render(self, folder='templates/', **kwargs):
        """
        :param folder: папка в которой ищем шаблон
        :param kwargs: параметры
        :return:
        """
        env = Environment(loader=FileSystemLoader(f'./{folder}'))
        template = env.get_template(self.template)

        return bytes(template.render(**kwargs), 'utf-8')


class IndexView(BaseView):
    template = 'index.html'


class PandasTableView(BaseView):
    df = None

    def get_context(self):
        context = super(PandasTableView, self).get_context()
        context['data_frame'] = self.df
        return context
