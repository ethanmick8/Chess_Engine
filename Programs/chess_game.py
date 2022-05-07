# Author: Ethan Mick
# Explanation: This is the main file for my implementation of Chess. It utilizes pygame to create a rudimentary
# chess environment that allows two players at the same screen to play a game of chess. I've added a lot of
# functionality like the ability to castle and promote pawns, but there's a lot of work left to be done if this
# program is to function more akin to that of a fully-fledged chess engine.

import pygame as pyg
import Pieces
import Engine

# Global Variables - used for calculations regarding movement/layout etc.
WIDTH = HEIGHT = 512
DIMENSION = 8
SIZE = HEIGHT // DIMENSION
FPS = 15
IMAGES = {}
invalid_move = "Invalid move! Try again."

# this function loads in the png images of the chess pieces, assigning them to their corresponding 2-character
# representations. The images are located in the "Images" folder in png form.
def loadPNGS():
    pieces = ["bp", "br", "bn", "bb", "bq", "bk", "wp", "wr", "wn", "wb", "wq", "wk"]
    for piece in pieces:
        IMAGES[piece] = pyg.transform.scale(pyg.image.load("images/" + piece + ".png"), (SIZE, SIZE))

# this function initializes a chess game
def createGame(screen, game):
    createBoard(screen)
    createPieces(screen, game.board)

# this function creates the chess board (w/o pieces) by using some global variables and the "Rect" feature
# of pygame.
def createBoard(screen):
    colors = [pyg.Color("white"), pyg.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row+column) % 2)]  # color based on position on board
            pyg.draw.rect(screen, color, pyg.Rect(column*SIZE, row*SIZE, SIZE, SIZE))

# this function creates the chess pieces and uses the "blit" feature of pygame to place them on top of the chess
# board (pyg.Rect....)
def createPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], pyg.Rect(column*SIZE, row*SIZE, SIZE, SIZE))

def main():
    pyg.init()
    screen = pyg.display.set_mode((WIDTH, HEIGHT))
    clock = pyg.time.Clock()
    screen.fill(pyg.Color("white"))
    game = Engine.Layout()
    loadPNGS()
    to_move = Pieces.Piece # init the piece to be moved, we don't know what it is yet
    selected = () # tuple in (row, column) form, keeps track of what square is selected by the user
    clicks = [] # keeps track of the coordinates of the start and destination of a piece [(r,c).(r,c)]
    castle = 0 # parameter for move_check that indicates whether a castling move can happen
    exitGame = False
    print("Welcome to Chess in pygame! Click the square of the piece you want to move followed by the")
    print("space you want to move it to to make a move. Only valid chess moves are accepted. When a move")
    print("is made, the simple row/column notation of that move will be displayed below. It's your responsibility")
    print("to determine when a player has won, as this program does not in its current state support")
    print("check/checkmate detection. Enjoy!\n")
    while not exitGame: # loop until game is exited
        for e in pyg.event.get():
            if e.type == pyg.QUIT:
                exitGame = True
            elif e.type == pyg.MOUSEBUTTONDOWN: # pygame detection of a click
                location = pyg.mouse.get_pos() # recognize a mouse click on a specific square
                column = location[0]//SIZE
                row = location[1]//SIZE
                if selected == (row, column): # make sure user hasn't already clicked
                    selected = () # reset to prevent invalid "move"
                    clicks = []
                else:
                    piece_type = Pieces.check_piece(row, column, game.board)
                    if not piece_type and len(clicks) == 0: # can't start with an empty space
                        continue # try again
                    elif len(clicks) == 0: # first click
                        to_move = piece_type
                        selected = (row, column)
                        clicks.append(selected)
                    else: # second click
                        selected = (row, column)
                        clicks.append(selected)
                if len(clicks) == 2: # only enter here if player has clicked twice, this is where the move occurs
                    piece = Pieces.check_piece(clicks[0][0], clicks[0][1], game.board)
                    if game.whiteMove and piece.color == "White": # white move
                        is_valid_move = to_move.move_check(to_move, clicks[0], clicks[1], game.board, castle)
                        if is_valid_move is True or is_valid_move == (True, 1) or is_valid_move == (True, 0):
                            to_move.promotion(to_move, clicks[0], clicks[1], game.board) # check for promotion
                            if is_valid_move == (True, 1): # castling move
                                white_rook_origin = (7, 7)
                                white_rook_to = (7, 5)
                                move = Engine.Move(white_rook_origin, white_rook_to, game.board, True)
                                game.makeMove(move)
                            move = Engine.Move(clicks[0], clicks[1], game.board, False)
                            current_move = move.get_notation()
                            print(current_move[0] + ' to ' + current_move[1])
                            game.makeMove(move) # make the move
                            selected = () # reset
                            clicks = []
                        else: # try again
                            print(invalid_move)
                            selected = ()
                            clicks = []
                    else:
                        if not game.whiteMove and piece.color == "Black": # black move
                            is_valid_move = to_move.move_check(to_move, clicks[0], clicks[1], game.board, castle)
                            if is_valid_move is True or is_valid_move == (True, 1) or is_valid_move == (True, 0):
                                to_move.promotion(to_move, clicks[0], clicks[1], game.board)  # promotion
                                print(castle)
                                if is_valid_move == (True, 1):
                                    black_rook_origin = (0, 7)
                                    black_rook_to = (0, 5)
                                    move = Engine.Move(black_rook_origin, black_rook_to, game.board, True)
                                    game.makeMove(move)
                                move = Engine.Move(clicks[0], clicks[1], game.board, False)
                                current_move = move.get_notation()
                                print(current_move[0] + ' to ' + current_move[1])
                                game.makeMove(move)  # make the move
                                selected = ()
                                clicks = []
                        else:
                            # otherwise, an opponents piece was clicked when it wasn't the opponent's turn
                            print("Wait your turn, bud.")
                            selected = () # reset
                            clicks = []

        createGame(screen, game)
        clock.tick(FPS) # fps setting
        pyg.display.flip() # update the screen


if __name__ == "__main__":
    main()

