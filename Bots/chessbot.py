import numpy as np

# Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot
from Bots.BaseMove import *

def chess_bot(player_sequence, board, time_budget, **kwargs):
    
    color = player_sequence[1]
    player_pieces = give_pieces(color, board)
    
    piece_moves = []
    while not piece_moves:
        piece_index = np.random.randint(0, len(player_pieces))
        selected_piece = player_pieces.pop(piece_index)
        piece_moves = give_moves(selected_piece, board)
    
    selected_move = piece_moves[np.random.randint(0, len(piece_moves))]
    
    # Return random move in possible_moves
    print(board[selected_piece[0],selected_piece[1]] + " " + str(selected_piece) + " -> " +
            board[selected_move[0],selected_move[1]] + " " + str(selected_move))
    print(piece_moves)
    return selected_piece, selected_move

def give_pieces(color, board):
    CHESS_PIECES = ["k", "q", "n", "b", "r", "p"]
    player_pieces = []

    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            for p in CHESS_PIECES:
                if board[x, y] == p + color:
                    player_pieces.append((x, y))
    
    return player_pieces

# Example how to register the function
register_chess_bot("RandomMoves", chess_bot)
