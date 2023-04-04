from common.connection import Connection
from common.qTable import QTable
from common.gameTable import GameTable
from ticTacToe.agent import TicTacToeAgent
import shortuuid

# Debug
from common.log import getLogging
logger = getLogging()
import numpy as np

class TicTacToeGame:
    def __init__(self, gameId=None):

        # Configuration
        self.width = 3
        self.states = ["","X","O"]
        self.agentIndex = 1
        self.alpha = .2 #Alpha
        self.gamma = .8 #Gamma
        self.epsilon = .2 #Epsilon

        self.numStates = len(self.states)

        self.conn = Connection('tictactoe')
        self.gameId = gameId
        self.qTable = QTable(self.conn, width=self.width, numStates=self.numStates)
        self.gameTable = GameTable(self.conn)
        self.agent = TicTacToeAgent(self.width, self.numStates, self.agentIndex, self.alpha, self.gamma)

    def _getShortHash(self):
        return shortuuid.ShortUUID().random(length=10)

    def _getDefaultModel(self):
        return [0] * self.width * self.width

    def _getQid(self, model):
        qid = 1
        i = 0
        for value in model:
            if value >= self.numStates:
                raise ValueError("CellValue is not in states.")
            elif value > 0:
                qid += value * pow(self.numStates,i)
            i += 1
        return qid

    def _getDependentRows(self, qid):
        tableIds = [qid]

        for i in range(self.width * self.width):
            tableIds.append(tableIds[0] + pow(self.numStates, i))

        return self.qTable.getDependentRows(tableIds)

    def startGame(self):
        defaultModel = self._getDefaultModel()
        self.gameId = self._getShortHash()
        self.gameTable.createNewGame(self.gameId, defaultModel)
        return self.gameId

    def nonAgentTurn(self, pos, value="O"):
        model = self.gameTable.getModel(self.gameId)
        if pos >= self.width * self.width:
            raise ValueError("Position is out of bounds")
        if model[pos] != 0:
            raise ValueError("Index is already filled in")
        model[pos] = self.states.index(value)

        return True

    def close(self):
        self.conn.close()

    def open(self):
        self.conn.open()

    def agentTurn(self):
        model = self.gameTable.getModel(self.gameId)
        qid = self._getQid(model)
        dependentRows = self._getDependentRows(qid)
        self.agent.load(
            model=model,
            dependentRows=dependentRows,
            qid=qid
        )

        if np.random.random_sample() < self.epsilon:
            chosen = self.agent.choseRandomValueInModel()
        else:
            chosen = self.agent.choseBestInModel()

        return int(chosen)

    def runUpdate(self, chosen, index):
        logger.debug("runUpdate")
        logger.debug(chosen)
        logger.debug(index)
        model = self.gameTable.getModel(self.gameId)
        qid = self._getQid(model)
        tableValues = self.qTable.getRow(qid)

        updatedValues = self.agent.getUpdatedModel(tableValues, index)
        self.qTable.updateRow(qid, updatedValues.tolist())

        logger.debug("qTable should be updated")

        model[chosen] = index
        self.gameTable.updateModel(self.gameId, model)

        logger.debug("gameTable should be updated")
