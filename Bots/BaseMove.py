def is_free(pos, board):
    """
    Check if the position is free on the board
    @pos: position to check
    @board: board to check on
    @return: True if the position is free, False otherwise
    """
    return board[pos[0], pos[1]] == ''

def is_enemy(pos, board, player_color):
    """
    Check if the position is occupied by an enemy piece
    @pos: position to check
    @board: board to check on
    @player_color: list of color allied
    @return: True if the position is nemesis, False otherwise
    """
    target = board[pos[0], pos[1]]
    if target == '':
        return False
    return target[1] not in player_color

def check_boundary(pos, board):
    """
    Check if the position is into the board
    @pos: position to check
    @board: board to check on
    @return: True if the position is in the board, False otherwise
    """
    if pos[0] < 0 or pos[0] >= board.shape[0] or \
       pos[1] < 0 or pos[1] >= board.shape[1] or \
       board[pos[0], pos[1]] == 'X':
       return False
    return True

def can_move_or_capture(pos, board, player_color):
    """
    Check if the position is occupied by an enemy piece
    @pos: position to check
    @board: board to check on
    @player_color: list of color allied
    @return: True if we can move or capture the position, False otherwise
    """
    if check_boundary(pos, board):
        return is_free(pos, board) or is_enemy(pos, board, player_color)
    else:
        return False

def move_diagonal(pos, board, player_color):
    """
    Give the move in diagonal possible from a position
    @pos: starting position
    @board: board to check on
    @player_color: list of color allied
    @return: list of possible move
    """
    moves = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy
        while check_boundary((x, y), board):
            if is_free((x, y), board):
                moves.append((x, y))
            elif is_enemy((x, y), board, player_color):
                moves.append((x, y))
                break
            else:
                break
            x += dx
            y += dy
    
    return moves

def move_axis(pos, board, player_color):
    """
    Give the move in axis possible from a position
    @pos: starting position
    @board: board to check on
    @player_color: list of color allied
    @return: list of possible move
    """
    moves = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy
        while check_boundary((x, y), board):
            if is_free((x, y), board):
                moves.append((x, y))
            elif is_enemy((x, y), board, player_color):
                moves.append((x, y))
                break
            else:
                break
            x += dx
            y += dy
    
    return moves

def pawn_moves(pos, board, player_color, advance=(1, 0)):
    """
    Give the possible moves for a pawn at a position
    @pos: starting position
    @board: board to check on
    @player_color: list of allied colors
    @advance: direction of the pawn advance
    @return: list of possible moves
    """
    moves = []

    # Move when pawn can eat
    eating = [(1, 1), (-1, -1)]
    for dx, dy in eating:
        d = (pos[0] + advance[0] + dx * advance[1], pos[1] + advance[1] + dy * advance[0])
        if check_boundary(d, board):
            if is_enemy(d, board, player_color):
                moves.append(d)
    
    # Move when pawn advance
    d = (pos[0]+advance[0], pos[1]+advance[1])
    if check_boundary(d, board):
        if is_free(d, board):
            moves.append(d)

    return moves


def knight_moves(pos, board, player_color):
    """
    Give the move of a knight at a position
    @pos: starting position
    @board: board to check on
    @player_color: list of color allied
    @return: list of possible move
    """
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
    """
    Give the move of a king at a position
    @pos: starting position
    @board: board to check on
    @player_color: list of color allied
    @return: list of possible move
    """
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

def give_moves(pos, board, advance=(1, 0), player_color=None):
    """
    Give moves according to a piece at a position given
    @pos: starting position
    @board: board to check on
    @advance: direction of the pawn advance
    @player_color: list of color allied
    @return: list of possible move
    """

    if player_color is None:
        piece, player_color = board[pos[0], pos[1]]
        player_color = [player_color]
    else:
        piece, _ = board[pos[0], pos[1]]
    moves = []
    
    match piece:
        case 'p': # Pawn
            moves = pawn_moves(pos, board, player_color, advance)
        case 'n': # Knight
            moves = knight_moves(pos, board, player_color)
        case 'b': # Bishop
            moves = move_diagonal(pos, board, player_color)
        case 'r': # Rock
            moves = move_axis(pos, board, player_color)
        case 'q': # Queen
            moves += move_diagonal(pos, board, player_color)
            moves += move_axis(pos, board, player_color)
        case 'k': # King
            moves = king_moves(pos, board, player_color)
    
    return moves
    
def give_eating_moves(pos, board, advance=(1, 0), player_color=None):
    """
    Give moves according to a piece at a position given
    @pos: starting position
    @board: board to check on
    @advance: direction of the pawn advance
    @player_color: list of color allied
    @return: list of possible move
    """
    
    if player_color is None:
        piece, player_color = board[pos[0], pos[1]]
        player_color = [player_color]
    else:
        piece, _ = board[pos[0], pos[1]]
    moves = []
    
    match piece:
        case 'p': # Pawn
            moves = pawn_moves(pos, board, player_color, advance)
        case 'n': # Knight
            moves = knight_moves(pos, board, player_color)
        case 'b': # Bishop
            moves = move_diagonal(pos, board, player_color)
        case 'r': # Rock
            moves = move_axis(pos, board, player_color)
        case 'q': # Queen
            moves += move_diagonal(pos, board, player_color)
            moves += move_axis(pos, board, player_color)
        case 'k': # King
            moves = king_moves(pos, board, player_color)
    
    eating_moves = []
    for move in moves:
        if is_enemy(move, board, player_color):
            eating_moves.append(move)
    
    if not eating_moves:
        return moves
    return eating_moves