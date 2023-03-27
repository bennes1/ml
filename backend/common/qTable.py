from common.log import getLogging
logger = getLogging()

class QTable:
    def __init__(self, connection, places=9, states=None):
        if not connection:
            raise ValueError("Connection must be defined.")

        self.connection = connection
        self.places = places
        self.states = states
        self.table = 'q_table'

    def setup(self):
        self.connection.execute(
            f'CREATE TABLE IF NOT EXISTS {self.table} ( '
                'qid int PRIMARY KEY, '
                'table_values list<int>'
            ')'
        )

        self.connection.execute(f'TRUNCATE TABLE {self.table}')

        return True

    def _validateLength(self, grid=[], start='Grid needs'):
        if not grid or len(grid) != self.places:
            raise ValueError(f"{start} to be the same size as the table.")

    def _getTableId(self, grid=[]):
        if not self.states:
            states = 2
        else:
            states = len(self.states)

        tableId = 1
        i = 0
        for x in grid:
            part = self._getIdPart(x)
            if part > 0:
                tableId += part + states * i
            i += 1
        return tableId

    def _getIdPart(self, cellValue):
        if not self.states:
            if isspace(cellValue):
                return 0
            else:
                return 1
        else:
            i = 0
            for x in self.states:
                if x == cellValue:
                    return i
                i += 1
            raise ValueError("CellValue is not in states.")


    def getRow(self, grid=[]):
        self._validateLength(grid)
        tableId = self._getTableId(grid)

        query = self.connection.query(f'SELECT table_values FROM {self.table} WHERE qid = {tableId}')

        if not len(query):
            return [0] * self.places
        else:
            return query[0][0]

    def updateRow(self, grid=[], values=[]):
        self._validateLength(grid)
        self._validateLength(values, start='Values need')

        tableId = self._getTableId(grid)

        self.connection.execute(f'UPDATE {self.table} set table_values = {values} WHERE qid = {tableId}')

        return True


