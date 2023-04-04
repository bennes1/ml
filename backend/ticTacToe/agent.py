from common.log import getLogging
logger = getLogging()
import numpy as np
import json

class TicTacToeAgent:
    def __init__(self, width=None, numStates=None, agentIndex=None, alpha=None, gamma=None):
        # Configuration
        self.width = width
        self.numStates = numStates
        self.agentIndex = agentIndex
        self.alpha = alpha
        self.gamma = gamma

        self.shape = (self.width,self.width)

    def load(self, model=None, dependentRows=None, qid=None):
        if model:
            self.model = np.array(model)
        if dependentRows:
            self.dependentValues = np.array(dependentRows[0])
            self.dependentIds = np.array(dependentRows[1])
        if qid:
            self.qid = qid

    def choseRandomValueInModel(self):
        validIndices = np.flatnonzero(self.model == 0)
        if not len(validIndices):
            raise ValueError("No options available")
        return np.random.choice(validIndices)

    def choseBestInModel(self, returnTableValues=False):
        valid = np.ma.masked_where(self.model != 0, self.model) + 1
        tableValues = self._getTableValues(self.qid, self.dependentValues, self.dependentIds) * valid
        maxValue = np.amax(tableValues)
        chosen = np.random.choice(np.flatnonzero(tableValues == maxValue))

        if returnTableValues:
            return (chosen, tableValues)
        else:
            return chosen

    def getUpdatedModel(self, tableValues, index=None):
        if not index:
            index = self.agentIndex
        tableValues = np.array(tableValues)
        validIndices = np.flatnonzero(self.model == 0)
        if not len(validIndices):
            raise ValueError("No options available")

        reward = np.zeros(self.width * self.width)
        for x in validIndices:
            a = np.copy(self.model)
            a[x] = index
            reward[x] = self._getReward(a)

        maxValues = self._getMaxValues(self.qid, self.dependentValues, self.dependentIds)

        updatedValues = tableValues + self.alpha * (reward + self.gamma * maxValues) - tableValues
        return np.ma.filled(updatedValues, 0)

    def _getReward(self, a):
        a = np.reshape(a, self.shape)

        """ horizonal or vertical """
        for i in range(1, self.numStates):
            y = self._countRowOrCol(a, i, 0)
            if y:
                return y

            x = self._countRowOrCol(a, i, 1)
            if x:
                return x

        """ Diagonals """
        diagonal = self._countDiagonal(a.diagonal())
        if diagonal:
            return diagonal
        diagonal = self._countDiagonal(np.fliplr(a).diagonal())
        if diagonal:
            return diagonal

        """ Draw """
        numZeroes = np.count_nonzero(a == 0)
        if numZeroes == 0:
            return -1

        return 0

    def _countDiagonal(self, a):
        unique, counts = np.unique(a, return_counts=True)
        index = 0
        returnValue = 0
        for x in unique:
            if counts[index] == self.width:
                if x == self.agentIndex:
                    returnValue = 1
                    break
                elif x > 0:
                    returnValue = -1
                    break
            index += 1

        return returnValue



    def _countRowOrCol(self, a, i, axis):
        y = np.count_nonzero(a == i, axis=axis)
        y = np.count_nonzero(y == self.width)
        if y:
            if i == self.agentIndex:
                return 1
            else:
                return -1
        return 0


    def _getTableValues(self, qid, dependentValues, dependentIds):
        if len(dependentValues) == 0:
            return np.zeros(self.width * self.width)

        index = np.where(dependentIds == qid)[0]
        if (len(index) == 0):
            raise ValueError("Qid is not found")
        return dependentValues[index]

    # From Stack Overflow
    def _getIndices(self, x, y):
        index = np.argsort(x)
        sortedX = x[index]
        sortedIndex = np.searchsorted(sortedX, y)
        yindex = np.take(index, sortedIndex, mode="clip")
        mask = x[yindex] != y

        returnArray = np.ma.filled(np.ma.array(yindex + 1, mask=mask), 0)

        return returnArray

    def _getMaxValues(self, qid, dependentValues, dependentIds):
        if len(dependentValues) == 0:
            return np.zeros(self.width * self.width)

        newValuesBuffer = None
        maxValue = []
        lookup = np.arange(self.width * self.width)
        lookup = np.power(self.numStates, lookup)
        lookup += qid

        indices = self._getIndices(dependentIds, lookup)

        maxValue = np.amax(dependentValues, axis=1)
        maxValue = np.concatenate(([0], maxValue))

        return maxValue[indices]
