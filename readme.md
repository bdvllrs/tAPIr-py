# tAPIr

tAPIr is a wrapper for the requests python package the makes API requests easier.

## Basic idea

tAPIr uses models that represents an API endpoit. You have to specify each model, the arguments you want to pass to the API, the url and the method.

## Configuration

You first have to import `API_CONFIG` from the `API_config.py`
file then create a configuration variable:

``` python
CONFIG = API_CONFIG('http://localhost/api')
```

where `htp://locahost/api` is your API enter point.
Then instanciate your model. The constructor takes the API configuration.

### Authentification

You can use a basic auth to connect to the API: 

 ``` python 
CONFIG.basic_auth('username', 'password')
```

### Add global arguments

To add arguments that will be added to the request you can call the
`API_CONFIG.set_global_arg(self, key, value)` method.
To get a global argument, use the `API_CONFIG.get_global_arg(self, key)` method.

## Creating a model

The model is a class which extends from the Model class.

### Defining the arguments

You first have to set the args attribute which contains all the possible attributes you want to send to the API.

`args` is a dict object and each key corresponds to the name of an attribute.
Each attributes is a `Attribute` object.

``` python
Attribute(methods=[], mandatory=[], type=None)
```

- the `method` argument corresponds to the methods the attribute can be used for ('get', 'post', 'put', 'patch', 'delete' available).
- the `mandatory` argument precise in which method the attribute is required.
- the type argument is the type of the attribute.

For instance, if you want an `id` argument available for the get and post methods, mandatory for the post and must be an integer: 
``` python

class Example(Model):
    args = {
        'id': Attribute(methods=['get', 'post'], mandarory=['post'], type=int) 
    }
```

If the type of your attributes is different between several methods, `type` can also be a dict object : 

``` python

class Example(Model):
    args = {
        'id': Attribute(methods=['get', 'post'], mandarory=['post'], type={
            'get': str,
            'post': int
        }) 
    }

```

### Methods

You can then precise the methods of you model that will be used to call the API.

We will for instance create a `get` method that will fetch all the examples in the API. In yout model class, add

``` python
    def get(self, **params):
        return params
``` 

this method needs to get all the attribute you want to pass to the API as input and must then return those parameters.
To specify that this method will call the API with a `GET` method, we will add the `Model.method` decorator and we will add the `Model.url` decorator to specify the endpoint:

``` python
    @Model.method('GET')
    @Model.url('/examples')
    def get(self, **params):
        return params
```

### Passing arguments to the url

There is some case when the url depends on some arguments. 
The `Model.url` decorator can contain some `{param}` in its content. 
You will then have to pass a `_param` to your get method:

``` python
    @Model.method('GET')
    @Model.url('/examples/{id}')
    def get(self, **params):
        return params
```

If you then call `Example.get(_id=5)` it will call the url ``/examples/5`.

### Calling the API

You can now instanciate your model to use it (don't forget to pass the CONFIG parameter):

``` python
example = Example(CONFIG)
results = example.get(id=5)
```

will call `http://localhost/api/examples?id=5`.
