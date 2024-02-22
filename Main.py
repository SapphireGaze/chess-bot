import ChessEngine as ce
import chess as ch

class Game:

    def __init__(self, Board=ch.Board):
        self.Board=Board

    # Play human move
    def playHumanMove(self):
        try:
            print(self.Board, "\n")
            # Get user move
            print(self.Board.legal_moves)
            print("""To undo your last move, type "undo".""")
            play = input("Your move: ")

            # Undo
            if (play=="undo"):
                self.Board.pop()
                self.Board.pop()
                self.playHumanMove()
                return

            # Add move
            self.Board.push_san(play) # Reads SAN (Standard Algebraic Notation),
                                      # converts to a move parseable by python-chess

        except ch.InvalidMoveError:
            self.playHumanMove()

    # Play bot move
    def playEngineMove(self, maxDepth, color):
        print(self.Board, "\n")
        engine = ce.Engine(self.Board, maxDepth, color)
        self.Board.push(engine.getBestMove())

    def startGame(self):

        # Pre-game: Initialize settings
        color = None
        while(color!="b" and color!="w"):
            color = input("""Play as (type "b" or "w"): """)

        maxDepth = None
        while( isinstance(maxDepth, int) == False ):
            maxDepth = int(input("""Choose depth: """))

        # (Play first move if white)
        if color == "w":
            self.playHumanMove()
            print(self.Board) 

        # Main gameplay loop
        while ( self.Board.is_checkmate() == False ):
            # Bot move first
            print("The engine is thinking...")
            self.playEngineMove(maxDepth, ch.WHITE)

            # Bugfix: Check is_checkmate() after bot move

            # Human move last
            self.playHumanMove()

        # Game end
        print(self.Board)
        print(self.Board.outcome())

# (Equivalent to driver.cpp)
# Only runs if played directly from Main.py
# and not if included as a library
if __name__ == "__main__":
    newBoard = ch.Board()
    newGame = Game(newBoard)
    newGame.startGame()
