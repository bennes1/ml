import json
from tornado.web import RequestHandler
from log import getLogging
logger = getLogging()

class TicTacToeView(RequestHandler):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET", "POST"]

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self):
        try:
            action = self.get_argument('action', 'view')
            database = 'test'
            match action:
                case 'reset_db':
                    from TicTacToe.resetDatabase import resetDatabase
                    data = resetDatabase(database)
                case 'view':
                    data = self.showView()
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
