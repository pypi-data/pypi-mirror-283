# PopIt Game Documentation

## Overview
The `PopIt` game is a simple turn-based game where two players take turns popping elements on a 6x6 board. The game is won ehen one player forces the other to make the last move.

## Constants

- `FIRST = 1`: Represents the first player.
- `SECOND = 2`: Represents the second player.
- `NONE = 0`: Represents an empty spot on the board.
- `POPPED = 1`: Represents a popped spot on the board.
- `NORESULT = 0`: Indicates no result.
- `FIRSTWIN = 1`: Indicates a win for the first player.
- `SECONDWIN = 2`: Indicates a win for the second player.

## PopIt Class

### Initialization

```python
class PopIt:
    def __init__(self, board=None, turn=FIRST):
        if board is None:
            self.board = [[NONE for _ in range(6)] for _ in range(6)]
        else:
            self.board = board
        self.turn = turn
```

- `board`: A 6x6 matrix representing the game board. Defaults to an empty board if not provided.
- `turn`: Indicates the current player's turn. Defaults to `FIRST`.

### Methods

#### makeMove

```python
def makeMove(self, moveRow, numberOfPops):
    new_board = [row[:] for row in self.board]
    for _ in range(numberOfPops):
        for col in range(6):
            if new_board[moveRow][col] == NONE:
                new_board[moveRow][col] = POPPED
                break
    new_turn = 3 - self.turn
    return PopIt(board=new_board, turn=new_turn)
```

- `moveRow`: The row where the move is made.
- `numberOfPops`: The number of pops to make in the specified row.
- Returns a new `PopIt` object with the updated board and turn.

## Functions

### printPopIt

```python
def printPopIt(PopIt, fancy=False):
  for row in range(6):
    print(f"{row + 1} ", end="")
    for col in range(6):
      if fancy:
        if PopIt.board[row][col] == NONE:
          print("🔲", end="")
        else:
          print("⬛", end="")
      else:
        if PopIt.board[row][col] == NONE:
          print("-", end=" ")
        else:
          print("X", end=" ")
    print()
  if fancy:
    print("   1 2 3 4 5 6")
  else:
    print("  1 2 3 4 5 6")
  print()
```

- `PopIt`: The game state to be printed.
- `fancy`: Wether to print the fancy board or not (Default False)(Not all terminals support it)
- Prints the current state of the game board.

### moveGen

```python
def moveGen(PopIt):
    return [sum(1 for col in row if col == 0) for row in PopIt.board]
```

- `PopIt`: The game state.
- Returns a list indicating the number of available pops in each row.

### makeMove

```python
def makeMove(PopIt, moveRow, numberOfPops):
    for _ in range(numberOfPops):
        for col in range(6):
            if PopIt.board[moveRow][col] == NONE:
                PopIt.board[moveRow][col] = POPPED
                break
    PopIt.turn = 3 - PopIt.turn
    return PopIt
```

- `PopIt`: The game state.
- `moveRow`: The row where the move is made.
- `numberOfPops`: The number of pops to make in the specified row.
- Updates the game state with the specified move and returns the updated state.

### boardFull

```python
def boardFull(PopIt):
    for row in range(6):
        for col in range(6):
            if PopIt.board[row][col] == NONE:
                return False
    return True
```

- `PopIt`: The game state.
- Returns `True` if the board is full, otherwise `False`.

### getResult

```python
def getResult(PopIt):
    if boardFull(PopIt):
        return PopIt.turn
    elif isCheckMate(PopIt):
        return 3 - PopIt.turn
    return NORESULT
```

- `PopIt`: The game state.
- Returns the result of the game (`FIRSTWIN`, `SECONDWIN`, or `NORESULT`).

### isCheckMate

```python
def isCheckMate(PopIt):
    numPops = 0
    for row in range(6):
        for col in range(6):
            if PopIt.board[row][col] == NONE:
                numPops += 1
                if numPops > 1:
                    return False
    return True
```

- `PopIt`: The game state.
- Returns `True` if the game is in a checkmate position, otherwise `False`.

### perfD

```python
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
```

- `PopIt`: The game state.
- `depth`: The depth to search.
- Returns the number of nodes at the specified depth.

### perfT

```python
def perfT(PopIt, maxDepth):
    startTime = time.time()
    totalNodes = 0
    for depth in range(1, maxDepth + 1):
        totalNodes += perfD(PopIt, depth)
        elapsed = time.time() - startTime
        print(
            f"info string perft depth {depth} nodes {totalNodes} time {int(1000 * elapsed)} nps {int(totalNodes / (elapsed + 0.00000001))}"
        )
```

- `PopIt`: The game state.
- `maxDepth`: The maximum depth to search.
- Performs a perft (performance test) up to the specified depth and prints the results.

---

# Example Usage
Simple examples making use of the `Popitto` package
## Printing move generation
```python
import Popitto.Framework as Popitto
Pop = Popitto.PopIt()
print(Popitto.moveGen(Pop))
```
## Performing a performance test
```python
import Popitto.Framework as Popitto
Pop = Popitto.PopIt()
Popitto.perfT(Pop, 4)
```

## Simple Pop-It Game
```python
import Popitto.Framework as Popitto
Pop = Popitto.PopIt()
while True:
  Popitto.printPopIt(Pop)
  if Popitto.boardFull(Pop):
    print(f"{'First Player' if Popitto.getResult(Pop) == Popitto.FIRST else 'Second Player'} WON!")
    break

  moveRow = input("Select a row (1-6): ")
  numberOfPops = input("Select number of pops: ")
  Pop = Pop.makeMove(int(moveRow) - 1, int(numberOfPops))
```