# Cactuar

An ASGI compliant web microframework that takes a class based approach to routing.
Heavily influenced by CherryPy but made compatible with asyncio.

### Installing

```bash
pip install cactuar
```

## Getting Started

### 2 Minute App Example

```python
from cactuar import quick_start, expose

class Root:
    @expose.get
    async def index(self):
        return "Hello, world!"

quick_start(Root)

# Go to http://localhost:8080
```

### Features Example

```python
from dataclasses import dataclass

from cactuar import quick_start, expose
from cactuar.content_types import TextPlain, TextHTML, ApplicationJson


@dataclass
class Request:
    arg1: int
    arg2: str


@dataclass
class Response:
    param1: str
    param2: float


class SubPage:
    @expose.post
    async def index(self, request: Request) -> Response:
        """
        With type hints indicating a dataclass object, the body of the request will
        automatically be deserialized into that object, even if it contains nested
        dataclasses and types will be checked thanks to the library dacite. Returning
        a dataclass will result in it being serialized into a JSON string and the
        content-type header will be set to application/json.

        URL: http://127.0.0.1:8888/subpage
        POST body: {"arg1": 3, "arg2": "something"}
        Response body: {"param1": "SOMETHING", "param2": 4.5}
        """
        return Response(request.arg2.upper(), request.arg1 * 1.5)

    @expose.get
    async def hello(self, name: str) -> TextPlain:
        """
        Arguments to methods can come from the leftover parts of the URI after the
        route has found a match, querystrings, form-url-encoded data or json strings.

        URL: http://127.0.0.1:8888/subpage/hello/{name}
        """
        return f"Hi {name}"


class Root:
    subpage = SubPage()

    @expose.get
    async def index(self) -> TextPlain:
        """
        The index method behaves similarly to an index.html file in most web servers.

        URL: http://127.0.0.1:8888
        """
        return "Hello, world!"

    @expose.get('somepage')
    async def some_page(self) -> TextHTML:
        """
        Returning a file like object result in the file contents being read and put
        into the response body.

        The expose decorator methods can take an optional argument for the name you
        would like to use for the route if you don't want it to be the name of the
        method.

        To indicate what the content-type header you want to set then use a type hints
        for the return value from cactuar.content_types. This feature may or may not
        stay as part of the project. It will not overwrite any content type set manually
        inside the method.

        URL: http://127.0.0.1:8888/somepage
        """
        return open('some_page.html')

    @expose.post
    async def do_a_thing(self, data1: int, data2: str) -> ApplicationJson:
        """
        Even without a dataclass the individule top level keys in JSON object will be
        passed as arguments. It is possible to return strings, UTF-8 encoded bytes,
        integers, file like objects, dicts or lists (as long as they are JSON
        serializable) and dataclasses.

        URL: http://127.0.0.1:8888/do_a_thing
        POST body: {"data1": 2, "data2": "things to do"}
        """
        complete, success, result = await do_that_thing(data1, data2)
        return {"completed": complete, "outcome": success, "body": result}


quick_start(Root, host="127.0.0.1", port=8888)
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and 
the process for submitting pull requests.

## Versioning

[SemVer](http://semver.org/) is used for versioning. For the versions available, see the 
[tags on this repository](https://github.com/Ayehavgunne/Cactuar/tags). 

## Author

* **Anthony Post** - [Ayehavgunne](https://github.com/Ayehavgunne)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) 
file for details

## Acknowledgments

* CherryPy
* Quart
* Starlette
* uvicorn

## TODO
- JWT integration
- Authentication
- URL generation
- Configuration
- Static Files
- Indicate Content-Type of response from method return type hint (on the fence about 
  this, could be a fun experiment)
