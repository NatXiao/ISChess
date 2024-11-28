import numpy

def chess_bot(player_sequence, board, time_budget, **kwargs):
    
    color = player_sequence[1]
    random_piece(color, board)
    #find all possible moves for one piece
   
    # return random in possible_mooves

    return (0,0), (0,0)

def random_piece(color, board):
    CHESS_PIECES = ["k",  "q", "n", "b", "r", "p"]
    selected_chess = (board.shape[0]-1, board.shape[1])
    chess_piece = []

    for x in range(board.shape[0]-1):
        for y in range(board.shape[1]):
            if board[x,y] == CHESS_PIECES+color:
                chess_piece.append((x, y))
    selected_chess = chess_piece[numpy.random(0, len(chess_piece)-1)]
    print(selected_chess)
    return selected_chess


def possible_moove():
    return 0
