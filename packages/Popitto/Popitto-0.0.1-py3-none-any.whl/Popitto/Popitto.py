import time

FIRST = 1
SECOND = 2

NONE = 0
POPPED = 1

NORESULT = 0
FIRSTWIN = 1
SECONDWIN = 2


class PopIt:
    def __init__(self, board=None, turn=FIRST):
        if board is None:
            self.board = [[NONE for _ in range(6)] for _ in range(6)]
        else:
            self.board = board
        self.turn = turn

    def makeMove(self, moveRow, numberOfPops):
        new_board = [row[:] for row in self.board] 
        for _ in range(numberOfPops):
            for col in range(6):
                if new_board[moveRow][col] == NONE:
                    new_board[moveRow][col] = POPPED
                    break
        new_turn = 3 - self.turn
        return PopIt(board=new_board, turn=new_turn)



def printPopIt(PopIt):
  for row in range(6):
    print(f"{row + 1} ", end="")
    for col in range(6):
      if PopIt.board[row][col] == NONE:
        print("🔲", end="")
      else:
        print("⬛", end="")
    print()
  print("   1 2 3 4 5 6")
  print()


def moveGen(PopIt):
  return [sum(1 for col in row if col == 0) for row in PopIt.board]


def makeMove(PopIt, moveRow, numberOfPops):
  for _ in range(numberOfPops):
    for col in range(6):
      if PopIt.board[moveRow][col] == NONE:
        PopIt.board[moveRow][col] = POPPED
        break
  PopIt.turn = 3 - PopIt.turn
  return PopIt


def boardFull(PopIt):
  for row in range(6):
    for col in range(6):
      if PopIt.board[row][col] == NONE:
        return False
  return True


def getResult(PopIt):
  if boardFull(PopIt):
    return PopIt.turn
  elif isCheckMate(PopIt):
    return 3 - PopIt.turn
  return NORESULT


def isCheckMate(PopIt):
  numPops = 0
  for row in range(6):
    for col in range(6):
      if PopIt.board[row][col] == NONE:
        numPops += 1
        if numPops > 1:
          return False
  return True

def perfD(PopIt, depth):
    if depth == 0:
        return 1
    nodes = 0
    row = 0
    for totalPopsAvail in moveGen(PopIt):
        for numberOfPops in range(1, totalPopsAvail + 1):
            newPopIt = PopIt.makeMove(row, numberOfPops)
            nodes += perfD(newPopIt, depth - 1)
        row += 1
    return nodes


def perfT(PopIt, maxDepth):
  startTime = time.time()
  totalNodes = 0
  for depth in range(1, maxDepth + 1):
    totalNodes += perfD(PopIt, depth)
    elapsed = time.time() - startTime
    print(
        f"info string perft depth {depth} nodes {totalNodes} time {int(1000 * elapsed)} nps {int(totalNodes / (elapsed + 0.00000001))}"
    )

Pop = PopIt()
perfT(Pop, 4)
