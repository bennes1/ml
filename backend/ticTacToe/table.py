from common.log import getLogging
logger = getLogging()
from common.qTable import QTable

class TicTacToeTable(QTable):
    def __init__(self):
        from common.qTable import QTable
        from common.connection import Connection
        super().__init__(Connection('tictactoe'), states=["","X","O"])
