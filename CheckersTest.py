import unittest
import Checkers
import Engine
import Pieces
import ConsoleGame
from ddt import ddt, data, unpack

__author__ = 'jspear'

allSquares = list(range(1, 33))
bottomRow = list(range(29, 33))
topRow = list(range(1, 5))
oddRows = topRow + list(range(9, 13)) + list(range(17, 21))
evenRows = list(range(5, 9)) + list(range(13, 17)) + list(range(21, 25))


@ddt
class TestBlack(unittest.TestCase):

    black = Pieces.Black()

    @data(4, 12, 20, 28, 5, 13, 21)
    def test_validMoves_returnsXplus4_forSideSquares(self, value):
        self.assertEqual(self.black.validMoves(value), [value + 4])

    @data(*bottomRow)
    def test_validMoves_returnsEmptyList_forBottomRows(self, value):
        self.assertEqual(self.black.validMoves(value), [])

    oddNonSideRows = list(set(oddRows) - set([4, 12, 20, 28]))

    @data(*oddNonSideRows)
    def test_validMoves_returnsXplus4andXplus5_forOddRows(self, value):
        self.assertEqual(self.black.validMoves(value), [value + 4, value + 5])

    evenNonSideRows = list(set(evenRows) - set([5, 13, 21]))

    @data(*evenNonSideRows)
    def test_validMoves_returnsXplus3andXplus4_forEvenRows(self, value):
        self.assertEqual(self.black.validMoves(value), [value + 3, value + 4])

    @data(*bottomRow)
    def test_canBePromoted_returnsTrue_forPositionOnBottomRow(self, value):
        self.assertEqual(self.black.canBePromoted(value), True)

    nonBottomRow = list(set(allSquares) - set(bottomRow))

    @data(*nonBottomRow)
    def test_canBePromoted_returnsFalse_forPositionsNotOnBottomRow(self, value):
        self.assertEqual(self.black.canBePromoted(value), False)


@ddt
class TestRed(unittest.TestCase):

    red = Pieces.Red()

    @data(*topRow)
    def test_canBePromoted_returnsTrue_forPositionOnTopRow(self, value):
        self.assertEqual(self.red.canBePromoted(value), True)

    nonTopRow = list(set(allSquares) - set(topRow))

    @data(*nonTopRow)
    def test_canBePromoted_returnsFalse_forPositionsNotOnTopRow(self, value):
        self.assertEqual(self.red.canBePromoted(value), False)

    def test_generatePossibleMoves_rightMovesFor1BlackPieceOnFirstTurn(self):
        black = Pieces.Black()
        board = {1: black}
        self.assertEqual(Checkers.generatePossibleMoves(board, 1), [{5: black}, {6: black}])

    def test_generatePossibleMoves_rightMovesFor1BlackPieceOnSecondTurn(self):
        black = Pieces.Black()
        board = {1: black}
        self.assertEqual(Checkers.generatePossibleMoves(board, 2), [])

    def test_generatePossibleMoves_2blackpiecesOnFirstTurn(self):
        black = Pieces.Black()
        board = {1: black, 2: black}
        possibleBoard1 = {5: black, 2: black}
        possibleBoard2 = {6: black, 2: black}
        possibleBoard3 = {1: black, 6: black}
        possibleBoard4 = {1: black, 7: black}
        self.assertEqual(Checkers.generatePossibleMoves(board, 1), [possibleBoard1, possibleBoard2, possibleBoard3, possibleBoard4])

    def test_generatePossibleMoves_rightMovesFor1BlackPieceAnd1RedPieceOnFirstTurn(self):
        black = Pieces.Black()
        board = {1: black, 29: self.red}
        self.assertEqual(Checkers.generatePossibleMoves(board, 1), [{5: black, 29: self.red}, {6: black, 29: self.red}])

    def test_generatePossibleMoves_rightMovesFor1BlackPieceAnd1RedPieceOnSecondTurn(self):
        black = Pieces.Black()
        board = {1: black, 29: self.red}
        self.assertEqual(Checkers.generatePossibleMoves(board, 2), [{1: black, 25: self.red}])

    def test_generatePossibleMoves_rightJumpsFor1BlackPieceAnd1RedPieceOnFirstTurn(self):
        black = Pieces.Black()
        board = {1: black, 6: self.red}
        self.assertEqual(Checkers.generatePossibleMoves(board, 1), [{10: black}])

    def test_generatePossibleMoves_rightJumpsFor1BlackPieceAnd1RedPieceOnSecondTurn(self):
        black = Pieces.Black()
        board = {1: black, 6: self.red}
        expectedBoard = [{1: black, 2: Pieces.RedKing()}]
        self.assertEqual(Checkers.generatePossibleMoves(board, 2), expectedBoard)

    def test_generatePossibleMoves_doubleJump(self):
        black = Pieces.Black()
        board = {1: black, 6: self.red, 14: self.red}
        expectedBoard = [{17: black}]
        self.assertEqual(Checkers.generatePossibleMoves(board, 1), expectedBoard)

    def test_generatePossibleMoves_twoPossibleJumps(self):
        black = Pieces.Black()
        board = {1: black, 6: self.red, 14: self.red, 15: self.red}
        expectedBoard = [{15: self.red, 17: black}, {14: self.red, 19: black}]
        self.assertEqual(Checkers.generatePossibleMoves(board, 1), expectedBoard)

    def test_possibleJumps_wrongDoubleJump(self):
        black = Pieces.Black()
        board = {1: black, 6: self.red, 9: self.red}
        expectedBoard = [{9: self.red, 10: black}]
        self.assertEqual(Checkers.possibleJumps(1, board), expectedBoard)

    def test_possibleJumps(self):
        black = Pieces.Black()
        board = {1: black, 6: self.red}
        self.assertEqual(Checkers.possibleJumps(1, board), [{10: black}])

    def test_generateMoves(self):
        black = Pieces.Black()
        board = {1: black}
        self.assertEqual(Checkers.possibleMoves(1, board), [{5: black}, {6: black}])

    def test_evaluateMove(self):
        black = Pieces.Black()
        board = {1: black}
        self.assertEqual(Checkers.evaluateMove(1, 5, board), [{5: black}])

    def test_move(self):
        black = Pieces.Black()
        board = {1: black}
        self.assertEqual(Checkers.move(1, 5, board), {5: black})

    @data(12, 20, 28, 5, 13, 21, 29)
    def test_validMoves_returnsXminus4_forSideSquares(self, value):
        self.assertEqual(self.red.validMoves(value), [value - 4])

    oddNonSideRows = list(set(oddRows) - set([12, 20, 28]) - set(topRow))

    @data(*oddNonSideRows)
    def test_validMoves_returnsXminus4andXminus3_forOddRows(self, value):
        self.assertEqual(self.red.validMoves(value), [value - 4, value - 3])

    evenNonSideRows = list(set(evenRows + bottomRow) - set([5, 13, 21, 29]))

    @data(*evenNonSideRows)
    def test_validMoves_returnsXpminus5andXminus4_forEvenRows(self, value):
        self.assertEqual(self.red.validMoves(value), [value - 5, value - 4])


