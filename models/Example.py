from models.Model import Model, Attribute


class Example(Model):
    args = {
        'id': Attribute(methods=['get'], type=int),
        'name': Attribute(methods=['get', 'post', 'put'],
                          mandatory=['post'], type=str),
    }

    # The order of decorator is important, call the method first, then url
    # If using the url decorator, must return a dict of params
    # If not, must return a couple of url, params
    @Model.method('GET')
    @Model.url('/examples/')
    def get(self, **params):
        return params

    @Model.method('POST')
    @Model.url('/example')
    def post(self, **params):
        return params

    @Model.method('PUT')
    @Model.url('/example/{id}')
    def put(self, **params):
        return params
