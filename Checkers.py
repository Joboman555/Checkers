import Engine

__author__ = 'jspear'


def generatePossibleMoves(board, turn):
    """All possible moves available that turn"""
    # Since black starts at turn 1, all even turns are red
    if isRedsTurn(turn):
        occupiedTiles = [position for position, piece in board.iteritems() if piece.isRed()]
    else:
        occupiedTiles = [position for position, piece in board.iteritems() if piece.isBlack()]

    jumps = join([possibleJumps(position, board) for position in occupiedTiles])
    moves = [] if jumps else join([possibleMoves(position, board) for position in occupiedTiles])

    return jumps + moves


def isRedsTurn(turn): return turn % 2 == 0


def join(listOfLists): return [j for i in listOfLists for j in i]


def possibleMoves(position, board):
    """All possible moves for a single piece"""
    unoccupiedMoves = []
    if (position in board):
        piece = board[position]
        validMoves = piece.validMoves(position)
        for nextPosition in validMoves:
            unoccupiedMoves.append(evaluateMove(position, nextPosition, board))
    return join(unoccupiedMoves)


def evaluateMove(position, nextPosition, board):
    """returns the board state possible for a given move"""
    # Evaluates to true if another piece with that location is on the board
    newBoard = []
    if not squareIsOccupied(nextPosition, board):
        newBoard.append(move(position, nextPosition, board))
    return newBoard


def possibleJumps(position, board):
    jumps = []
    piece = board[position]
    validMoves = piece.validMoves(position)
    canJumpOver = lambda move: squareIsOccupied(move, board) and not areSameColor(piece, board[move])
    occupiedEnemySquares = list(filter(canJumpOver, validMoves))
    for middlePosition in occupiedEnemySquares:
        jumpPosition = piece.getJumpPosition(position, middlePosition)
        if not (Engine.isOnEdge(middlePosition) or squareIsOccupied(jumpPosition, board)):
            newBoard = jumpOver(position, middlePosition, board)
            nextJumps = possibleJumps(jumpPosition, newBoard)
            # If there are no next jumps
            if not nextJumps:
                # Add this jump to the list
                jumps.append(newBoard)
            else:
                # Add  the next jumps to the list
                jumps += nextJumps

    return jumps


def move(position, nextPosition, board):
    """moves a piece and replaces it with a king if it can be promoted"""
    piece = board[position]
    newBoard = removePiece(board, position)
    newPiece = piece.promote() if piece.canBePromoted(nextPosition) else piece
    newBoard = addPiece(newBoard, nextPosition, newPiece)
    return newBoard


def jumpOver(position, middlePosition, board):
    jumpingPiece = board[position]
    finalPosition = jumpingPiece.getJumpPosition(position, middlePosition)
    # Move jumping piece
    newBoard = move(position, finalPosition, board)
    # Remove jumped piece
    newBoard = removePiece(newBoard, middlePosition)
    return newBoard


def removePiece(board, position):
    newBoard = dict(board)
    del newBoard[position]
    return newBoard


def addPiece(board, position, piece):
    newBoard = dict(board)
    newBoard[position] = piece
    return newBoard


def areSameColor(piece1, piece2): return piece1.isRed() == piece2.isRed()


def squareIsOccupied(position, board): return position in board
