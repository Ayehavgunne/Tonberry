from dataclasses import dataclass

from tonberry import File, create_app, expose, jinja, quick_start, request, session
from tonberry.content_types import ApplicationJson, TextHTML, TextPlain
from tonberry.exceptions import HTTPRedirect


@dataclass
class Request1:
    thing1: int
    thing2: str


@dataclass
class Request2:
    thing1: str
    thing2: str


class ChildOne:
    @expose.get
    async def index(self) -> TextPlain:
        return "Child 1"

    @expose.get
    async def sit(self) -> TextPlain:
        return "Child 1 Sat Down"

    @expose.post
    async def stand_up(self) -> TextPlain:
        return "Child 1 Stood Up"

    @expose.post
    async def stuff_with_json(self, request1: Request1) -> TextPlain:
        return f"Child 1 has {request1.thing1} {request1.thing2}"

    @expose.post
    async def stuff_with_urlencoded(self, request2: Request2) -> TextPlain:
        return f"Child 1 has {request2.thing1} {request2.thing2}"


class ChildsChild:
    @expose.get
    async def index(self) -> TextPlain:
        return "Child Child Index"

    @expose.get
    async def something(self) -> TextPlain:
        url = request.current_route.get_url()
        print(url)
        return "something"

    @expose.get
    async def shout(self, something: str = "stuff") -> TextPlain:
        return f"AHHHHH {something}"


class ChildTwo:
    childschild = ChildsChild()

    def __init__(self, child: int) -> None:
        self.child = child

    @expose.get
    async def index(self) -> TextHTML:
        self.child += 1
        return File("test.html")

    @expose.get
    async def sit(self, name: str) -> TextPlain:
        return f"Child 2 named {name} Sat Down"

    @expose.get("up")
    async def stand_up(self) -> TextPlain:
        return "Child 2 Stood Up"


class Root:
    child_one = ChildOne()
    child_two = ChildTwo(0)

    @expose.get
    async def index(self) -> TextPlain:
        return "Hello, how are you?"

    @expose.get
    async def hey(self) -> TextHTML:
        num = session.get("num", 0) + 1
        print(num)
        session["num"] = num
        return File("test.html")

    @expose.get
    async def what(self, thing, num) -> TextPlain:
        return f"Hello {thing} {num}"

    @expose.post
    async def what(self, thing, num) -> TextPlain:
        return f"Go away {thing} {num}"

    @expose.get
    async def hello(self) -> TextPlain:
        return "GET Tonberry says Hello World"

    @expose.post
    async def hello(self) -> TextPlain:
        return "POST Tonberry says Hello World"

    @expose.get
    async def getjson(self) -> ApplicationJson:
        thing = self.do_a_thing(2)
        return {"hello": "world", "thing": thing}

    @staticmethod
    async def do_a_thing(num: int) -> int:
        return num * 2

    @expose.get
    async def i_redirect(self):
        raise HTTPRedirect("/getjson")

    @expose.get
    async def jinja_stuff(self) -> TextPlain:
        return jinja(file_name="jinja.txt", context={"my_var": "hello"})


app = create_app(Root)


if __name__ == "__main__":
    quick_start(Root, "127.0.0.1", 8000)
