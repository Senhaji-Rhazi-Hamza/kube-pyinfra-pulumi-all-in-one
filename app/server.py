from sanic import Sanic
from sanic.response import text

from lib.hello import hello

app = Sanic("MyHelloWorldApp")

@app.get("/")
async def hello_world(request):
    return text(hello())
