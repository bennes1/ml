import json
from common.log import getLogging
logger = getLogging()

class GameTable:
    def __init__(self, connection):
        if not connection:
            raise ValueError("Connection must be defined.")

        self.connection = connection
        self.table = 'game'

    def createNewGame(self, gameId, defaultModel):
        defaultModel = json.dumps(defaultModel)
        self.connection.execute(
            f"INSERT INTO {self.table} (gameid, model) "
            f"VALUES ('{gameId}', {defaultModel})"
        )
        return gameId

    def getModel(self, gameId):
        query = self.connection.query(f"SELECT model FROM {self.table} WHERE gameid = '{gameId}'")

        if not len(query):
            return []
        else:
            return query[0][0]

    def updateModel(self, gameId, model):
        self.connection.execute(
            f"UPDATE {self.table} "
            f"SET model = {model} WHERE gameid = '{gameId}'"
        )
