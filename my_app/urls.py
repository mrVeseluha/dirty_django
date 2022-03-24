from .view import myView, myPandasView

ROUTES = {
    '/abc/': myView,
    '/pandas/': myPandasView,
}