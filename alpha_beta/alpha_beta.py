import numpy as np
from numpy.typing import NDArray

class AlphaBeta:

    __rows = 6
    __cols = 7
    __winning_len = 4

    def __init__(self) -> None:
        self.board = self._create_board()

    @property
    def rows(self) -> int:
        return self.__rows
    
    @rows.setter
    def rows(self, rows: int):
        self.__rows = rows

    @property
    def cols(self) -> int:
        return self.__cols
    
    @cols.setter
    def cols(self, cols: int):
        self.__cols = cols

    @property
    def winning_len(self) -> int:
        return self.__winning_len
    
    @winning_len.setter
    def winning_len(self, winning_len: int):
        self.__winning_len = winning_len

    def _create_board(self) -> NDArray:
        # СОздание пустого поля
        return np.zeros((self.rows, self.cols))
    
    def print_board(self) -> None:
        # Вывод поля
        tags = [i for i in range(1, self.cols)]
        print(np.flip(self.board, 0))
        print(" ", tags)

    def is_valid_location(self, board: NDArray, col: int) -> bool:
        # Поверка, заполнена ли колонка
        return board[self.rows - 1][col] == 0

    def get_next_open_row(self, board: NDArray, col: int) -> int:
        # Определение места заполнения
        for r in range(self.rows):
            if board[r][col] == 0:
                return r

    def drop_piece(self, board: NDArray, row: int, col: int, piece: int) -> None:
        # Присвоение клекти поля значения
        board[row][col] = piece

    def winning_move(self, board: NDArray, piece: int) -> bool:
        # Проверка горизонтальных, вертикальных и диагональных побед
        for c in range(self.cols - 3):
            for r in range(self.rows):
                if all(board[r][c+i] == piece for i in range(self.winning_len)):
                    return True

        for c in range(self.cols):
            for r in range(self.rows - 3):
                if all(board[r+i][c] == piece for i in range(self.winning_len)):
                    return True

        for c in range(self.cols - 3):
            for r in range(self.rows - 3):
                if all(board[r+i][c+i] == piece for i in range(self.winning_len)):
                    return True

        for c in range(self.cols - 3):
            for r in range(3, self.rows):
                if all(board[r-i][c+i] == piece for i in range(self.winning_len)):
                    return True

        return False

    def _evaluate_window(self, window: list, piece: int):
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

    def _score_position(self, board: NDArray, piece: int) -> int:
        score = 0
        
        # Оценка горизонтальных окна
        for r in range(self.rows):
            row_array = [int(i) for i in list(board[r])]
            for c in range(self.cols - 3):
                window = row_array[c:c + self.winning_len]
                score += self._evaluate_window(window, piece)

        # Оценка вертикальных окна
        for c in range(self.cols):
            col_array = [int(board[r][c]) for r in range(self.rows)]
            for r in range(self.rows - 3):
                window = col_array[r:r + self.winning_len]
                score += self._evaluate_window(window, piece)

        # Оценка диагональных окна (слева направо)
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [board[r + i][c + i] for i in range(self.winning_len)]
                score += self._evaluate_window(window, piece)

        # Оценка диагональных окна (справа налево)
        for r in range(self.rows - 3):
            for c in range(3, self.cols):
                window = [board[r + i][c - i] for i in range(self.winning_len)]
                score += self._evaluate_window(window, piece)

        return score

    def alpha_beta(
            self,
            board: NDArray, 
            depth: int, 
            alpha: float = float('-inf'), 
            beta: float = float('inf'), 
            maximizing_player: bool = False
        ) -> list[int, int]:
        valid_locations = [c for c in range(self.cols) if self.is_valid_location(board, c)]
        
        is_stop = self.winning_move(board, 1) or self.winning_move(board, 2) or len(valid_locations) == 0
        
        if depth == 0 or is_stop:
            if is_stop:
                if self.winning_move(board, 1):
                    return (None, float('inf'))
                elif self.winning_move(board, 2):
                    return (None, float('-inf'))
                else: 
                    return (None, 0)
            else:
                return (None, self._score_position(board, 1))

        if maximizing_player:
            value = float('-inf')
            column = valid_locations[0]
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                temp_board = board.copy()
                self.drop_piece(temp_board, row, col, 1)
                new_score = self.alpha_beta(temp_board, depth-1, alpha, beta, False)[1]
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
                row = self.get_next_open_row(board, col)
                temp_board = board.copy()
                self.drop_piece(temp_board, row, col, 2)
                new_score = self.alpha_beta(temp_board, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return column, value
        
    def check_winning_move(self, board: NDArray):
        valid_locations = [c for c in range(self.cols) if self.is_valid_location(board, c)]

        block = -1
        # Проверка на выигрышный ход для компьютера или игрока
        for col in valid_locations:
            row = self.get_next_open_row(board, col)

            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, 2)
            if self.winning_move(temp_board, 2):
                return col
            
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, 1)
            if self.winning_move(temp_board, 1):
                block = col

        return block

