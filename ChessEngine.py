import chess as ch # AKA python-chess
import random

class Engine:
    # Properties:
        # - Board 
        #   - (class object imported from python-chess; not defined by us)
        #   - legal_moves: property of Board
        # - color (b/w)
        # - maxDepth (higher depth = bigger brain, slower computing time)

    # Methods:
        # public:
        #   - getBestMove() (called by Main.py)
        #       - calls recursive search
        #       - returns Move with best evaluation
        # private: 
        #   - search(Move candidate, int depth)
        #       - 

    # Constructors:
        # - Parameterized: (Board, maxDepth, color)

    def __init__(self, Board, maxDepth, color):
        self.Board = Board
        self.color = color
        self.maxDepth = maxDepth
        self.pieceValues = {
            ch.PAWN : 1,
            ch.ROOK : 5.1,
            ch.BISHOP : 3.33,
            ch.KNIGHT : 3.2,
            ch.QUEEN : 8.8,
            ch.KING : 10_000} # based on Hans Berliner System
    
    def getBestMove(self):
        bestMove, bestValue = self.search(candidate = None, depth = 1) # self is passed automatically
        print(bestMove, bestValue)
        return bestMove

    def evaluate(self):
        score = 0

        # Iternate through entire board, sum up piece values of each square
        for i in range(64):
            score += self.evalSquareValue(ch.SQUARES[i])

        # Misc. score improvements - ADD MORE LOGIC HERE
        score += (
              self.evalMateOpportunity()
            + self.evalOpening()
            + (0.001 * random.random()) # ensure bot doesn't play exact same moves in each scenario - less predictable
        )
        return score


    def evalMateOpportunity(self):
        ### Stalemate or checkmate is worst outcome ###

        if (self.Board.legal_moves.count()==0):
            if (self.Board.turn == self.color):
                return -999
            else:
                return 999
        else:
            return 0


    # Prioritize the bot developing the opening
    def evalOpening(self):
        if (self.Board.fullmove_number<10):
            if (self.Board.turn == self.color):
                return 1/30 * self.Board.legal_moves.count()
            else:
                return -1/30 * self.Board.legal_moves.count()
        else:
            return 0

    # Takes a square as input and returns
    # the corresponding Hans Berliner's
    # system value of the piece atop it
    def evalSquareValue(self, square):
        piece_type = self.Board.piece_type_at(square)
        if piece_type:
            pieceValue = self.pieceValues[piece_type]
            ishumanColor = self.Board.color_at(square) == self.color
            return pieceValue if ishumanColor else -pieceValue # python ternary operator
        return 0
            

    # Recursive search function
    def search(self, candidate, depth):
        
        #reached max depth of search or no possible moves
        if ( depth == self.maxDepth or self.Board.legal_moves.count() == 0 ):
            return self.evaluate()
        
        else:
            # Get list of legal moves of the current position
            moveList = list(self.Board.legal_moves)
            
            # Initialise newCandidate
            newCandidate = None
            #(uneven depth means engine's turn)
            if(depth % 2 != 0):
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")
            
            # Analyze board after deeper moves
            for i in moveList:

                # TEMPORARILY play move i
                self.Board.push(i)

                # Get value of move i (by exploring the repercussions)
                value = self.search(newCandidate, depth + 1) 

                # Basic minimax algorithm:
                # if bot's turn, maximize value
                # if human's turn, minimize value

                # Bot - Maximize
                if(value > newCandidate and depth % 2 != 0):
                    if (depth == 1):
                        move = i
                    newCandidate = value

                # Human - Minimize
                elif(value < newCandidate and depth % 2 == 0):
                    newCandidate = value

                # Alpha-beta pruning cuts: 
                # (if previous move was made by the engine)
                if (candidate != None
                 and value < candidate
                 and depth % 2 == 0):
                    self.Board.pop()
                    break

                #(if previous move was made by the human player)
                elif (candidate != None 
                 and value > candidate 
                 and depth % 2 != 0):
                    self.Board.pop()
                    break
                
                # Undo TEMP move
                self.Board.pop()

            # Return result
            if (depth > 1):
                # Return value of a move in the tree
                return newCandidate
            else:
                # Return the move (only on first move)
                return (move, newCandidate)