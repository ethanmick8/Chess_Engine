# Author: Ethan Mick
# Description: Class from my simple chess library that describes the specifications of
# the pieces in the game and how they function. Several functions are included to check the
# legality of moves attempting to be made, and functionality is currently supported for every
# aspect of the game except for parts of check and all of checkmate. As of this writing, there's
# several things I'd like to improve regarding the implementation of the functions/classes in
# this file, but for now this is what it is.

import Engine
game = Engine.Layout()

# Base class for a Chess piece, includes methods for validating moves and checking color, as well as
# a method for checking if a move is a pawn promotion move
class Piece(object):
    def __init__(self, color):
        self.name = ""
        self.color = color

    def move_check(self, piece, origin, to, board, castle):
        return False

    def white_check(self):
        return self.color

    def promotion(self, piece, origin, to, board):
        return

# Pawn subclass of the Piece class, defines characteristics of, well, a Pawn
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'p'

    def move_check(self, piece, origin, to, board, castle):
        if abs(origin[1] - to[1]) == 1 or abs(origin[0] - to[0]) == 1 or abs(origin[0] - to[0]) == 2:
            captured_piece = check_piece(to[0], to[1], board)
            if captured_piece:
                if captured_piece.color != piece.color: # determine that capture attempt is not a friendly piece
                    return check_pawn(captured_piece, origin, to)
            else:
                return check_pawn(captured_piece, origin, to)
        return False

    def promotion(self, piece, origin, to, board):
        if board[origin[0]][origin[1]] == "wp" or board[origin[0]][origin[1]] == "bp":
            if abs(origin[1] - to[1]) == 1 or abs(origin[0] - to[0]) == 1:
                if to[0] == 0 or to[0] == 7:  # pawn reached the other side
                    print("Promotion Menu:")
                    print("1. Queen\n2. Bishop\n3. Knight\n4. Rook")
                    promote_to = int(input("What is your choice? (Enter number): "))
                    if promote_to == 1: # Queen
                        if piece.white_check() == "White":
                            board[origin[0]][origin[1]] = "wq"
                        else:
                            board[origin[0]][origin[1]] = "bq"
                        piece = Queen(piece.white_check())
                        return
                    elif promote_to == 2: # Bishop
                        if piece.white_check() == "White":
                            board[origin[0]][origin[1]] = "wb"
                        else:
                            board[origin[0]][origin[1]] = "bb"
                        piece = Bishop(piece.white_check())
                        return
                    elif promote_to == 3: # Knight
                        if piece.white_check() == "White":
                            board[origin[0]][origin[1]] = "wn"
                        else:
                            board[origin[0]][origin[1]] = "bn"
                        piece = Knight(piece.white_check())
                        return
                    elif promote_to == 4: # Rook
                        if piece.white_check() == "White":
                            board[origin[0]][origin[1]] = "wr"
                        else:
                            board[origin[0]][origin[1]] = "br"
                        piece = Queen(piece.white_check())
                        return
        return # not a promotion scenario

class Rook(Piece):
    def __init__(self, color, is_first_move=True):
        super().__init__(color)
        self.name = 'r'
        self.is_first_move = is_first_move

    def move_check(self, piece, origin, to, board, castle):
        if origin[0] == to[0] or origin[1] == to[1]: # valid move
            captured_piece = check_piece(to[0], to[1], board)
            if captured_piece:
                if captured_piece.color != piece.color: # determine that capture attempt is not a friendly piece
                    return check_straight(piece, board, origin, to)
            else:
                return check_straight(piece, board, origin, to)
        return False # otherwise, the move is invalid
        
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def move_check(self, piece, origin, to, board, castle):
        if abs(origin[0] - to[0]) == 2:
            if abs(origin[1] - to[1]) == 1:
                captured_piece = check_piece(to[0], to[1], board)
                if captured_piece:
                    if captured_piece.color != piece.color:
                        return True # valid Knight move
                else:
                    return True
        if abs(origin[0] - to[0]) == 1:
            if abs(origin[1] - to[1]) == 2:
                captured_piece = check_piece(to[0], to[1], board)
                if captured_piece:
                    if captured_piece.color != piece.color:
                        return True
                else:
                    return True
        return False # otherwise the move is invalid

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    def move_check(self, piece, origin, to, board, castle):
        if abs(origin[0] - to[0]) != 0 and abs(origin[1] - to[1]) != 0:
            if abs(origin[0] - to[0]) == abs(origin[1] - to[1]): # change in row/column must be the same
                captured_piece = check_piece(to[0], to[1], board)
                if captured_piece:
                    if captured_piece.color != piece.color:
                        return check_diagonal(board, origin, to)
                else:
                    return check_diagonal(board, origin, to)
        return False
        
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    def move_check(self, piece, origin, to, board, castle):
        if abs(origin[0] - to[0]) != 0 and abs(origin[1] - to[1]) != 0: # diagonal move
            if abs(origin[0] - to[0]) == abs(origin[1] - to[1]):
                captured_piece = check_piece(to[0], to[1], board)
                if captured_piece:
                    if captured_piece.color != piece.color:
                        return check_diagonal(board, origin, to)
                else:
                    return check_diagonal(board, origin, to)
        if origin[0] == to[0] or origin[1] == to[1]: # straight move
            captured_piece = check_piece(to[0], to[1], board)
            if captured_piece:
                if captured_piece.color != piece.color:
                    return check_straight(piece, board, origin, to)
            else:
                return check_straight(piece, board, origin, to)
        return False

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'k'

    def move_check(self, piece, origin, to, board, castle):
        if abs(origin[0] - to[0]) == 1 or abs(origin[1] - to[1]) == 1 or origin[1] - to[1] == -2:
            if abs(origin[0] - to[0]) > 1 or abs(origin[1] - to[1]) > 1:
                return False # catch crazy moves
            captured_piece = check_piece(to[0], to[1], board)
            if captured_piece:
                if captured_piece.color != piece.color:
                    return check_king(piece, board, origin, to, castle)
            else:
                return check_king(piece, board, origin, to, castle)
        return False

