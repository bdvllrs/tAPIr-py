from requests.auth import HTTPBasicAuth


class API_CONFIG:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.use_auth = False
        self.use_token = False

    def auth(self, authObj):
        self.use_auth = True
        self.auth = authObj

    def basicAuth(self, username, password):
        self.auth(HTTPBasicAuth(username, password))

    def tokenAuth(self, token, field='token'):
        self.use_auth = True
        self.use_token = True
        self.auth_token = token
        self.auth_token_field = field
