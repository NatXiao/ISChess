from Bots.BaseMove import *
from Bots.chessbot import *
from Bots.BaseStrategy import *
import time

# Value given to the pieces
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

DFS_visited = 0
def recursive(player_sequence, board, our_color, depth, current_score = 0):
    """
    Recursive approach DFS
    @player_sequence: sequence of the game
    @board: chess board
    @our_color: color of the player who should play
    @depth: depth of the BFS
    @return: tuple move with piece position and piece new position
    """
    global DFS_visited; DFS_visited += 1

    # To know who is playing
    color = player_sequence[1]
    new_sequence = player_sequence[3:] + player_sequence[:3]

    # Extract possible move
    player_pieces = give_pieces(color, board)
    moves = []
    for p in player_pieces:
        moves += [[p, m] for m in give_moves(p, board)]
    
    best_score = current_score
    best_move = moves[0]
    
    # Check player if is real turn player or enemy
    if color == our_color:
        for move in moves:
            score = 0
            p = board[move[1]]
            if p != '':
                score += value_pieces[p[0]]
            if depth != 0:
                new_board, _, _ = create_board(move, board)
                score, _, _ = recursive(new_sequence, new_board[::-1], depth-1, current_score+score)
            
            if score > best_score:
                best_score = score
                best_move = move
    else:
        for move in moves:
            score = 0
            p = board[move[1]]
            if p != '':
                score -= value_pieces[p[0]]
            if depth != 0:
                new_board, _, _ = create_board(move, board)
                score, _, _ = recursive(new_sequence, new_board, depth-1, current_score-score)
            
            if score > best_score:
                best_score = score
                best_move = move
                
    return (best_score, best_move[0], best_move[1])

def bfsMove(player_sequence, board, depth):
    """
    BFS naive
    @player_sequence: sequence of the game
    @board: chess board
    @our_color: color of the player who should play
    @depth: depth of the BFS
    @return: tuple move with piece position and piece new position
    """
    visited = 0

    # To know who is playing
    color = player_sequence[1]
    player_sequence = player_sequence[1] + player_sequence[4]

    # (current board, player sequence, current depth, move)
    queue = [(board, player_sequence, 0, None)]
    
    best_move = []
    start_move = []
    
    while queue:
        current_board, current_sequence, current_depth, base_move = queue.pop(0)
        visited += 1
        if current_depth >= depth:
            continue
        
        # Generate all possible moves for the current player
        player_pieces = give_pieces(current_sequence[0], current_board)
        
        if current_sequence[0] == color:
            advance = (1,0)
        else:
            advance = (-1,0)
        
        possible_moves = []
        for p in player_pieces:
            possible_moves += [(p, m) for m in give_moves(p, current_board, advance=advance)]
        
        # Check all possible move
        new_sequence = current_sequence[1:] + current_sequence[0]
        for move in possible_moves:
            # Creat new board
            new_board, _, eated = create_board(move, board)
            
            # Check if king is eated
            if eated != '':
                if eated[0] == 'k' and current_depth <= depth:
                    depth = current_depth
                    if eated[1] != color:
                        best_move.append(move)
            
            # Put in queue
            if current_depth == 0:
                queue.append((new_board, new_sequence, current_depth + 1, move))
                start_move = possible_moves
            else:
                queue.append((new_board, new_sequence, current_depth + 1, base_move))
            
    # Select move to play
    print("BFS Visited: ", visited)
    if not best_move:
        return start_move[np.random.randint(0,len(start_move))]
    else:
        selected = best_move[np.random.randint(0,len(best_move))]
        if selected:
            return selected
        time.sleep(10)
        return

