from sanic import Sanic
from sanic.response import text



app = Sanic("MyHelloWorldApp")

@app.get("/")
async def hello_world(request):
    return text("Hello world from Sanic")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)