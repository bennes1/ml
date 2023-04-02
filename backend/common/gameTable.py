from common.log import getLogging
logger = getLogging()

class GameTable:
    def __init__(self, connection):
        if not connection:
            raise ValueError("Connection must be defined.")

        self.connection = connection
        self.table = 'steps'

    def _getShortHash(self):
        import shortuuid
        return shortuuid.ShortUUID().random(length=10)

    def createNewGame(self, defaultModel):
        gameid = self._getShortHash()
        self.connection.execute(
            f"INSERT INTO {self.table} (gameid, created_time, model, steps) "
            f"VALUES ('{gameid}', toUnixTimestamp(now()), {defaultModel}, [1])"
        )
        return gameid

    def addStep(self, gameId, qTableId):
        self.connection.execute(
            f"UPDATE TABLE {self.table} SET steps = steps + ['{qTableId}'] "
            f"WHERE gameid = '{gameId}'"
        )

        return True

    def getSteps(self, gameId):
        query = self.connection.query(f'SELECT steps FROM {self.table} WHERE gameid = {gameId}')

        if not len(query):
            return []
        else:
            return query[0][0]

    def deleteSteps(self, gameId):
        self.connection.execute(f"DELETE FROM {self.table} WHERE gameid = '{gameId}'")

        return True
