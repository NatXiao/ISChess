def is_free(pos, board):
    return board[pos[0], pos[1]] == ''

def color_at(pos, board):
    return board[pos[0], pos[1]][1]

def can_move_or_capture(pos, board, player_color):
    return is_free(pos, board) or color_at(pos, board) != player_color


def check_boundary(pos, board):
    #   Check boundary condition
    if pos[0] < 0 or pos[0] >= board.shape[0] or \
       pos[1] < 0 or pos[1] >= board.shape[1] or \
       board[pos[0], pos[1]] == 'X':
       return False
    return True

def move_diagonal(pos, board, player_color):
    moves = []
    x = pos[0]+1
    y = pos[1]+1
    while True:
        if can_move_or_capture((x,y), board, player_color):
            moves.append((x,y))
        else:
            break
        x += 1
        y += 1
    x = pos[0]-1
    y = pos[1]-1
    while True:
        if can_move_or_capture((x,y), board, player_color):
            moves.append((x,y))
        else:
            break
        x -= 1
        y -= 1
    x = pos[0]+1
    y = pos[1]-1
    while True:
        if can_move_or_capture((x,y), board, player_color):
            moves.append((x,y))
        else:
            break
        x += 1
        y -= 1
    x = pos[0]-1
    y = pos[1]+1
    while True:
        if can_move_or_capture((x,y), board, player_color):
            moves.append((x,y))
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
        if can_move_or_capture((x,y), board, player_color):
            moves.append((x,y))
        else:
            break
        x += 1
    x = pos[0]-1
    while True:
        if can_move_or_capture((x,y), board, player_color):
            moves.append((x,y))
        else:
            break
        x -= 1
    x = pos[0]
    y = pos[1]+1
    while True:
        if can_move_or_capture((x,y), board, player_color):
            moves.append((x,y))
        else:
            break
        y += 1
    y = pos[1]-1
    while True:
        if can_move_or_capture((x,y), board, player_color):
            moves.append((x,y))
        else:
            break
        y -= 1
    return moves

def give_moves(pos, board):
    piece, player_color = board[pos[0], pos[1]]
    moves = []
    
    match piece:
        case 'p': # Pawn
            if is_free((pox[0]+1,pos[1]), board):
                moves.append((pox[0]+1,pos[1]))
            if color_at((pox[0]+1,pos[1]+1), board) != player_color:
                moves.append((pox[0]+1,pos[1]+1))
            if color_at((pox[0]+1,pos[1]-1), board) != player_color:
                moves.append((pox[0]+1,pos[1]-1))
            break
        case 'n':
            knight_moves = [
                (pos[0]+2, pos[1]+1), (pos[0]+2, pos[1]-1),
                (pos[0]-2, pos[1]+1), (pos[0]-2, pos[1]-1),
                (pos[0]+1, pos[1]+2), (pos[0]+1, pos[1]-2),
                (pos[0]-1, pos[1]+2), (pos[0]-1, pos[1]-2) 
            ]
            for m in knight_moves:
                if can_move_or_capture(m, board, player_color):
                    moves.append(m)
            break
        case 'b':
            moves = move_diagonal(pos, board, player_color)
            break
        case 'r':
            moves = move_axis(pos, board, player_color)
            break
        case 'q':
            moves.append(move_diagonal(pos, board, player_color))
            moves.append(move_axis(pos, board, player_color))
            break
        case 'k':
            king_moves = [
                (pos[0]+1, pos[1]), (pos[0]-1, pos[1]),
                (pos[0], pos[1]+1), (pos[0], pos[1]-1),
                (pos[0]+1, pos[1]+1), (pos[0]+1, pos[1]-1),
                (pos[0]-1, pos[1]+1), (pos[0]-1, pos[1]-1)
            ]
            for m in king_moves:
                if can_move_or_capture(m, board, player_color):
                    moves.append(m)
            break
    
    return moves
