from common.log import getLogging
logger = getLogging()
import json
import numpy as np

class TicTacToeAgent:
    def __init__(self):
        from common.connection import Connection
        self.conn = Connection('tictactoe')

        # Configuration
        self.places = 9
        self.states = ["","X","O"]
        self.me = "X"

        from common.qTable import QTable
        from common.gameTable import GameTable

        self.qTable = QTable(self.conn, places=self.places, states=self.states)
        self.gameTable = GameTable(self.conn)

    def _getDefaultModel(self):
        model = np.array(self.states[0])
        model = np.repeat(model, self.places)
        model = np.array2string(model, separator=",")
        return model

    def startGame(self):
        defaultModel = self._getDefaultModel()
        gameId = self.gameTable.createNewGame(defaultModel)
        return gameId
