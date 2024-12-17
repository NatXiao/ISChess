
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
        
    
    if not best_move:
        best_move = start_move[np.random.randint(0,len(possible_moves))]
    return best_move

def chess_bot_bfs(player_sequence, board, time_budget, **kwargs):
    selected_piece, selected_move = bfsMove(player_sequence, board, 5)
    return selected_piece, selected_move


def visited_bfsMove(player_sequence, board, depth):
    visite = 0
    color = player_sequence[1]
    player_sequence = player_sequence[1] + player_sequence[4]
    queue = [(board, player_sequence, 0, 0, None)]
    # (current board, player sequence, current depth, score, move)
    visited = {}
    best_move = []
    start_move = None
    best_score = 0
    
    while queue:
        visite += 1
        current_board, current_sequence, current_depth, current_score, base_move = queue.pop(0)
        
        if current_depth >= depth:
            continue
        
        tupled_board = str(current_board) + str(current_sequence)
        if tupled_board in visited.keys():
            if visited[tupled_board][1] < current_depth or visited[tupled_board][0] > current_score:
                continue
            elif visited[tupled_board][1] > current_depth and visited[tupled_board][0] == current_score:
                visited[tupled_board] = (current_score, current_depth)
            elif visited[tupled_board][0] < current_score:
                visited[tupled_board] = (current_score, current_depth)
            elif visited[tupled_board][0] == current_score and np.random.rand() > 0.5:
                visited[tupled_board] = (current_score, current_depth)

        else:
            visited[tupled_board] = (current_score, current_depth)


        # Generate all possible moves for the current player
        player_pieces = give_pieces(current_sequence[0], current_board)
        possible_moves = []
        
        for p in player_pieces:
            possible_moves += [(p, m) for m in give_moves(p, current_board, color == current_sequence[0])]
        
        if color == current_sequence[0]:
            for move in possible_moves:
                new_board = current_board.copy()
                piece = new_board[move[0][0]][move[0][1]]
                eated = new_board[move[1][0]][move[1][1]]
                new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
                new_board[move[0][0]][move[0][1]] = ''
                
                score = current_score
                if piece[0] == 'p':
                    score += value_pieces['n']
                    if move[1][0] == 7:
                        score += value_pieces['q']
                        new_board[move[1][0]][move[1][1]] = 'q' + piece[1]
                if eated != '':
                    score += value_pieces[eated[0]]
                    if eated[0] == 'k':
                        depth = current_depth
                        if current_depth == 0:
                            return move
                elif piece[0] == 'k':
                    score -= value_pieces['n']
                
                new_sequence = current_sequence[1:] + current_sequence[0]
                
                if base_move is None:
                    start_move = possible_moves
                    queue.append((new_board, new_sequence, current_depth + 1, score, move))
                else:
                    queue.append((new_board, new_sequence, current_depth + 1, score, base_move))
                
                    if score > best_score:
                        best_score = score
                        best_move = [base_move]
                    if score == best_score:
                        best_move.append(base_move)
        else:
            worst_score = 0
            worst_board = None
            for move in possible_moves:
                new_board = current_board.copy()
                piece = new_board[move[0][0]][move[0][1]]
                eated = new_board[move[1][0]][move[1][1]]
                new_board[move[1][0]][move[1][1]] = new_board[move[0][0]][move[0][1]]
                new_board[move[0][0]][move[0][1]] = ''
                
                score = current_score
                if piece[0] == 'p':
                    score += value_pieces['n']
                    if move[1][0] == 0:
                        score += value_pieces['q']
                        new_board[move[1][0]][move[1][1]] = 'q' + piece[1]
                if eated != '':
                    score += value_pieces[eated[0]]
                    if eated[0] == 'k':
                        current_depth = depth
                        break
                elif piece[0] == 'k':
                    score -= value_pieces['n']
                
                
                if score > worst_score:
                    worst_score = score
                    worst_board = new_board
                if score == worst_score and np.random.rand() > 0.5:
                    worst_score = score
                    worst_board = new_board

            if worst_score == 0:
                worst_board = new_board
            new_sequence = current_sequence[1:] + current_sequence[0]
            queue.append((worst_board, new_sequence, current_depth + 1, current_score-worst_score, base_move))
            
    

    print(visite, len(visited), best_score, best_move)
    if best_score == 0:
        return start_move[np.random.randint(0,len(start_move))]
    else:
        return best_move[np.random.randint(0,len(best_move))]

def chess_bot_visited(player_sequence, board, time_budget, **kwargs):
    selected_piece, selected_move = visited_bfsMove(player_sequence, board, 5)
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


register_chess_bot("WrongBFSMove", chess_bot)
register_chess_bot("Test", chess_bot_test)
register_chess_bot("BFSMove", chess_bot_bfs)
register_chess_bot("visited BFSMove", chess_bot_visited)