# this function checks the character representation of a board piece and returns the determined piece type of
# the piece in question.
def check_piece(row, column, board):
    piece = board[row][column]
    # determine what piece is at the square that the user selected
    if piece[0] == "w":
        if piece[1] == "p":
            piece_type = Pawn("White")
            return piece_type
        elif piece[1] == "r":
            piece_type = Rook("White")
            return piece_type
        elif piece[1] == "n":
            piece_type = Knight("White")
            return piece_type
        elif piece[1] == "b":
            piece_type = Bishop("White")
            return piece_type
        elif piece[1] == "q":
            piece_type = Queen("White")
            return piece_type
        elif piece[1] == "k":
            piece_type = King("White")
            return piece_type
    elif piece[0] == "b":
        if piece[1] == "p":
            piece_type = Pawn("Black")
            return piece_type
        elif piece[1] == "r":
            piece_type = Rook("Black")
            return piece_type
        elif piece[1] == "n":
            piece_type = Knight("Black")
            return piece_type
        elif piece[1] == "b":
            piece_type = Bishop("Black")
            return piece_type
        elif piece[1] == "q":
            piece_type = Queen("Black")
            return piece_type
        elif piece[1] == "k":
            piece_type = King("Black")
            return piece_type
    else:
        return None # empty square was chosen

# These variables are used in determining whether castling rooks have moved or not
# (Note: gotta find a better way to do this (maybe one that doesn't use globals)
black_castling_rook = check_piece(0, 7, game.board)
white_castling_rook = check_piece(7, 7, game.board)

# This function checks to make sure that a move along a column or row is valid, meaning it does not move over
# other game pieces. It is only called within the "move_check" method of a few pieces (aside from check_king's
# implementation) and thus, outside of check_king, it assumes that a piece *attempting* to be captured will always
# be of the opposite color. It returns True if the move is valid and False otherwise.
def check_straight(piece, board, origin, to):
    # If the move attempt is along a row
    if origin[0] == to[0]:
        if origin[1] < to[1]:
            for i in range(origin[1]+1, to[1]):
                if board[origin[0]][i] != "--":
                    return False # invalid move, there's a piece in the way
            if piece.color == "White": # castling logic; checking for a rook's first move
                if origin == (7, 7):
                    white_castling_rook.is_first_move = False
            else:
                if origin == (0, 7):
                    black_castling_rook.is_first_move = False
            return True
        if origin[1] > to[1]:
            for i in range(to[1]+1, origin[1]):
                if board[origin[0]][i] != "--":
                    return False # invalid move
            if piece.color == "White":
                if origin == (7, 7):
                    white_castling_rook.is_first_move = False
            else:
                if origin == (0, 7):
                    black_castling_rook.is_first_move = False
            return True

    # if the move attempt is along a column
    if origin[1] == to[1]:
        if origin[0] < to[0]:
            for i in range(origin[0]+1, to[0]):
                if board[i][origin[1]] != "--":
                    return False  # invalid move
            if piece.color == "White":
                if origin == (7, 7):
                    white_castling_rook.is_first_move = False
            else:
                if origin == (0, 7):
                    black_castling_rook.is_first_move = False
            return True
        if origin[0] > to[0]:
            for i in range(to[0]+1, origin[0]):
                if board[i][origin[1]] != "--":
                    return False  # invalid move
            if piece.color == "White":
                if origin == (7, 7):
                    white_castling_rook.is_first_move = False
            else:
                if origin == (0, 7):
                    black_castling_rook.is_first_move = False
            return True

