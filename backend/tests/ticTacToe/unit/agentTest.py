import pytest
import sys
sys.path.append("/app")
from ticTacToe.agent import TicTacToeAgent
from common.log import getLogging
logger = getLogging()
import numpy as np

def testRandom():
    model = [[3,0,1],[6,0,0],[6,6,0]]
    agent = TicTacToeAgent()
    result = agent.exploreModel(model)
    testList = [
        (0,1),
        (1,1),
        (1,2),
        (2,2)
    ]
    assert result in testList

def testExploit():
    model = [3,0,1,6,0,4,6,6,0]
    agent = TicTacToeAgent()
    result = agent.exploitModel(model, 2, [
                                [
                                    [.4,.6,.7,85,7,80,6,6,0.7],
                                    [.4,.6,.7,6,7,80,6,6,0.7],
                                    [.4,.655,.73,6,7,86,6,6,0.7],
                                ],
                                [2,83,11]
                            ])

    assert True

def testGetReward():
    model = [3,3,4,5,3,2,3,4,2]
    agent = TicTacToeAgent()
    result = agent._getReward(np.array(model),7)

    assert result == -1
