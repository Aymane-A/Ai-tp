def minimax(node, depth, maximizingPlayer):
    if depth == 0 or is_terminal_node(node):
        return heuristic_value(node)
    if maximizingPlayer:
        value = -math.inf
        for child in get_children(node, 'X'):
            value = max(value, minimax(child, depth - 1, False))
    else:
        value = +math.inf
        for chuld in get_children(node, 'X'):
            value = min(value, minimax(child, depth -1, True))
    return value


# jeu TIC TAC TOE

def minimax(board, depth, is_maximizing):
    if is_game_over(board):
        return evaluate_board(board)
    
    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_0
                    score = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else :
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    score = minimax(board, depth+1, True)
                    board[i][j] = EMPTY
                    best_score = min(score, best_score)
        return best_score
    

#verifie l'etat finale du jeu
def is_game_over(board):
    for row in board:
        if row.count(row[0]) == 3 and row[0] != EMPTY:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return True
    if (board[0][0] == board[1][1] == board[2][2] != EMPTY) or (board[0][2] == board[1][1] == board[2][0] != EMPTY):
        return True
    if all(cell != EMPTY for row in board for cell in row ):
        return True
    return False


#calculer l'heuristique
def evaluate_board(board):
    for row in board:
        if row.count(PLAYER_0) == 3:
            return 1
        if row.count(PLAYER_X) == 3:
            return -1
    for col in range(3):
        if (board[0][col] == board[1][col] == board[2][col] ) and board[0][col] != EMPTY:
            return 1 if board[0][col] == PLAYER_0 else -1
    if (board[0][0] == board[1][1] == board[2][2] != EMPTY):
        return 1 if board[1][1] == PLAYER_0 else -1
    if (board[0][2] == board[1][1] == board[2][0] != EMPTY):
        return 1 if board[1][1] == PLAYER_0 else -1
    return 0


def find_best_move(board):
    best_score = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_0
                score = minimax(board, 0, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move



import math 

PLAYER_X = "X"
PLAYER_0= "O"
EMPTY = ' '

def print_board(board):
    for row in board:
        print("/".join(row))
        print("-"*5)


#fonction principale
def main():
    board = [[EMPTY] *3 for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while not is_game_over(board):
        # Player X's turn
        while True:
            try:
                x, y = map(int, input("Enter your move (row, column").split())
                if board[x][y] == EMPTY:
                    board[x][y] = PLAYER_X
                    break
                else :
                    print("Cell already occupied! Try again.")
            except (ValueError, IndexError):
                print("Invalid input! Enter row and column as two numbers (0, 1, or 2).")

        print_board(board)

        if is_game_over(board):
            break
        
        # Computer's turn 
        print("Computer's turn: ")
        move = find_best_move(board)
        if move != (-1, -1):
            board[move[0]][move[1]] = PLAYER_0
            print_board(board)
    
        if is_game_over(board):
            if evaluate_board(board) == 1:
                print("Computer (O) wins!")
            elif evaluate_board(board) == -1:
                print("You (X) wins!")
            else:
                print("It's a draw!")
            

if __name__ == "__main__":
    main()