# This function is very similar to check_straight, except it checks the diagonals of the board. It is used
# for checking bishop moves and Queen moves.
def check_diagonal(board, origin, to):
    # Quadrant I movement
    if origin[0] > to[0] and origin[1] < to[1]:
        length = 0
        for i in range(origin[1]+1, to[1]): # calculate length of path
            length += 1
        for j in range(1, length+1): # check all spaces in between for pieces
            if board[origin[0] - j][origin[1] + j] != "--":
                return False # move is invalid, it's path crosses another piece
        return True

    # Quadrant II movement
    if origin[0] > to[0] and origin[1] > to[1]:
        length = 0
        for i in range(to[0]+1, origin[0]):
            length += 1
        for j in range(1, length+1):
            if board[origin[0] - j][origin[1] - j] != "--":
                return False
        return True

    # Quadrant III movement
    if origin[0] < to[0] and origin[1] > to[1]:
        length = 0
        for i in range(origin[0]+1, to[0]):
            length += 1
        for j in range(1, length+1):
            if board[origin[0] + j][origin[1] - j] != "--":
                return False
        return True

    # Quadrant IV movement
    if origin[0] < to[0] and origin[1] < to[1]:
        length = 0
        for i in range(origin[1]+1, to[1]):
            length += 1
        for j in range(1, length+1):
            if board[origin[0] + j][origin[1] + j] != "--":
                return False # piece in the way
        return True

# This function is a little different than the previous 2 in that it checks for pawn moves, which are some
# of the most unique moves in the game. Still, it serves the same pupose: determine if the move is valid, if  so,
# return True, otherwise return False.
def check_pawn(captured_piece, origin, to):
    if captured_piece: # if the space to be moved to is occupied by an opponent's piece
        # pawn can't assassinate like this
        if abs(origin[0] - to[0]) == 2 or abs(origin[0] - to[0]) == 1:
            return False

        # pawn assassination verification
        elif abs(origin[1] - to[1]) == 1:
            return True
    else: # move is to an empty space
        # first move verification
        if abs(origin[0] - to[0]) == 2:
            if origin[0] == 1 or origin[0] == 6:  # pawn starter rows
                return True
            return False
        # assassination can't be performed on nothing
        elif abs(origin[1] - to[1]) == 1:
            return False
        else:
            return True