def visited_bfsMove(player_sequence, board, depth):
    """
    BFS with heuristic and visited update
    @player_sequence: sequence of the game
    @board: chess board
    @our_color: color of the player who should play
    @depth: depth of the BFS
    @return: tuple move with piece position and piece new position
    """
    visite = 0

    # To know who is playing
    color = player_sequence[1]
    player_sequence = player_sequence[1] + player_sequence[4]

    # (current board, player sequence, current depth, score, move)
    queue = [(board, player_sequence, 0, 0, None)]

    visited = {}
    best_move = []
    start_move = None
    best_score = 0
    
    while queue:
        current_board, current_sequence, current_depth, current_score, base_move = queue.pop(0)
        visite += 1
        if current_depth >= depth:
            continue
        
        # Store visited node
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
        
        if current_sequence[0] == color:
            advance = (1,0)
        else:
            advance = (-1,0)

        possible_moves = []
        for p in player_pieces:
            possible_moves += [(p, m) for m in give_moves(p, current_board, advance=advance)]
        
        
        # Separate according to real player turn
        new_sequence = current_sequence[1:] + current_sequence[0]
        if color == current_sequence[0]:

            #Check all possible move
            for move in possible_moves:
                # Create new board
                new_board, piece, eated = create_board(move, board)
                
                # Compute score
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
                
                # Put in queue
                if current_depth == 0:
                    queue.append((new_board, new_sequence, current_depth + 1, current_score+score, move))
                    start_move = possible_moves
                else:
                    queue.append((new_board, new_sequence, current_depth + 1, current_score+score, base_move))

                    # Keep best moves
                    if score > best_score:
                        best_score = score
                        best_move = [base_move]
                    if score == best_score:
                        best_move.append(base_move)
        else:
            worst_score = 0
            worst_move = []
            # Check all possible enemy move
            for move in possible_moves:
                # Creat new board
                new_board, piece, eated = create_board(move, board)
                
                # Compute ennemy score
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
                
                # Keep best enemy move
                if score > worst_score:
                    worst_score = score
                    worst_move = [move]
                if score == worst_score:
                    worst_score = score
                    worst_move.append(move)

            # Creat best enemy board
            if worst_score == 0:
                worst_move = possible_moves
            
            move = worst_move[np.random.randint(0,len(worst_move))]
            
            new_board, _, _ = create_board(move, board)

            # Put best enemy move in queue
            queue.append((new_board, new_sequence, current_depth + 1, current_score-worst_score, base_move))
            
    

    # Select move to play
    print("BFS+ visited: ", visite, " but truly visited: ", len(visited), best_score)
    if best_score == 0:
        return start_move[np.random.randint(0,len(start_move))]
    else:
        selected = best_move[np.random.randint(0,len(best_move))]
        if selected:
            return selected
        time.sleep(10)
        return


def chess_bot_wrong(player_sequence, board, time_budget, **kwargs):
    """
    Chess bot to launch wrong BFS -> recursive
    @player_sequence: sequence of the game
    @board: chess board
    @time_budget: time allowed to run the algorithm
    @return: move with selected piece position and piece new position
    """
    global DFS_visited; DFS_visited = 0
    start = time.time()
    color = player_sequence[1]
    _, selected_piece, selected_move = recursive(player_sequence, board, color, 5)
    print("DFS Visited: ", DFS_visited)
    print("DFS Time   : ", time.time()-start)
    return selected_piece, selected_move

def chess_bot_bfs(player_sequence, board, time_budget, **kwargs):
    """
    Chess bot to launch naive BFS
    @player_sequence: sequence of the game
    @board: chess board
    @time_budget: time allowed to run the algorithm
    @return: move with selected piece position and piece new position
    """
    start = time.time()
    selected_piece, selected_move = bfsMove(player_sequence, board, 2)
    print("BFS Time   : ", time.time()-start)
    return selected_piece, selected_move

def chess_bot_bfsUP(player_sequence, board, time_budget, **kwargs):
    """
    Chess bot to launch BFS with score and visited update
    @player_sequence: sequence of the game
    @board: chess board
    @time_budget: time allowed to run the algorithm
    @return: move with selected piece position and piece new position
    """
    start = time.time()
    selected_piece, selected_move = visited_bfsMove(player_sequence, board, 5)
    print("BFS Time   : ", time.time()-start)
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
register_chess_bot("Recursive", chess_bot_wrong)
register_chess_bot("BFSMove", chess_bot_bfs)
register_chess_bot("updated BFSMove", chess_bot_bfsUP)