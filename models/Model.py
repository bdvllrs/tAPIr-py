import requests
import json
import re
import copy


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
        fields, headers, _ = self._build_request('get',
                                                 allowed,
                                                 mandatory,
                                                 **params)
        url = self.config.endpoint + url
        request = requests.get(url, fields,
                               auth=self.config.auth,
                               headers=headers)
        return self._build_response(request)

    def _post(self, url, **params):
        allowed, mandatory = self.get_args('post')
        fields, headers, content = self._build_request('post',
                                                       allowed,
                                                       mandatory,
                                                       **params)
        url = self.config.endpoint + url
        if content != {}:
            params = fields
            data = content
        else:
            data = fields
            params = {}
        request = requests.post(url, params=params, json=data, auth=self.config.auth,
                                headers=headers)
        return self._build_response(request)

    def _put(self, url, **params):
        allowed, mandatory = self.get_args('put')
        fields, headers, content = self._build_request('put', allowed,
                                                       mandatory, **params)
        url = self.config.endpoint + url
        if content != {}:
            params = fields
            data = content
        else:
            data = fields
            params = {}
        request = requests.put(url, params=params, json=data, auth=self.config.auth,
                               headers=headers)
        return self._build_response(request)

    def _patch(self, url, **params):
        allowed, mandatory = self.get_args('patch')
        fields, headers, content = self._build_request('patch', allowed,
                                                       mandatory, **params)
        url = self.config.endpoint + url
        if content != {}:
            params = fields
            data = content
        else:
            data = fields
            params = {}
        request = requests.patch(url, params=params, json=data, auth=self.config.auth,
                                 headers=headers)
        return self._build_response(request)

    def _delete(self, url, **params):
        allowed, mandatory = self.get_args('delete')
        fields, headers, content = self._build_request('delete', allowed,
                                                       mandatory, **params)
        url = self.config.endpoint + url
        if content != {}:
            params = fields
            data = content
        else:
            data = fields
            params = {}
        request = requests.delete(url, params=params, json=data, auth=self.config.auth,
                                  headers=headers)
        return self._build_response(request)

    def _build_response(self, response):
        response.encoding = 'utf-8'
        code = response.status_code
        if code == 404:
            raise NotFound('La requête demandé n\'est pas disponible.')
        # print(code, response.content)
        try:
            data = json.loads(response.content)
        except Exception as e:
            raise BadRequest(response.content)
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
        headers = {}
        content = {}
        for key, val in params.items():
            if not re.match('_{1,2}.*', key):
                # If dict, we take the type coresponding to the method
                if(key not in self.args.keys() or
                   method not in self.args[key].methods):
                    raise ParameterError('The parameter ' +
                                         key + ' is not allowed.')
                elif isinstance(self.args[key].type, dict):
                    type = self.args[key].type[method]
                else:
                    type = self.args[key].type
                if not isinstance(val, type):
                    raise ParameterError('The parameter ' +
                                         key + ' should be of type ' +
                                         type.__name__ + '.')
                if key in allowed:
                    fields[key] = val
            elif key == '__content':
                content = val
            elif key == '__headers':
                headers = val
        defaults = copy.copy(self.config.args)
        defaults.update(fields)
        fields = defaults
        for m in mandatory:
            if m not in fields.keys():
                raise ParameterError('The parameter ' + m + ' is required.')
        return fields, headers, content

    @staticmethod
    def url(addr):
        def decorate(func, addr=addr):
            def wrapper(self, addr=addr, **params):
                params = func(self, **params)
                regex = r'(?:[^{}])*{([a-zA-Z-9\_]*)}(?:[^{}])*'
                url_prog = re.compile(regex, re.DOTALL)
                if url_prog.match(addr):
                    res = url_prog.findall(addr)
                    for param in res:
                        if '_' + param in params.keys():
                            addr = addr.replace('{' + param + '}',
                                                str(params['_' + param]))
                        else:
                            raise ParameterError('The parameter _' +
                                                 param + ' is missing.')
                params['__url'] = addr
                if '__method' in params:
                    return self._call_api(params)
                return params
            return wrapper
        return decorate

    @staticmethod
    def method(method):
        def decorate(func):
            def wrapper(self, **params):
                params = func(self, **params)
                params['__method'] = method.lower()
                # If the url is already added, we can call the API
                if '__url' in params.keys():
                    return self._call_api(params)
                # Else we just return the parms
                return params
            return wrapper
        return decorate

    def _call_api(self, params):
        url = params['__url']
        method = params['__method']
        if method == 'get':
            response = self._get(url, **params)
        elif method == 'post':
            response = self._post(url, **params)
        elif method == 'put':
            response = self._put(url, **params)
        elif method == 'patch':
            response = self._patch(url, **params)
        elif method == 'delete':
            response = self._delete(url, **params)
        return response


class Attribute:
    def __init__(self, methods=[], mandatory=[], type=None):
        self.methods = methods
        self.mandatory = mandatory
        self.type = type
