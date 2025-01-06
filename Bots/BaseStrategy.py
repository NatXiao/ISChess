from Bots.BaseMove import *
import numpy as np

CHESS_PIECES = {"k", "q", "n", "b", "r", "p"}

def give_pieces(color, board):
    """
    Return all the piece for a given color
    @color: color of the pieces we want
    @board: chess board
    @return: list of tuple corresponding of the position of the pieces
    """
    player_pieces = np.argwhere(np.isin(board, [p + color for p in CHESS_PIECES]))
    return [tuple(pos) for pos in player_pieces]

def create_board(move, board):
    """
    Return new board
    @move: move done to create the new board
    @board: chess board
    @return: new board
    """
    new_board = board.copy()
    piece = new_board[move[0]]
    eated = new_board[move[1]]
    new_board[move[1]] = piece
    new_board[move[0]] = ''
    return (new_board, piece, eated)

def check_check(piece, board, advance):
    """
    Check if the piece put the adversery king in check
    @piece: position of the piece
    @board: chess board
    @advance: direction for pawn
    @return: boolean if the piece put king in check
    """
    move = give_moves(piece, board, advance)
    for m in move:
        n = board[m]
        if n != '' and (n[0] is 'k' and n[1] != board[piece][1]):
            return True
    return False