import chess as ch # AKA python-chess
import random

class Bot:
    # Properties:
        # - class: Board 
        #   - (class object imported from python-chess; not defined by us)
        #   - legal_moves: property of Board
        # - enum: Color
        #   - takes python-chess defined enums ch.WHITE / ch.BLACK
        # - int: max_depth
        #   - higher depth = bigger brain, slower computing time

    # Methods:
        # public:
        #   - getBestMove() (called by Main.py)
        #       - calls recursive search
        #       - returns Move with best evaluation
        # private: 
        #   - search()
        #   - evaluate()

    def __init__(self, Board, max_depth, Color):
        self.Board = Board
        self.Color = Color
        self.max_depth = max_depth
    
    def getBestMove(self):
        best_move = random.choice(list(self.Board.legal_moves))
        return best_move

    # Move score based on current board state
    def evaluate(self):
        pass

    # Recursive search function
    def search(self, depth):
        pass