import Engine

__author__ = 'jspear'


class EqualityMixin(object):

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class Black(EqualityMixin):

    def validMoves(self, position):
        """returns positions of valid moves for a regular black gamepiece on an empty board"""

        moves = []
        if Engine.isOnBottomRow(position):
            moves = []
        elif Engine.isOnRightEdge(position) or Engine.isOnLeftEdge(position):
            # Edges only have one valid move
            moves = [position + 4]
        elif Engine.isOnOddRow(position):
            # diagonals below pieces on odd rows are always 4 and 5 pieces after
            moves = [position + 4, position + 5]
        elif Engine.isOnEvenRow(position):
            # diagonals below pieces on even rows are always 3 and 4 piececs after
            moves = [position + 3, position + 4]
        return moves

    def getJumpPosition(self, position, middlePosition):
        # On odd rows, the square on the right is not at position + 4
        # On even rows, the square on the right is at position + 4
        isSkippingRight = Engine.isOnOddRow(position) != (middlePosition - position == 4)
        distanceToNextPosition = 9 if isSkippingRight else 7
        finalPosition = position + distanceToNextPosition
        return finalPosition

    def isBlack(self): return True

    def isRed(self): return not self.isBlack()

    def canBePromoted(self, position): return Engine.isOnBottomRow(position)
    """Black pieces can be promoted when they're on the bottom row"""

    def promote(self): return BlackKing()


class Red(EqualityMixin):

    def validMoves(self, position):
        """returns positions of valid moves for a regular red gamepiece on an empty board"""

        moves = []
        if Engine.isOnTopRow(position):
            moves = []
        elif Engine.isOnRightEdge(position) or Engine.isOnLeftEdge(position):
            # Edges only have one valid move
            moves = [position - 4]
        elif Engine.isOnOddRow(position):
            # diagonals above pieces on odd rows are always 4 and 5 pieces after
            moves = [position - 4, position - 3]
        elif Engine.isOnEvenRow(position):
            # diagonals below pieces on even rows are always 3 and 4 piececs after
            moves = [position - 5, position - 4]
        return moves

    def getJumpPosition(self, position, middlePosition):
        # On odd rows, the square on the right is not at position - 4
        # On even rows, the square on the right is at position - 4
        isSkippingRight = Engine.isOnOddRow(position) != (position - middlePosition == 4)
        distanceToNextPosition = 7 if isSkippingRight else 9
        finalPosition = position - distanceToNextPosition
        return finalPosition

    def isBlack(self): return False

    def isRed(self): return not self.isBlack()

    def canBePromoted(self, position): return Engine.isOnTopRow(position)
    """Red Pieces can be promoted when they're on the top row"""

    def promote(self): return RedKing()


class King(EqualityMixin):

    def validMoves(self, position):
        """returns positions of valid moves for a king on an empty board"""
        black = Black()
        red = Red()
        # A king can move like a red or a black piece
        moves = black.validMoves(position) + red.validMoves(position)
        return moves

    def getJumpPosition(self, position, middlePosition):
        """returns the position of the piece after a jump"""
        isJumpingDown = middlePosition > position
        # Jumps either like a red or a black piece
        if isJumpingDown:
            finalPosition = Black().getJumpPosition(position, middlePosition)
        else:
            finalPosition = Red().getJumpPosition(position, middlePosition)
        return finalPosition

    def canBePromoted(self, position): return False
    """Kings cannot be promoted"""

    def promote(self): return self

class BlackKing(King):

    def isBlack(self): return True

    def isRed(self): return not self.isBlack()


class RedKing(King):

    def isBlack(self): return False

    def isRed(self): return not self.isBlack()
