import numpy as np
from numpy.typing import NDArray

ROWS = 6
COLS = 7
WINNING_LENGTH = 4

def create_board() -> NDArray:
    # СОздание пустого поля
    return np.zeros((ROWS, COLS))

def is_valid_location(board: NDArray, col: int):
    # Поверка, заполнена ли колонка
    return board[ROWS - 1][col] == 0

def get_next_open_row(board: NDArray, col: int):
    # Определение места заполнения
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def drop_piece(board: NDArray, row: int, col: int, piece: int):
    # Присвоение клекти поля значения
    board[row][col] = piece

def winning_move(board: NDArray, piece: int):
    # Проверка горизонтальных, вертикальных и диагональных побед
    for c in range(COLS - 3):
        for r in range(ROWS):
            if all(board[r][c+i] == piece for i in range(WINNING_LENGTH)):
                return True

    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(WINNING_LENGTH)):
                return True

    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == piece for i in range(WINNING_LENGTH)):
                return True

    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == piece for i in range(WINNING_LENGTH)):
                return True

    return False

def evaluate_window(window: list, piece: int):
    # Оценка окна
    score = 0
    opponent_piece = 2 if piece == 1 else 1
    if window.count(piece) == 4:
        score += 10000
    elif window.count(piece) == 3 and window.count(0) >= 1:
        score += 500
    elif window.count(piece) == 2 and window.count(0) >= 2:
        score += 10
    elif window.count(piece) == 1 and window.count(0) >= 3:
        score += 1
    if window.count(opponent_piece) == 3 and window.count(0) >= 1:
        score -= 1000
    return score

def score_position(board: NDArray, piece: int):
    score = 0
    
    # Оценка горизонтальных окна
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r])]
        for c in range(COLS - 3):
            window = row_array[c:c + WINNING_LENGTH]
            score += evaluate_window(window, piece)

    # Оценка вертикальных окна
    for c in range(COLS):
        col_array = [int(board[r][c]) for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINNING_LENGTH]
            score += evaluate_window(window, piece)

    # Оценка диагональных окна (слева направо)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r + i][c + i] for i in range(WINNING_LENGTH)]
            score += evaluate_window(window, piece)

    # Оценка диагональных окна (справа налево)
    for r in range(ROWS - 3):
        for c in range(3, COLS):
            window = [board[r + i][c - i] for i in range(WINNING_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def alpha_beta(
        board: NDArray, 
        depth: int, 
        alpha: float, 
        beta: float, 
        maximizing_player: bool
    ) -> list[int, int]:
    valid_locations = [c for c in range(COLS) if is_valid_location(board, c)]
    
    is_stop = winning_move(board, 1) or winning_move(board, 2) or len(valid_locations) == 0
    
    if depth == 0 or is_stop:
        if is_stop:
            if winning_move(board, 1):
                return (None, float('inf'))
            elif winning_move(board, 2):
                return (None, float('-inf'))
            else: 
                return (None, 0)
        else:
            return (None, score_position(board, 1))

    if maximizing_player:
        value = float('-inf')
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 1)
            new_score = alpha_beta(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return column, value
    
    else: 
        value = float('inf')
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 2)
            new_score = alpha_beta(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if beta <= alpha:
                break
        return column, value

def print_board(board):
    # Вывод поля
    tags = [1, 2, 3, 4, 5, 6, 7]
    print(np.flip(board, 0))
    print(" ", tags)

def play_game(depth):
    board = create_board()
    game_over = False
    
    while not game_over:
        # Ход игрока (человека)
        while True: 
            print_board(board)
            try:
                col = int(input("Игрок, выберите колонку (1-7): "))
                col -= 1
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    break
                else:
                    print("Недопустимый ход. Попробуйте еще раз.")
                    
            except:
                print("Пожалуйста введите число от 1 до 7.")

        if winning_move(board, 1):
            print_board(board)
            print("Игрок выиграл!")
            game_over = True
            break
        
        # Ход компьютера
        while True: 
            print("Компьютер делает ход...")
            col, score = alpha_beta(board, depth=depth, alpha=float('-inf'), beta=float('inf'), maximizing_player=False)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                print("Компьютер сходил в колонку:", col+1)
                break
        
        if winning_move(board, 2):
            print_board(board)
            print("Компьютер выиграл!")
            game_over = True 
            break

if __name__ == "__main__":
    depth = 6
    play_game(depth)