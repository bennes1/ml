import asyncio
import tornado.web
import json
from TicTacToe.view import TicTacToeView

from log import setupLogging
setupLogging()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        from app.test import sample
        self.write(json.dumps(sample()))

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
