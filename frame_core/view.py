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
    filter = None

    def get_context(self):
        context = super(PandasTableView, self).get_context()
        df = self.df

        if self.request.get('GET'):
            sort_field = self.request['GET'].get('sort')
            if sort_field and ('-' == sort_field[0]):
                sort_field = sort_field[1:]
                ascending = False
            else:
                ascending = True
            if sort_field and (sort_field in df.columns):
                df.sort_values(by=sort_field, ascending=ascending, inplace=True)

            filter = self.request['GET'].get('filter')
            if filter and (filter in df.columns):
                context['filter'] = {'name': filter,
                                     'values': df[filter].unique()}
                for key, val in self.request['GET'].items():
                    if (key in df.columns) and val:
                        try:
                            val = int(val)
                        except:
                            try:
                                val = float(val)
                            except:
                                pass
                        df = df[df[key] == val]

        context['data_frame'] = df
        return context
