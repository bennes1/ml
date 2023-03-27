import asyncio
import tornado.web
import json
from ticTacToe.view import TicTacToeView

from common.log import setupLogging
setupLogging()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        file = open("/app/common/helloWorld.html", "r")
        self.write(file.read())

def makeApp():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ticTacToe", TicTacToeView)
    ],
        debug=True
    )

async def main():
    app = makeApp()
    app.listen(80)
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()

if __name__ == "__main__":
    asyncio.run(main())
