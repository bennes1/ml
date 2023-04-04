import json
from tornado.web import RequestHandler
from ticTacToe.game import TicTacToeGame
from tornado import concurrent

executor = concurrent.futures.ThreadPoolExecutor(8)

# Debug
from common.log import getLogging
logger = getLogging()

class TicTacToeView(RequestHandler):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET", "POST"]

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self):
        game = None

        def runUpdate(chosen, index):
            game.open()
            game.runUpdate(chosen, index)
            game.close()

        try:
            action = self.get_argument('action', 'view')
            gameId = self.get_argument('gameId', '')
            if action == 'view':
                data = self.showView()
            else:
                game = TicTacToeGame(gameId)

                match action:
                    case 'createGame':
                        data = game.startGame()
                    case 'nonAgentTurn':
                        pos = self.get_argument('pos', '')
                        value = self.get_argument('value', 'O')
                        if gameId == '':
                            raise ValueError("GameId is required")
                        if pos == '':
                            raise ValueError("Position is required")
                        data = game.nonAgentTurn(int(pos), value)

                        executor.submit(runUpdate, data, 2)

                    case 'agentTurn':
                        if gameId == '':
                            raise ValueError("GameId is required")
                        data = game.agentTurn()

                        executor.submit(runUpdate, data, 1)

                    case _:
                        raise ValueError("Action doesn't exist")

            returnValue = {
                'successful': True,
                'data': data
            }
        except Exception as e:
            returnValue = {
                'successful': False,
                'error': 'An error occurred'
            }
            logger.exception ('Failed to get request data')
        finally:
            if game:
                game.close()

        self.write(json.dumps(returnValue))

    def showView(self):
        """List of routes for this API."""
        routes = {
            'info': 'GET /api/v1',
            'register': 'POST /api/v1/accounts',
            'single profile detail': 'GET /api/v1/accounts/<username>',
            'edit profile': 'PUT /api/v1/accounts/<username>',
            'delete profile': 'DELETE /api/v1/accounts/<username>',
            'login': 'POST /api/v1/accounts/login',
            'logout': 'GET /api/v1/accounts/logout',
            "user's tasks": 'GET /api/v1/accounts/<username>/tasks',
            "create task": 'POST /api/v1/accounts/<username>/tasks',
            "task detail": 'GET /api/v1/accounts/<username>/tasks/<id>',
            "task update": 'PUT /api/v1/accounts/<username>/tasks/<id>',
            "delete task": 'DELETE /api/v1/accounts/<username>/tasks/<id>'
        }
        return routes
