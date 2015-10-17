__author__ = 'jspear'


def isOnEvenRow(position): return inRange(position, 1, 32) and not isOnOddRow(position)


def isOnEdge(pos):
    return isOnTopRow(pos) or isOnBottomRow(pos)or isOnRightEdge(pos) or isOnLeftEdge(pos)


def isOnRightEdge(position): return ((position - 4) % 8) == 0


def isOnOddRow(position):
    inFirstRow = inRange(position, 1, 4)
    inThirdRow = inRange(position, 9, 12)
    inFifthRow = inRange(position, 17, 20)
    inSeventhRow = inRange(position, 25, 28)
    return inFirstRow or inThirdRow or inFifthRow or inSeventhRow


def isOnLeftEdge(position): return (position - 5) % 8 == 0


def isOnBottomRow(position): return inRange(position, 29, 32)


def isOnTopRow(position): return inRange(position, 1, 4)


def inRange(n, start, end): return (n >= start) and (n <= end)
"""range including last element"""
