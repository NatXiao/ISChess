def is_free(pos, board):
    return board[pos[0], pos[1]] == ''

def is_ennemy(pos, board, player_color):
    target = board[pos[0], pos[1]]
    if target == '':
        return False
    return target[1] != player_color

def check_boundary(pos, board):
    #   Check boundary condition
    if pos[0] < 0 or pos[0] >= board.shape[0] or \
       pos[1] < 0 or pos[1] >= board.shape[1] or \
       board[pos[0], pos[1]] == 'X':
       return False
    return True

def can_move_or_capture(pos, board, player_color):
    if check_boundary(pos, board):
        return is_free(pos, board) or is_ennemy(pos, board, player_color)
    else:
        return False

def move_diagonal(pos, board, player_color):
    moves = []
    x = pos[0]+1
    y = pos[1]+1
    while True:
        if check_boundary((x,y), board):
            if is_free((x,y), board):
                moves.append((x,y))
            elif is_ennemy((x,y), board, player_color):
                moves.append((x,y))
                break
            else:
                break
        else:
            break
        x += 1
        y += 1
    x = pos[0]-1
    y = pos[1]-1
    while True:
        if check_boundary((x,y), board):
            if is_free((x,y), board):
                moves.append((x,y))
            elif is_ennemy((x,y), board, player_color):
                moves.append((x,y))
                break
            else:
                break
        else:
            break
        x -= 1
        y -= 1
    x = pos[0]+1
    y = pos[1]-1
    while True:
        if check_boundary((x,y), board):
            if is_free((x,y), board):
                moves.append((x,y))
            elif is_ennemy((x,y), board, player_color):
                moves.append((x,y))
                break
            else:
                break
        else:
            break
        x += 1
        y -= 1
    x = pos[0]-1
    y = pos[1]+1
    while True:
        if check_boundary((x,y), board):
            if is_free((x,y), board):
                moves.append((x,y))
            elif is_ennemy((x,y), board, player_color):
                moves.append((x,y))
                break
            else:
                break
        else:
            break
        x -= 1
        y += 1
    return moves
    
def move_axis(pos, board, player_color):
    moves = []
    x = pos[0]+1
    y = pos[1]
    while True:
        if check_boundary((x,y), board):
            if is_free((x,y), board):
                moves.append((x,y))
            elif is_ennemy((x,y), board, player_color):
                moves.append((x,y))
                break
            else:
                break
        else:
            break
        x += 1
    x = pos[0]-1
    while True:
        if check_boundary((x,y), board):
            if is_free((x,y), board):
                moves.append((x,y))
            elif is_ennemy((x,y), board, player_color):
                moves.append((x,y))
                break
            else:
                break
        else:
            break
        x -= 1
    x = pos[0]
    y = pos[1]+1
    while True:
        if check_boundary((x,y), board):
            if is_free((x,y), board):
                moves.append((x,y))
            elif is_ennemy((x,y), board, player_color):
                moves.append((x,y))
                break
            else:
                break
        else:
            break
        y += 1
    y = pos[1]-1
    while True:
        if check_boundary((x,y), board):
            if is_free((x,y), board):
                moves.append((x,y))
            elif is_ennemy((x,y), board, player_color):
                moves.append((x,y))
                break
            else:
                break
        else:
            break
        y -= 1
    return moves

def pawn_moves(pos, board, player_color):
    moves = []
    if is_free((pos[0]+1,pos[1]), board):
        moves.append((pos[0]+1,pos[1]))
    d = (pos[0]+1,pos[1]+1)
    if check_boundary(d, board):
        if is_ennemy(d, board, player_color):
            moves.append(d)
    d = (pos[0]+1,pos[1]-1)
    if check_boundary(d, board):
        if is_ennemy(d, board, player_color):
            moves.append(d)
    return moves

def knight_moves(pos, board, player_color):
    possible_moves = [
        (pos[0]+2, pos[1]+1), (pos[0]+2, pos[1]-1),
        (pos[0]-2, pos[1]+1), (pos[0]-2, pos[1]-1),
        (pos[0]+1, pos[1]+2), (pos[0]+1, pos[1]-2),
        (pos[0]-1, pos[1]+2), (pos[0]-1, pos[1]-2) 
    ]
    moves = []
    for m in possible_moves:
        if can_move_or_capture(m, board, player_color):
            moves.append(m)
    return moves

def king_moves(pos, board, player_color):
    possible_moves = [
        (pos[0]+1, pos[1]), (pos[0]-1, pos[1]),
        (pos[0], pos[1]+1), (pos[0], pos[1]-1),
        (pos[0]+1, pos[1]+1), (pos[0]+1, pos[1]-1),
        (pos[0]-1, pos[1]+1), (pos[0]-1, pos[1]-1)
    ]
    moves = []
    for m in possible_moves:
        if can_move_or_capture(m, board, player_color):
            moves.append(m)
    return moves

def give_moves(pos, board):
    piece, player_color = board[pos[0], pos[1]]
    moves = []
    
    match piece:
        case 'p': # Pawn
            moves = pawn_moves(pos, board, player_color)
        case 'n':
            moves = knight_moves(pos, board, player_color)
        case 'b':
            moves = move_diagonal(pos, board, player_color)
        case 'r':
            moves = move_axis(pos, board, player_color)
        case 'q':
            moves += move_diagonal(pos, board, player_color)
            moves += move_axis(pos, board, player_color)
        case 'k':
            moves = king_moves(pos, board, player_color)
    
    return moves
    
def give_eating_moves(pos, board):
    piece, player_color = board[pos[0], pos[1]]
    moves = []
    
    match piece:
        case 'p': # Pawn
            moves = pawn_moves(pos, board, player_color)
        case 'n':
            moves = knight_moves(pos, board, player_color)
        case 'b':
            moves = move_diagonal(pos, board, player_color)
        case 'r':
            moves = move_axis(pos, board, player_color)
        case 'q':
            moves += move_diagonal(pos, board, player_color)
            moves += move_axis(pos, board, player_color)
        case 'k':
            moves = king_moves(pos, board, player_color)
    
    eating_moves = []
    for move in moves:
        if is_ennemy(move, board, player_color):
            eating_moves.append(move)
    
    if not eating_moves:
        return moves
    return eating_moves