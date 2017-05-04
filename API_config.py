from requests.auth import HTTPBasicAuth


class API_CONFIG:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.args = {}
        self.use_auth = False
        self.auth = None
        self.use_token = False

    def set_auth(self, authObj):
        self.use_auth = True
        self.auth = authObj

    def basic_auth(self, username, password):
        self.set_auth(HTTPBasicAuth(username, password))

    def token_auth(self, token, field='token'):
        self.use_auth = True
        self.use_token = True
        self.auth_token = token
        self.auth_token_field = field

    def set_global_arg(self, key, value):
        self.args[key] = value

    def get_global_arg(self, key):
        return self.args[key]
