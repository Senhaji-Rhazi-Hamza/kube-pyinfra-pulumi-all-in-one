import os

from sanic import Sanic
from sanic.response import text, json

from lib.hello import hello

app = Sanic("MyHelloWorldApp")

@app.get("/")
async def hello_world(request):
    return json({"message":hello()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)