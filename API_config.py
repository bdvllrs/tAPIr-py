from requests.auth import HTTPBasicAuth, HTTPDigestAuth


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

    def digest_auth(self, username, password):
        self.set_auth(HTTPDigestAuth(username, password))

    def class_auth(self, auth_obj, *params):
        self.set_auth(auth_obj(*params))

    def set_global_arg(self, key, value):
        """
        Add or edit a global argument
        """
        self.args[key] = value

    def get_global_arg(self, key):
        """
        Get the value of a global argument
        """
        return self.args[key]
