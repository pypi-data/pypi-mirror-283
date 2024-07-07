import time

noPce = 0
red = 1
yellow = 2

class Board():
    '''
    A class for the board representation and several helper functions for the Connect-4 game
    There are a few descriptors being used to describe different types of elements here:

    BASE - Basic functions

    HELPERS - Functions that assist with base functions

    ADDITION - Additional functions
    '''
    def __init__(self, board = None, turn = red):
        if board is None:
            self.board = [[noPce for _ in range(7)] for _ in range(6)]
        else:
            self.board = board
        self.turn = turn

    def isConnect4(self, row : int, col : int) -> bool:
        '''
        HELPER: Returns True if the current square is part of a 4 in a row combination

        PARAMS:
        
        row - The row of the square

        col - The column of the square
        '''
        board : list[int:int] = self.board
        pce : int = board[row][col]

        if pce is not noPce:

            if row >= 3 and board[row - 1][col] == pce and board[
                    row - 2][col] == pce and board[row - 3][col] == pce:
                return True

            if row <= 2 and board[row + 1][col] == pce and board[
                    row + 2][col] == pce and board[row + 3][col] == pce:
                return True

            if col <= 3 and board[row][col + 1] == pce and board[row][
                    col + 2] == pce and board[row][col + 3] == pce:
                return True

            if col >= 3 and board[row][col - 1] == pce and board[row][
                    col - 2] == pce and board[row][col - 3] == pce:
                return True

            if row >= 3 and col <= 3 and board[row - 1][col + 1] == pce and board[
                    row - 2][col + 2] == pce and board[row - 3][col + 3] == pce:
                return True

            if row <= 2 and col <= 3 and board[row + 1][col + 1] == pce and board[
                    row + 2][col + 2] == pce and board[row + 3][col + 3] == pce:
                return True

            if row >= 3 and col >= 3 and board[row - 1][col - 1] == pce and board[
                    row - 2][col - 2] == pce and board[row - 3][col - 3] == pce:
                return True

            if row <= 2 and col >= 3 and board[row + 1][col - 1] == pce and board[
                    row + 2][col - 2] == pce and board[row + 3][col - 3] == pce:
                return True

        return False

    def isCheckmate(self) -> bool:
        '''
        BASE: Returns True if a 4 in a row is present in the current board
        '''
        for row in range(6):
            for col in range(7):
                if (self.isConnect4(row, col)):
                    return True

        return False

    def pseudoLegalMoveGen(self) -> list[int]:
        '''
        BASE: Returns a list of pseudo-legal moves (legal columns), which includes moves even after a board is in checkmate
        '''
        moves : list[int] = []
        board : list[int:int] = self.board
        for col in range(7):
            if board[0][col] == noPce:
                moves.append(col)
        return moves

    def moveGen(self) -> list[int]:
        '''
        BASE: Returns a list of legal moves (legal columns)
        '''
        moves : list[int] = []
        if not self.isCheckmate():
            board : list[int:int] = self.board
            for col in range(7):
                if board[0][col] == noPce:
                    moves.append(col)
        return moves

    def addPiece(self, col : int):
        '''
        BASE: Adds a piece to a column

        PARAMS:
        
        col - The column to add a piece
        '''
        pce : int = self.turn
        for row in range(6):
            if self.board[row][col] != noPce:
                self.board[row - 1][col] = pce
                self.turn = 3 - pce
                break
            if row == 5 and self.board[row][col] == noPce:
                self.board[row][col] = pce
                self.turn = 3 - pce
                break

    def undoMove(self, col : int):
        '''
        BASE: Undoes a move at a specified column

        PARAMS:
        
        col - The column which you wish to undo a move
        '''
        for row in range(6):
            if self.board[row][col] != noPce:
                self.board[row][col] = noPce
                self.turn = 3 - self.turn
                break

    def getNumMoves(self) -> int:
        '''
        HELPER: Returns the number of pieces on board
        '''
        moves : int = 0
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != noPce:
                    moves += 1
        return moves

    def show(self, debug : bool = False):
        '''
        BASE: Prints the board to the screen

        PARAMS:
        
        debug - Wether you are debugging or not
        '''
        board : list[int:int] = self.board
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
            print(f"Turn: {"red" if self.turn == red else "yellow"}")
            print(f"Moves Played: {self.getNumMoves()}")
            print(f"Checkmate Statues: {"True" if self.isCheckmate() else "False"}")
        print()


    def chash(self) -> str:
        '''
        BASE: Simple hashing of the board position
        '''
        fen : str = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                fen += str(self.board[i][j])
        return fen + str(self.turn)

    def flatten(self) -> list[int]:
        '''
        BASE: Flatten the board array
        '''
        flat : list[int] = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                flat.append(self.board[i][j])
        return flat

    def parse(self, string : str):
        '''
        Base: Parses the string board representation by chash

        PARAMS:

        string - The string board representation created by chash
        '''
        i : int = 0
        j : int = 0
        count : int = 0

        for char in string: 
            count += 1
            if count == 43:
                self.turn == int(char)  
                break
            if i == 7:
                i = 0
                j += 1

            self.board[j][i] = int(char)
            i += 1

    def perfD(self, depth : int) -> int:
        '''
        HELPER: Returns the number of nodes at a specified depth

        PARAMS:

        depth - The depth to search to
        '''
        if depth == 0:
            return 1
        nodes : int = 0
        legals : int = self.moveGen()
        for col in legals:
            self.addPiece(col)
            nodes += self.perfD(depth - 1)
            self.undoMove(col)
        return nodes


    def perfT(self, maxDepth : int):
        '''
        ADDITION - Initiates a performance test

        PARAMS:

        maxDepth - The maximum depth to run for this test
        '''
        startTime : float = time.time()
        for depth in range(1, maxDepth + 1):
            nodes : int = self.perfD(depth)
            elapsed : float = time.time() - startTime
            print(
                f"info string perft depth {depth} time {int(elapsed*1000)} nodes {nodes} nps {int(nodes / (elapsed + 0.000000001))}"
            )
'''EXAMPLE
board = Board()
board.show()
board.parse("0000000000000000000000000000000000000000012")
board.perfT(7)
'''