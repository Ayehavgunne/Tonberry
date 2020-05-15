# Tonberry <img src="https://raw.githubusercontent.com/Ayehavgunne/Tonberry/master/Tonberry.png" width="100" title="Tonberry">

An ASGI compliant web microframework that takes a class based approach to
routing. Influenced by [CherryPy](https://cherrypy.org/) but made compatible
with asyncio. A companion ASGI server named **Qactuar** was spawned from this
project which is currently in the works.

## Installing

```bash
$ pip install tonberry
```

## Getting Started

### 2 Minute App Example

```python
from tonberry import quick_start, expose

class Root:
    @expose.get
    async def index(self):
        return "Hello, world!"

quick_start(Root)

# Go to http://localhost:8080
```

### Features Example

```python
import asyncio
from dataclasses import dataclass

import uvicorn

from tonberry import create_app, expose, File, websocket, jinja
from tonberry.content_types import TextPlain, TextHTML, ApplicationJson


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
        With type hints indicating a dataclass object, the body of the request
        will automatically be deserialized into that object, even if it
        contains nested dataclasses and types will be checked thanks to the
        library dacite. Returning a dataclass will result in it being serialized
        into a JSON string and the content-type header will be set to
        application/json.

        URL: http://127.0.0.1:8888/subpage
        POST body: {"arg1": 3, "arg2": "something"}
        Response body: {"param1": "SOMETHING", "param2": 4.5}
        """
        return Response(request.arg2.upper(), request.arg1 * 1.5)

    @expose.get
    async def hello(self, name: str) -> TextPlain:
        """
        Arguments to methods can come from the leftover parts of the URI after
        the route has found a match, querystrings, form-url-encoded data or json
        strings.

        URL: http://127.0.0.1:8888/subpage/hello/{name}
        """
        return f"Hi {name}"


class Root:
    subpage = SubPage()

    @expose.get
    async def index(self) -> TextPlain:
        """
        The index method behaves similarly to an index.html file in most web
        servers.

        URL: http://127.0.0.1:8888
        """
        return "Hello, world!"

    @expose.get('somepage')
    async def some_page(self) -> TextHTML:
        """
        Returning a file like object result in the file contents being read and
        put into the response body.

        The expose decorator methods can take an optional argument for the name
        you would like to use for the route if you don't want it to be the name
        of the method.

        To indicate what the content-type header you want to set then use a type
        hints for the return value from tonberry.content_types. This feature may
        or may not stay as part of the project. It will not overwrite any
        content type set manually inside the method.

        URL: http://127.0.0.1:8888/somepage
        """
        return File('some_page.html')

    @expose.post
    async def do_a_thing(self, data1: int, data2: str) -> ApplicationJson:
        """
        Even without a dataclass the individule top level keys in JSON object
        will be passed as arguments. It is possible to return strings, UTF-8
        encoded bytes, integers, file like objects, dicts or lists (as long as
        they are JSON serializable) and dataclasses.

        URL: http://127.0.0.1:8888/do_a_thing
        POST body: {"data1": 2, "data2": "things to do"}
        """
        complete, success, result = await do_that_thing(data1, data2)
        return {"completed": complete, "outcome": success, "body": result}

    @expose.get
    async def use_jinja(self) -> TextPlain:
        """
        In the config a template path can be configured to point to where all
        your Jinja2 template files are located. To use a template just call
        the `jinja` function with a file name and a context dict with the
        desired replacement values.
        
        URL: http://127.0.0.1:8888/use_jinja
        Response Body: I say hello!
        """
        return jinja(file_name="jinja.txt", context={"my_var": "hello"})

    @expose.websocket
    async def ws(self):
        """
        Basic example of using a websocket. Sending and receiving are done
        through the websocket object.
        
        URL: ws://127.0.0.1:8888/ws
        """
        data = await websocket.receive_text()
        await websocket.send_text(f"echo {data}")
        count = 0
        while websocket.client_is_connected:
            count += 1
            await websocket.send_text(f"Hello {count}")
            await asyncio.sleep(3)


if __name__ == "__main__":
    app = create_app(root=Root)
    app.add_static_route(path_root="./static_files", route="static")
    # Using uvicorn here but any ASGI server will work just as well
    uvicorn.run(app, host="127.0.0.1", port=8888)
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of
conduct, and the process for submitting pull requests.

## Versioning

[SemVer](http://semver.org/) is used for versioning. For the versions available,
see the [tags on this repository](https://github.com/Ayehavgunne/Tonberry/tags).

## Authors

* **Anthony Post** - [Ayehavgunne](https://github.com/Ayehavgunne)

## License

This project is licensed under the MIT License - see the
[LICENSE.txt](LICENSE.txt) file for details

## Acknowledgments

* CherryPy
* Quart
* Starlette
* uvicorn

## TODO
- JWT integration
- Authentication
- URL generation
- Tests
- Documentation
