
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

def give_score(board, p: tuple[int, int]):
    return value_pieces[board[p[0]][p[1]][0]] if board[p[0]][p[1]] != '' else 0

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
                s, _, _ = wrongbfsMove(new_sequence, new_board[::-1], our_color, step-1, score+s)
            
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
                s, _, _ = wrongbfsMove(new_sequence, new_board, our_color, step-1, score-s)
            
            if s > best_score:
                best_score = s
                best_move = m
                
    return (best_score, best_move[0], best_move[1])

register_chess_bot("WrongBFSMove", chess_bot)


# def bfsMove(player_sequence, board, step):
#     player_pieces = give_pieces(player_sequence[1], board)
#     nemesis_pieces = give_pieces(player_sequence[4], board)
#     dict_player_pieces = {}
#     dict_nemesis_pieces = {}


#     moves = []
#     for p in player_pieces:
#         dict_player_pieces[board[p[0]][p[1]]] = p
#         moves += [[give_score(board, m), [(p, m)]] for m in give_moves(p, board)]
#     for p in nemesis_pieces:
#         dict_nemesis_pieces[board[p[0]][p[1]]] = (7-p[0], 7-p[1])
    
#     q = moves
#     best_score = float('-inf')
#     best_move = None

#     while q:
#         n = q.pop(0)
#         score, mov = n
#         if score < 0:
#             continue
#         if len(mov) > step:
#             if score > best_score:
#                 best_score = score
#                 best_move = mov[0]
#                 print("->", end='')
#                 print(n)
#             if score == best_score and np.random.rand() > 0.5:
#                 best_score = score
#                 best_move = mov[0]
#                 print("r>", end='')
#                 print(n)
#             continue
        
#         new_board = board.copy()
#         new_player_pieces = dict_player_pieces.copy()
#         new_nemesis_pieces = dict_nemesis_pieces.copy()
#         me = True
#         for m in mov:
#             if me:
#                 new_player_pieces[board[m[0][0]][m[0][1]]] = m[1]
#                 del new_player_pieces[board[m[0][0]][m[0][1]]]
#                 if (7-m[1][0], 7-m[1][1])  in new_nemesis_pieces.values():
#                     del new_nemesis_pieces[board[m[1][0]][m[1][1]]]
#             else:
#                 new_nemesis_pieces[board[m[0][0]][m[0][1]]] = m[1]
#                 del new_nemesis_pieces[board[m[0][0]][m[0][1]]]
#                 if m[1] in new_player_pieces.values():
#                     del new_player_pieces[board[m[1][0]][m[1][1]]]
#             p = new_board[m[0]]
#             new_board[m[0]] = ''
#             new_board[m[1]] = p
#             me = not me
        
#         if me:
#             pieces = new_player_pieces.values()
#             for p in pieces:
#                 q += [[score + give_score(new_board, m), mov + [(p, m)]] for m in give_moves(p, new_board)]
#         else:
#             new_board = np.array([list(b[::-1]) for b in new_board[::-1]])
#             pieces = new_nemesis_pieces.values()
#             for p in pieces:
#                 q += [[score - 1.5 * give_score(new_board, m), mov + [((7 - p[0], 7 - p[1]), (7 - m[0], 7 - m[1]))]] for m in give_moves((7 - p[0], 7 - p[1]), new_board)]
    
#     return best_move[0], best_move[1]

def bfsMove(player_sequence, board, depth):
    color = player_sequence[1]
    player_sequence = player_sequence[1] + player_sequence[4]
    queue = [(board, player_sequence, 0, 0, None)]
    # (current board, player sequence, current depth, score, move)
    visited = {}
    best_move = None
    start_move = None
    best_score = 0
    
    while queue:
        current_board, current_sequence, current_depth, current_score, base_move = queue.pop(0)
        
        if current_depth == depth or current_score < 0 + current_depth*50:
            continue

        # Generate all possible moves for the current player
        player_pieces = give_pieces(current_sequence[0], current_board)
        possible_moves = []
        
        for p in player_pieces:
            possible_moves += [(p, m) for m in give_moves(p, current_board, color == current_sequence[0])]
        
        for move in possible_moves:
            new_board = current_board.copy()
            eated = new_board[move[1][0]][move[1][1]]
            new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
            new_board[move[0][0]][move[0][1]] = ''
            
            score = current_score
            if eated != '':
                if color == current_sequence[0]:
                    score += value_pieces[eated[0]]
                else:
                    score -= value_pieces[eated[0]]
            
            new_sequence = current_sequence[1:] + current_sequence[0]
            
            if base_move is None:
                queue.append((new_board, new_sequence, current_depth + 1, score, move))
                start_move = possible_moves
            else:
                queue.append((new_board, new_sequence, current_depth + 1, score, base_move))
            
            if score > best_score:
                best_score = score
                best_move = base_move
            if score == best_score and np.random.rand() > 0.5:
                best_score = score
                best_move = base_move
        
        if best_score >= 1000:
            break
    
    if not best_move:
        best_move = start_move[np.random.randint(0,len(possible_moves))]
    return best_move

def chess_bot_bfs(player_sequence, board, time_budget, **kwargs):
    selected_piece, selected_move = bfsMove(player_sequence, board, 5)
    return selected_piece, selected_move


def chess_bot_test(player_sequence, board, time_budget, **kwargs):

    for b in board:
        print(b)
    
    for b in board[::-1]:
        print(b)

    new_board = board
    move = [((1, 3), (2, 3)), ((7, 1), (5, 2)), ((0, 3), (7, 3)), ((7, 2), (6, 3))]
    for m in move:
        p = new_board[m[0]]
        new_board[m[0]] = ''
        new_board[m[1]] = p

    print("-------------------------------------")

    for b in board:
        print(b)
    
    for b in board[::-1]:
        print(b)

    return (0,1), (0,1)


register_chess_bot("Test", chess_bot_test)
register_chess_bot("BFSMove", chess_bot_bfs)