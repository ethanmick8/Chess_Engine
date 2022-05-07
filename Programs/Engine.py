# Author: Ethan Mick
# Explanation: This file outlines classes pertaining to the chess board and moves on the chess board.

# Class defining the layout of the chess board, as well as the action of moving pieces to different
# positions on the game board.
class Layout(object):
    def __init__(self):
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
        ]
        self.whiteMove = True  # white moves first
        self.move_history = [] # logs moves
        self.piece_log = [] # logs pieces that have been moved

    def makeMove(self, move): # move a piece
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.stop_row][move.stop_col] = move.moved_piece
        self.move_history.append(move) # just keeps track of moves made
        self.piece_log.append(self.board[move.stop_row][move.stop_col]) # keeps track of pieces moved
        if not move.castle_check: # if the move isn't a castle move (99% of the time it won't be)
            self.whiteMove = not self.whiteMove # after a move is made, it's the next players turn to move

# class that defines parameters necessary for making a move, as well as converting moves into the chess notation
# representation for display to the user after a move is made.
class Move(object):
    # converting regular matrix notations to chess board notation (e7, d2, etc etc)
    # visualization:
    # [(0,0), (0,1), (0,2) ... (0,7)]      [(a,8), (b,8), (c,8) ... (h,8)]
    # [(1,0), (1,1), ... ...   (1,7)]      [(a,7), (b, 7), ... ...  (h,7)]
    # [   ...                       ]      [   ...                       ]
    # [   ...                       ]  ->  [   ...                       ]
    # [   ...                       ]      [   ...                       ]
    # [   ...                       ]      [   ...                       ]
    # [   ...                       ]      [   ...                       ]
    # [(7,0), (7,1), ... ...   (7,7)]      [(a,1), (b,1), ... ...   (h,1)]
    rows_to_chess_nums = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    convert_rows = {value: key for key, value in rows_to_chess_nums.items()}
    cols_to_chess_chars = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    convert_cols = {value: key for key, value in cols_to_chess_chars.items()}

    def __init__(self, start, stop, board, castle_check):
        self.start_row = int(start[0])
        self.start_col = int(start[1])
        self.stop_row = int(stop[0])
        self.stop_col = int(stop[1])
        self.castle_check = castle_check
        self.moved_piece = board[self.start_row][self.start_col]
        self.captured_piece = board[self.stop_row][self.stop_col]

    # this method retrieves the notation of a move, for example (b7 to b5) (a pawn's first move)
    def get_notation(self):
        start = self.get_conversion(self.start_row, self.start_col)
        stop = self.get_conversion(self.stop_row, self.stop_col)
        move_record = [start, stop]
        return move_record

    # finally, this method retrieves the conversion of moves into chess notation, useful within the previous
    # functions implementation
    def get_conversion(self, row, column):
        return self.convert_cols[column] + self.convert_rows[row]
