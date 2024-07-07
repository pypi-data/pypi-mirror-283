# Connectide Game Documentation

## Overview

The `connectide` module provides a class-based implementation of the Connect-4 game. This module includes various functionalities to represent the game board, manage game state, and perform operations like move generation, checking for wins, adding and undoing moves, and running performance tests.

## Constants

- `noPce = 0`: Represents an empty spot on the board.
- `red = 1`: Represents a red piece on the board.
- `yellow = 2`: Represents a yellow piece on the board.

## Board Class

### Initialization

```python
class Board:
    def __init__(self, board=None, turn=red):
        if board is None:
            self.board = [[noPce for _ in range(7)] for _ in range(6)]
        else:
            self.board = board
        self.turn = turn
```

- `board`: A 6x7 matrix representing the game board. Defaults to an empty board if not provided.
- `turn`: Indicates the current player's turn. Defaults to `red`.

### Methods

#### `isConnect4`

```python
def isConnect4(self, row: int, col: int) -> bool:
    board = self.board
    pce = board[row][col]

    if pce is not noPce:
        if row >= 3 and board[row - 1][col] == pce and board[row - 2][col] == pce and board[row - 3][col] == pce:
            return True
        if row <= 2 and board[row + 1][col] == pce and board[row + 2][col] == pce and board[row + 3][col] == pce:
            return True
        if col <= 3 and board[row][col + 1] == pce and board[row][col + 2] == pce and board[row][col + 3] == pce:
            return True
        if col >= 3 and board[row][col - 1] == pce and board[row][col - 2] == pce and board[row][col - 3] == pce:
            return True
        if row >= 3 and col <= 3 and board[row - 1][col + 1] == pce and board[row - 2][col + 2] == pce and board[row - 3][col + 3] == pce:
            return True
        if row <= 2 and col <= 3 and board[row + 1][col + 1] == pce and board[row + 2][col + 2] == pce and board[row + 3][col + 3] == pce:
            return True
        if row >= 3 and col >= 3 and board[row - 1][col - 1] == pce and board[row - 2][col - 2] == pce and board[row - 3][col - 3] == pce:
            return True
        if row <= 2 and col >= 3 and board[row + 1][col - 1] == pce and board[row + 2][col - 2] == pce and board[row + 3][col - 3] == pce:
            return True

    return False
```

- `row`: The row of the square.
- `col`: The column of the square.
- Returns `True` if the square is part of a 4-in-a-row, otherwise `False`.

#### `isCheckmate`

```python
def isCheckmate(self) -> bool:
    for row in range(6):
        for col in range(7):
            if self.isConnect4(row, col):
                return True
    return False
```

- Returns `True` if a 4-in-a-row is present on the board, otherwise `False`.

#### `pseudoLegalMoveGen`

```python
def pseudoLegalMoveGen(self) -> list[int]:
    moves = []
    board = self.board
    for col in range(7):
        if board[0][col] == noPce:
            moves.append(col)
    return moves
```

- Returns a list of pseudo-legal moves (legal columns), which includes moves even after a board is in checkmate.

#### `moveGen`

```python
def moveGen(self) -> list[int]:
    moves = []
    if not self.isCheckmate():
        board = self.board
        for col in range(7):
            if board[0][col] == noPce:
                moves.append(col)
    return moves
```

- Returns a list of legal moves (legal columns).

#### `addPiece`

```python
def addPiece(self, col: int):
    pce = self.turn
    for row in range(6):
        if self.board[row][col] != noPce:
            self.board[row - 1][col] = pce
            self.turn = 3 - pce
            break
        if row == 5 and self.board[row][col] == noPce:
            self.board[row][col] = pce
            self.turn = 3 - pce
            break
```

- `col`: The column to add a piece.

#### `undoMove`

```python
def undoMove(self, col: int):
    for row in range(6):
        if self.board[row][col] != noPce:
            self.board[row][col] = noPce
            self.turn = 3 - self.turn
            break
```

- `col`: The column from which to undo a move.

#### `getNumMoves`

```python
def getNumMoves(self) -> int:
    moves = 0
    for i in range(6):
        for j in range(7):
            if self.board[i][j] != noPce:
                moves += 1
    return moves
```

- Returns the number of pieces on the board.

#### `show`

```python
def show(self, debug: bool = False):
    board = self.board
    for i in range(6):
        for j in range(7):
            pce = board[i][j]
            pceChar = "-" if pce == noPce else "R" if pce == red else "Y"
            print(pceChar, end=" ")
        if i != 5:
            print()
    print("\n-------------")
    print("1 2 3 4 5 6 7 ")
    if debug:
        print(f"Turn: {'red' if self.turn == red else 'yellow'}")
        print(f"Moves Played: {self.getNumMoves()}")
        print(f"Checkmate Status: {'True' if self.isCheckmate() else 'False'}")
    print()
```

- `debug` (optional): Whether to print additional debug information. Defaults to `False`.

#### `chash`

```python
def chash(self) -> str:
    fen = ""
    for i in range(len(self.board)):
        for j in range(len(self.board[0])):
            fen += str(self.board[i][j])
    return fen + str(self.turn)
```

- Returns a simple hash of the board position.

#### `flatten`

```python
def flatten(self) -> list[int]:
    flat = []
    for i in range(len(self.board)):
        for j in range(len(self.board[0])):
            flat.append(self.board[i][j])
    return flat
```

- Returns the flattened board array as a 1D list.

#### `parse`

```python
def parse(self, string: str):
    i = 0
    j = 0
    count = 0

    for char in string:
        count += 1
        if count == 43:
            self.turn = int(char)
            break
        if i == 7:
            i = 0
            j += 1

        self.board[j][i] = int(char)
        i += 1
```

- `string`: The string board representation created by `chash`.

#### `perfD`

```python
def perfD(self, depth: int) -> int:
    if depth == 0:
        return 1
    nodes = 0
    legals = self.moveGen()
    for col in legals:
        self.addPiece(col)
        nodes += self.perfD(depth - 1)
        self.undoMove(col)
    return nodes
```

- `depth`: The depth to search to.
- Returns the number of nodes at a specified depth.

#### `perfT`

```python
def perfT(self, maxDepth: int):
    startTime = time.time()
    for depth in range(1, maxDepth + 1):
        nodes = self.perfD(depth)
        elapsed = time.time() - startTime
        print(
            f"info string perft depth {depth} time {int(elapsed*1000)} nodes {nodes} nps {int(nodes / (elapsed + 0.000000001))}"
        )
```

- `maxDepth`: The maximum depth to run for this test.
- Initiates a performance test.

### Example Usage

```python
board = Board()
board.show()
board.parse("0000000000000000000000000000000000000000012")
board.perfT(7)
```