import random
import Checkers

__author__ = 'jspear'


def makeMove(board, weights, whoseTurn):
    moves = Checkers.generatePossibleMoves(board, whoseTurn)
    moveValues = {move: assignValue(move, weights) for move in moves}
    bestMoves = getKeysWithHighestValue(moveValues)
    bestMove = random.choice(bestMoves)
    return bestMove


def getKeysWithHighestValue(dict):
    """Gets all moves from a dictionary with the highest value"""
    bestKeys = []
    highestValue = 0
    for key, value in dict.itervalues():
        if value > highestValue:
            highestValue = value
            bestKeys = [key]
        elif value == highestValue:
            bestKeys.append(key)
    return bestKeys

    # highestValue = max(dict.itervalues())
    # Get all the moves with the highest value
    # bestMoves = [move for move, value in dict.iteritems() if value == highestValue]
    # return bestMoves


def assignValue(board, weights):
    """assigns a value to a given board state"""
    pass


def updateWeights(board, trainingValue, currentWeights, step):
    """updates the weights of our board representation using LMS"""
    calculatedValue = assignValue(board, currentWeights)
    error = trainingValue - calculatedValue
    pieceFrequencies = getFrequencies(board)

    newWeights = []
    for weight, feature in zip(currentWeights, pieceFrequencies):
        weight = weight + step * error * feature
        newWeights.append(weight)

    return newWeights
