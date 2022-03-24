from jinja2 import Template
import os


class BaseView():
    template = None

    def __init__(self, request):
        self.request = request

    def get_page(self):
        return self.getCode(), [self.getBody()]

    def getCode(self):
        return '200 OK'

    def get_context(self):
        return self.request

    def getBody(self):
        if self.template:
            return self.render(**self.get_context())
        else:
            return b''

    def render(self, folder='templates/', **kwargs):
        """
        :param folder: папка в которой ищем шаблон
        :param kwargs: параметры
        :return:
        """
        file_path = os.path.join(os.path.abspath(folder), self.template)
        if not os.path.exists(file_path):
            raise Exception('Template file doesn\'t exist!')
        # Открываем шаблон по имени
        with open(file_path, encoding='utf-8') as f:
            template = Template(f.read())
        return bytes(template.render(**kwargs), 'utf-8')


class IndexView(BaseView):
    template = 'index.html'

class PandasTableView(BaseView):
    df = None

    def get_context(self):
        context = super(PandasTableView, self).get_context()
        context['data_frame'] = self.df
        return context
