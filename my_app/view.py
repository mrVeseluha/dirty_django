from frame_core.view import BaseView, PandasTableView
import pandas as pd
from urllib.parse import unquote
import pickle
import os


class myView(BaseView):
    template = 'abc.html'


class myPandasView(PandasTableView):
    df = pd.read_csv(
        'https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv')
    template = 'pandas_view_example.html'

    def POST(self):
        csv = self.request['POST'].get('csv')
        if csv:
            self.df = pd.read_csv(unquote(unquote(csv)))
        return self.GET()


class myMessageBoardView(BaseView):
    template = 'message_board.html'
    model_name = 'message_board.pkl'

    def get_context(self):
        context = super(myMessageBoardView, self).get_context()
        if os.path.exists(self.model_name):
            with open(self.model_name, 'rb') as f:
                data = pickle.load(f)
            context['messages'] = data
        return context

    def POST(self):
        if os.path.exists(self.model_name):
            with open(self.model_name, 'rb') as f:
                data = pickle.load(f)
        else:
            data = []

        data.append(self.request.get('POST'))

        with open(self.model_name, 'wb') as f:
            pickle.dump(data, f)

        return self.GET()