@ddt
class TestKing(unittest.TestCase):

    king = Pieces.King()

    def test_validMoves_returns25_for29(self):
        self.assertEqual(self.king.validMoves(29), [25])

    def test_validMoves_returns8_for4(self):
        self.assertEqual(self.king.validMoves(4), [8])

    @data(5, 12, 13, 20, 21, 28)
    def test_validMoves_returnsXplus4andXminus4_forSideSquares(self, value):
        self.assertEqual(self.king.validMoves(value), [value + 4, value - 4])


@ddt
class TestCheckers(unittest.TestCase):

    @data(*oddRows)
    def test_isOnOddRow_returnsTrue_forOddRows(self, value):
        self.assertTrue(Engine.isOnOddRow(value))

    @data(*evenRows)
    def test_isOnOddRow_returnsFalse_forEvenRows(self, value):
        self.assertFalse(Engine.isOnOddRow(value))

    @data(*evenRows)
    def test_isOnEvenRow_returnsTrue_forEvenRows(self, value):
        self.assertTrue(Engine.isOnEvenRow(value))

    @data(*oddRows)
    def test_isOnEvenRow_returnsFalse_forOddRows(self, value):
        self.assertFalse(Engine.isOnEvenRow(value))

    @data(*bottomRow)
    def test_isOnBottomRow_returnsTrue_forBottomRows(self, value):
        self.assertTrue(Engine.isOnBottomRow(value))

    nonBottomRows = list(set(range(-10, 100)) - set(bottomRow))

    @data(*nonBottomRows)
    def test_isOnBottomRow_returnsFalse_forNonBottomRows(self, value):
        self.assertFalse(Engine.isOnBottomRow(value))

    nonTopRows = list(set(range(-10, 100)) - set(topRow))

    @data(*topRow)
    def test_isOnTopRow_returnsTrue_forTopRow(self, value):
        self.assertTrue(Engine.isOnTopRow(value))

    @data(*nonTopRows)
    def test_isOnTopRow_returnsFalse_forNonTopsRows(self, value):
        self.assertFalse(Engine.isOnTopRow(value))


@ddt
class TestConsoleGame(unittest.TestCase):

    redKing = Pieces.RedKing()
    blackKing = Pieces.BlackKing()

    @data((Pieces.Black(), 'b'), (Pieces.Red(), 'r'), (redKing, 'R'), (blackKing, 'B'))
    @unpack
    def test_getChar(self, piece, char):
        self.assertEqual(ConsoleGame.getChar(piece), char)

if __name__ == '__main__':
    unittest.main()
