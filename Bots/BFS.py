
# Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot
from Bots.BaseMove import *
from Bots.chessbot import *



def chess_bot(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]
    _, selected_piece, selected_move = wrongbfsMove(player_sequence, board, color, 3)
    return selected_piece, selected_move

value_pieces = {
    "k": 1000,
    "q": 700,
    "n": 400,
    "b": 300,
    "r": 500,
    "p": 100
}

def wrongbfsMove(player_sequence, board, our_color, step, score = 0):
    
    color = player_sequence[1]
    new_sequence = player_sequence[3:] + player_sequence[:3]
    
    player_pieces = give_pieces(color, board)
    moves = []
    for p in player_pieces:
        moves += [[p, m] for m in give_moves(p, board)]
    best_score = score
    best_move = moves[0]
    
    if color == our_color:
        for m in moves:
            s = 0
            p = board[m[1]]
            if p != '':
                s += value_pieces[p[0]]
            if step != 0:
                new_board = board.copy()
                new_board[m[1]] = new_board[m[0]]
                new_board[m[0]] = ''
                s, _, _ = bfsMove(new_sequence, new_board[::-1], our_color, step-1, score+s)
            
            if s > best_score:
                best_score = s
                best_move = m
    else:
        for m in moves:
            s = 0
            p = board[m[1]]
            if p != '':
                s -= value_pieces[p[0]]
            if step != 0:
                new_board = board.copy()
                new_board[m[1]] = new_board[m[0]]
                new_board[m[0]] = ''
                s, _, _ = bfsMove(new_sequence, new_board, our_color, step-1, score-s)
            
            if s > best_score:
                best_score = s
                best_move = m
                
    return (best_score, best_move[0], best_move[1])

register_chess_bot("WrongBFSMove", chess_bot)




def bfsMove(player_sequence, board, our_color, step, score = 0):
    
    color = player_sequence[1]
    new_sequence = player_sequence[3:] + player_sequence[:3]
    
    player_pieces = give_pieces(color, board)
    moves = []
    for p in player_pieces:
        moves += [[p, m] for m in give_moves(p, board)]
    best_score = score
    best_move = moves[0]
    
    #Something like this
    q = moves

    while not q:
        pass
                
    return best_move[0], best_move[1]