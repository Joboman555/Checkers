import Pieces
import Checkers

__author__ = 'jspear'


def generateEmptyBoard():
    oddRow  = "   [ ]   [ ]   [ ]   [ ]\n"
    evenRow = "[ ]   [ ]   [ ]   [ ]   \n"
    emptyBoard = oddRow + evenRow + oddRow + evenRow + oddRow + evenRow + oddRow + evenRow
    return emptyBoard


def toString(board):
    emptyBoard = generateEmptyBoard()
    #for pieceNumber in range(1,)
    for position, piece in board.iteritems():
        charPosition = getCharPosition(position)
        char = getChar(piece)
        emptyBoard = insertChar(emptyBoard, char, charPosition)
    return emptyBoard


def insertChar(boardString, char, charPosition):
    boardAsList = list(boardString)
    boardAsList[charPosition] = char
    return ''.join(boardAsList)


def getChar(piece):
    if piece == Pieces.Black():
        return 'b'
    elif piece == Pieces.Red():
        return 'r'
    elif piece == Pieces.RedKing():
        return 'R'
    elif piece == Pieces.BlackKing():
        return 'B'


def getCharPosition(piecePosition):
    quotient, rem = divmod(piecePosition, 8)
    # Same pattern repeats after second row every 8 pieces and 50 characters
    pieceToCharPositions = {1: 4, 2: 10, 3: 16, 4: 22, 5: 26, 6: 32, 7: 38, 8: 44}
    charPosition = 50 * quotient + pieceToCharPositions[rem]
    return charPosition
