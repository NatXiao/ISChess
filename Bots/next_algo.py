
from Bots.ChessBotList import register_chess_bot
from Bots.BaseMove import *
from Bots.BaseStrategy import *
from Bots.chessbot import *
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

def next_algo(player_sequence, board, depth):
    """
    [test]
    Better algorithm
    @player_sequence: sequence of the game
    @board: chess board
    @depth: depth of the BFS
    @return: tuple move with piece position and piece new position
    """
    visite = 0
    
    # To know who is playing
    color = player_sequence[1]
    player_sequence = player_sequence[1] + player_sequence[4]
    # (current board, player sequence, current depth, score, move)
    queue = [(board, player_sequence, 0, 0, None)]
    queue.append((board, player_sequence[1:] + player_sequence[0], 1, 0, None))
    
    visited = {}
    best_move = []
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
                score = 0
                if piece[0] == 'p':
                    if move[1][0] == 7:
                        score += value_pieces['q']
                        new_board[move[1][0]][move[1][1]] = 'q' + piece[1]
                if eated != '':
                    score += value_pieces[eated[0]]
                    if eated[0] == 'k':
                        if current_depth <= 1:
                            return move
                        depth = current_depth + 2 if current_depth + 2 <= depth else depth
                if check_check(move[1], new_board, advance):
                    score += value_pieces['n']
                score //= (current_depth + 1)
                score += current_score

                
                # Put in queue
                if base_move is None and current_depth == 0:
                    start_move = possible_moves
                    queue.append((new_board, new_sequence, current_depth + 1, score, move))
                else:
                    queue.append((new_board, new_sequence, current_depth + 1, score, base_move))
                
                    # Keep best moves
                    if score > best_score:
                        best_score = score
                        best_move = [base_move]
                    if score == best_score:
                        best_move.append(base_move)
        else:
            worst_score = 0
            worst_move = []
            king_eat = False
            # Check all possible enemy move
            for move in possible_moves:
                new_board, piece, eated = create_board(move,board)
                
                # Compute ennemy score
                score = 0
                if piece[0] == 'p':
                    if move[1][0] == 0:
                        score += value_pieces['q']
                        new_board[move[1][0]][move[1][1]] = 'q' + piece[1]
                if eated != '':
                    score += value_pieces[eated[0]]
                    if eated[0] == 'k':
                        king_eat = True
                        break
                if check_check(move[1], new_board, advance):
                    score += value_pieces['n']
                score //= (current_depth + 1)
                
                # Keep best enemy move
                if score > worst_score:
                    worst_score = score
                    worst_move = [move]
                if score == worst_score:
                    worst_score = score
                    worst_move.append(move)

            if not king_eat:
                # Creat best enemy board
                if worst_score == 0:
                    worst_move = possible_moves
                
                move = worst_move[np.random.randint(0,len(worst_move))]
                
                new_board, piece, eated = create_board(move, board)

                # Put best enemy move in queue
                queue.append((new_board, new_sequence, current_depth + 1, current_score-worst_score, base_move))
            
    # Select move to play
    print("Algo visited: ", visite, " but truly visited: ", len(visited), best_score)
    if best_score == 0:
        return start_move[np.random.randint(0,len(start_move))]
    else:
        selected = best_move[np.random.randint(0,len(best_move))]
        if selected:
            return selected
        time.sleep(10)
        return

def chess_bot_scored(player_sequence, board, time_budget, **kwargs):
    """
    Chess bot to launch BFS with score and visited update
    @player_sequence: sequence of the game
    @board: chess board
    @time_budget: time allowed to run the algorithm
    @return: move with selected piece position and piece new position
    """
    start = time.time()
    selected_piece, selected_move = next_algo(player_sequence, board, 5)
    print("Algo Time   : ", time.time()-start)
    return selected_piece, selected_move

register_chess_bot("Next Algo", chess_bot_scored)