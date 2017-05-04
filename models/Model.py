import requests
import json


class APIError(Exception):
    pass


class InvalidToken(APIError):
    pass


class ParameterError(APIError):
    pass


class NotFound(APIError):
    pass


class UnauthorizedRequest(APIError):
    pass


class BadRequest(APIError):
    pass


class Model:

    def __init__(self, config):
        self.config = config

    def get_args(self, method):
        """
        Get the available and mandatory arguments associated
        to the given method
        :param method: method
        :return: couple composed of the allowed and mandatory fields
        :rtype: tuple
        """
        allowed, mandatory = [], []
        for name, arg in self.args.items():
            if method in arg.methods:
                allowed.append(name)
                if((isinstance(arg.mandatory, bool) and
                    arg.mandatory) or
                   (isinstance(arg.mandatory, list) and
                        method in arg.mandatory)):
                    mandatory.append(name)
        return allowed, mandatory

    def _get(self, url, **params):
        """
        Get method
        :param url: url relative to the config.endpoint
        :param params: fields for the request
        """
        allowed, mandatory = self.get_args('get')
        fields = self._build_request('get', allowed, mandatory, **params)
        url = self.config.endpoint + url
        if self.config.use_auth and self.config.use_token:
            fields[self.config.auth_token_field] = self.config.auth_token
            request = requests.get(url, fields)
        elif self.config.use_auth:
            request = requests.get(url, fields, auth=self.config.auth)
        else:
            request = requests.get(url, fields)
        return self._build_response(request)

    def _post(self, url, **params):
        allowed, mandatory = self.get_args('post')
        fields = self._build_request('post', allowed, mandatory, **params)
        url = self.config.endpoint + url
        if self.config.use_auth and self.config.use_token:
            fields[self.config.auth_token_field] = self.config.auth_token
            request = requests.post(url, fields)
        elif self.config.use_auth:
            request = requests.post(url, fields, auth=self.config.auth)
        else:
            request = requests.post(url, fields)
        return self._build_response(request)

    def _put(self, url, **params):
        allowed, mandatory = self.get_args('put')
        fields = self._build_request('put', allowed, mandatory, **params)
        url = self.config.endpoint + url
        if self.config.use_auth and self.config.use_token:
            fields[self.config.auth_token_field] = self.config.auth_token
            request = requests.put(url, fields)
        elif self.config.use_auth:
            request = requests.put(url, fields, auth=self.config.auth)
        else:
            request = requests.put(url, fields)
        return self._build_response(request)

    def _patch(self, url, **params):
        allowed, mandatory = self.get_args('patch')
        fields = self._build_request('patch', allowed, mandatory, **params)
        url = self.config.endpoint + url
        if self.config.use_auth and self.config.use_token:
            fields[self.config.auth_token_field] = self.config.auth_token
            request = requests.patch(url, fields)
        elif self.config.use_auth:
            request = requests.patch(url, fields, auth=self.config.auth)
        else:
            request = requests.patch(url, fields)
        return self._build_response(request)

    def _delete(self, url, **params):
        allowed, mandatory = self.get_args('delete')
        fields = self._build_request('delete', allowed, mandatory, **params)
        url = self.config.endpoint + url
        if self.config.use_auth and self.config.use_token:
            fields[self.config.auth_token_field] = self.config.auth_token
            request = requests.delete(url, data=fields)
        elif self.config.use_auth:
            request = requests.delete(url, data=fields, auth=self.config.auth)
        else:
            request = requests.put(url, data=fields)
        return self._build_response(request)

    def _build_response(self, response):
        response.encoding = 'utf-8'
        code = response.status_code
        if code == 404:
            raise NotFound('La requête demandé n\'est pas disponible.')

        data = json.loads(response.content)

        if code == 403:  # FORBIDDEN
            raise InvalidToken(data)
        elif code == 400:
            raise ParameterError(data)
        elif code == 401:
            raise UnauthorizedRequest(data)
        elif code != 200:
            raise BadRequest('La requête est invalide.')
        return data

    def _build_request(self, method, allowed=[], mandatory=[], **params):
        """
        Build the request
        :param method: met
        """
        fields = {}
        for key, val in params.items():
            # If dict, we take the type coresponding to the method
            if(key not in self.args.keys() or
               method not in self.args[key].methods):
                raise ParameterError('The parameter ' +
                                     key + ' is not allowed.')
            if isinstance(self.args[key].type, dict):
                type = self.args[key].type[method]
            else:
                type = self.args[key].type
            if not isinstance(val, type):
                raise ParameterError('The parameter ' +
                                     key + ' should be of type ' +
                                     type.__name__ + '.')
            if key in allowed:
                fields[key] = val
        for m in mandatory:
            if m not in fields.keys():
                raise ParameterError('The parameter ' + m + ' is required.')
        return fields

    @staticmethod
    def url(url):
        def decorate(func):
            def wrapper(self, **params):
                return url, params
            return wrapper
        return decorate

    @staticmethod
    def method(method):
        def decorate(func):
            def wrapper(self, **params):
                params = func(self, **params)
                if '_url' in params.keys():
                    url = params['_url']
                else:
                    raise 
                if method.lower() == 'get':
                    response = self._get(url, **params)
                elif method.lower() == 'post':
                    response = self._post(url, **params)
                elif method.lower() == 'put':
                    response = self._put(url, **params)
                elif method.lower() == 'patch':
                    response = self._patch(url, **params)
                elif method.lower() == 'delete':
                    response = self._delete(url, **params)
                return response
            return wrapper
        return decorate


class Attribute:
    def __init__(self, methods=[], mandatory=[], type=None):
        self.methods = methods
        self.mandatory = mandatory
        self.type = type
