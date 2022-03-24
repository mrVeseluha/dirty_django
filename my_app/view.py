from frame_core.view import BaseView, PandasTableView
import pandas as pd


class myView(BaseView):
    template = 'abc.html'


class myPandasView(PandasTableView):
    df = pd.read_csv(
        'https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv')
    template = 'pandas_view_example.html'