# This behemoth of a function is, truthfully, a work in progress and most likely not the most professional way
# of implementing something like this. The current functionality allows it to check that wherever the King is
# trying to be moved to won't put it in a check position, but it, along with all the other functions in this
# library, don't currently have a way of telling if the king is in check BEFORE a move is made. This is something
# that I plan to eventually add. Right now. check_king uses check_straight and check_diagonal in a unique way to
# instead check for threat in all directions of a destination space. It also checks if castling is possible assuming
# the user tries to make that move. Again, return type is True on valid move and false otherwise (except for castling,
# in which the return type includes the castle parameter so that the driver code can know to perform a special move).
def check_king(piece, board, origin, to, castle):
    checker = 0
    color = piece.color

    # first, check and see if a castling move is possible
    if origin[1] - to[1] == -2:
        if can_castle(piece, board, origin, to, castle):
            if color == "White":
                print("Castled!")
                castle = 1
                return True, castle
            else:
                # black_rook_origin = (0, 7)
                # black_rook_to = (0, 5)
                # move = Engine.Move(black_rook_origin, black_rook_to, board, True)
                # game.makeMove(move)
                print("Castled!")
                castle = 1
                return True, castle
        else:
            return False

    # for NSEW, check for hostile pieces that might make a King's move invalid
    i = to[0] + 1
    j = to[1] + 1
    try:
        while board[i][j]:
            scanner = [i, j]
            pawn_check = check_piece(i, j, board)
            if pawn_check == Pawn:
                if pawn_check.color != color: # hostile pawn
                    return False
            if abs(to[0] - i) == 2:
                if abs(to[1] - j) == 1:
                    check_knight = check_piece(i, j, board)
                    if check_knight == Knight:
                        if check_knight.color != color:
                            return False # hostile knight
            if abs(to[0] - i) == 1:
                if abs(to[1] - j) == 2:
                    check_knight = check_piece(i, j, board)
                    if check_knight == Knight:
                        if check_knight.color != color:
                            return False
            if check_diagonal(board, to, scanner):
                encountered = check_piece(i, j, board)
                if encountered == Bishop or encountered == Queen:
                    if encountered.color != color:
                        return False # King can't move into the path of an opponents piece
            straight_scanner = [i, to[1]]
            if check_straight(piece, board, to, straight_scanner): # check along column (+)
                straight_threat = check_piece(i, j, board)
                if straight_threat == Rook or straight_threat == Queen:
                    if straight_threat.color != color:
                        return False
            i += 1
            j += 1
    except IndexError: # board is out of range, no piece was encountered
        checker += 1
    i = to[0] - 1
    j = to[1] - 1
    try:
        while board[i][j]:
            scanner = [i, j]
            pawn_check = check_piece(i, j, board)
            if pawn_check == Pawn:
                if pawn_check.color != color:
                    return False
            if abs(to[0] - i) == 2:
                if abs(to[1] - j) == 1:
                    check_knight = check_piece(i, j, board)
                    if check_knight == Knight:
                        if check_knight.color != color:
                            return False
            if abs(to[0] - i) == 1:
                if abs(to[1] - j) == 2:
                    check_knight = check_piece(i, j, board)
                    if check_knight == Knight:
                        if check_knight.color != color:
                            return False
            if check_diagonal(board, to, scanner):
                encountered = check_piece(i, j, board)
                if encountered == Bishop or encountered == Queen:
                    if encountered.color != color:
                        return False
            straight_scanner = [i, to[1]]
            if check_straight(piece, board, to, straight_scanner): # check along column (-)
                straight_threat = check_piece(i, j, board)
                if straight_threat == Rook or straight_threat == Queen:
                    if straight_threat.color != color:
                        return False
            i -= 1
            j -= 1
    except IndexError:
        checker += 1
    i = to[0] - 1
    j = to[1] + 1
    try:
        while board[i][j]:
            scanner = [i, j]
            pawn_check = check_piece(i, j, board)
            if pawn_check == Pawn:
                if pawn_check.color != color:
                    return False
            if abs(to[0] - i) == 2:
                if abs(to[1] - j) == 1:
                    check_knight = check_piece(i, j, board)
                    if check_knight == Knight:
                        if check_knight.color != color:
                            return False
            if abs(to[0] - i) == 1:
                if abs(to[1] - j) == 2:
                    check_knight = check_piece(i, j, board)
                    if check_knight == Knight:
                        if check_knight.color != color:
                            return False
            if check_diagonal(board, to, scanner):
                encountered = check_piece(i, j, board)
                if encountered == Bishop or encountered == Queen:
                    if encountered.color != color:
                        return False
            straight_scanner = [to[0], j]
            if check_straight(piece, board, to, straight_scanner): # check along row (+)
                straight_threat = check_piece(i, j, board)
                if straight_threat == Rook or straight_threat == Queen:
                    if straight_threat.color != color:
                        return False
            i -= 1
            j += 1
    except IndexError:
        checker += 1
    i = to[0] + 1
    j = to[1] - 1
    try:
        while board[i][j]:
            scanner = [i, j]
            pawn_check = check_piece(i, j, board)
            if pawn_check == Pawn:
                if pawn_check.color != color:
                    return False
            if abs(to[0] - i) == 2:
                if abs(to[1] - j) == 1:
                    check_knight = check_piece(i, j, board)
                    if check_knight == Knight:
                        if check_knight.color != color:
                            return False
            if abs(to[0] - i) == 1:
                if abs(to[1] - j) == 2:
                    check_knight = check_piece(i, j, board)
                    if check_knight == Knight:
                        if check_knight.color != color:
                            return False
            if check_diagonal(board, to, scanner):
                encountered = check_piece(i, j, board)
                if encountered == Bishop or encountered == Queen:
                    if encountered.color != color:
                        return False
            straight_scanner = [to[0], j]
            if check_straight(piece, board, to, straight_scanner): # check along row (-)
                straight_threat = check_piece(i, j, board)
                if straight_threat == Rook or straight_threat == Queen:
                    if straight_threat.color != color:
                        return False
            i += 1
            j -= 1
    except IndexError:
        checker += 1

    if checker == 4: # no hostile pieces were detected
        return True

# This function checks to see if a passed in piece can castle. It returns False if it can't, and True if it can. It
# checks the game piece log of Engine.py for king moves first, before checking the global castle variables to see
# if their "is_first_move" values have been changed.
def can_castle(piece, board, origin, to, castle):
    color = piece.color

    for i in range(0, len(game.piece_log)):
        if color == "White" and game.piece_log[i] == "wk": # king already moved
            return False
        elif color == "Black" and game.piece_log[i] == "bk":
            return False

    if color == "White":
        if not white_castling_rook.is_first_move: # rook already moved
            return False
        else:
            temp_to = [7, 5]
            if check_king(piece, board, origin, temp_to, castle):
                temp_origin = [7, 5]
                if check_king(piece, board, temp_origin, to, castle):
                    return True
            return False
    else:
        if not black_castling_rook.is_first_move:
            return False
        else:
            temp_to = [7, 5]
            if check_king(piece, board, origin, temp_to, castle):
                temp_origin = [7, 5]
                if check_king(piece, board, temp_origin, to, castle):
                    return True
            return False
