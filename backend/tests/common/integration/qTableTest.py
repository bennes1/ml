import pytest
import sys
sys.path.append("/app")
import common.qTable
import common.connection

VALID_GRID = ["","X","O","X"]
VALID_VALUES = [1,2,3,4]

def setup():
    conn = common.connection.Connection('test')
    qTable = common.qTable.QTable(conn, places=4, states=["","X","O"])
    return [conn, qTable]

def provideGetRowError():
    data = [
        [["", ""], 'Grid needs to be the same size as the table.'],
        [["P", "", "", "X"], 'CellValue is not in states.']
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
        [["", ""], VALID_VALUES, 'Grid needs to be the same size as the table.'],
        [VALID_GRID, [1, 2], 'Values need to be the same size as the table.'],
        [["P", "", "", "X"], VALID_VALUES, 'CellValue is not in states.']
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
    qTable.setup()
    results = qTable.getRow(VALID_GRID)
    assert results == [0,0,0,0]
    conn.close()

def testNewRowSuccess():
    [conn, qTable] = setup()
    qTable.setup()
    qTable.updateRow(VALID_GRID, VALID_VALUES)
    results = qTable.getRow(VALID_GRID)
    assert results == VALID_VALUES
    conn.close()
