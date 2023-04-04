import pytest
import sys
sys.path.append("/app")
import common.qTable
import common.connection
import numpy as np
from common.log import getLogging
logger = getLogging()

VALID_GRID = [[0,1],[2,1]]
EMPTY_GRID = [[2,2],[2,2]]

def setup():
    conn = common.connection.Connection('test')
    qTable = common.qTable.QTable(conn, width=2, numStates=3)
    return [conn, qTable]

def provideGetRowError():
    data = [
        [[0, 0], 'Grid needs to be the same size as the table.'],
        [[[7, 0], [0, 1]], 'CellValue is not in states.']
    ]
    for row in data:
        yield row

@pytest.mark.parametrize("testInput", provideGetRowError())
def testGetRowError(testInput):
    [conn, qTable] = setup()
    model = testInput[0]
    expectedError = testInput[1]
    with pytest.raises(ValueError) as excinfo:
        qTable.getRow(model)
    assert str(excinfo.value) == expectedError
    conn.close()

def provideUpdateRowError():
    data = [
        [[0,0], VALID_GRID, 'Grid needs to be the same size as the table.'],
        [VALID_GRID, [1, 2], 'Values need to be the same size as the table.'],
        [[[7,0],[0,2]], VALID_GRID, 'CellValue is not in states.']
    ]
    for row in data:
        yield row

@pytest.mark.parametrize("testInput", provideUpdateRowError())
def testUpdateRowError(testInput):
    [conn, qTable] = setup()
    model = testInput[0]
    values = testInput[1]
    expectedError = testInput[2]
    with pytest.raises(ValueError) as excinfo:
        qTable.updateRow(model, values)
    assert str(excinfo.value) == expectedError
    conn.close()

def testGetRowEmptySet():
    [conn, qTable] = setup()
    results = qTable.getRow(EMPTY_GRID)
    assert results == [[0,0],[0,0]]
    conn.close()

def testNewRowSuccess():
    [conn, qTable] = setup()
    qTable.updateRow(VALID_GRID, VALID_GRID)
    results = qTable.getRow(VALID_GRID)
    assert results == VALID_GRID
    conn.close()

def testGetDependentRows():
    [conn, qTable] = setup()
    qTable.updateRow([[2,1],[0,0]], [[1,2],[4,5]])
    qTable.updateRow([[2,1],[0,1]], [[2,2],[3,3]])
    qTable.updateRow([[0,1],[0,1]], [[1,2],[3,3]])

    results = qTable.getDependentRows([[2,1],[0,0]])

    logger.debug(results)

    assert len(list(results[0])) == 2
    assert len(list(results[1])) == 2
