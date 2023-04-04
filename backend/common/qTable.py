from common.log import getLogging
logger = getLogging()
import numpy as np
import json

class QTable:
    def __init__(self, connection, width=3, numStates=2):
        if not connection:
            raise ValueError("Connection must be defined.")

        self.connection = connection
        self.width = width
        self.numStates = numStates
        self.table = 'qtable'

    def setup(self):
        self.connection.execute(
            f'CREATE TABLE IF NOT EXISTS {self.table} ( '
                'qid int PRIMARY KEY, '
                'table_values list<int>'
            ')'
        )

        self.connection.execute(f'TRUNCATE TABLE {self.table}')

        return True

    def getRow(self, qid):
        query = self.connection.query(f'SELECT table_values FROM {self.table} WHERE qid = {qid}')

        if not len(query):
            return [0] * self.width * self.width
        else:
            return query[0][0]

    def getDependentRows(self, tableIds):
        tableIdsString = ','.join(map(str, tableIds))

        query = self.connection.query(f'SELECT qid, table_values FROM {self.table} WHERE qid IN ({tableIdsString})')

        return self._extractRows(query)

    def _extractRows(self, query):
        return [
            list(map(lambda x: x[1], query)),
            list(map(lambda x: x[0], query))
        ]

    def updateRow(self, qid, values):
        logger.debug("updateRow")
        logger.debug(qid)
        logger.debug(values)
        self.connection.execute(f"UPDATE {self.table} set table_values = {values} WHERE qid = {qid}")

        return True


