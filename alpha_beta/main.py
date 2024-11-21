import pygame
from alpha_beta import AlphaBeta

# Константы
WIDTH = 700
HEIGHT = 700
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
CHIP_RADIUS = RADIUS - 4

# Цвета
FIELD = (131, 84, 31)
BG = (183, 235, 247)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4 в ряд")


def draw_board(board, cols: int, rows: int):
    # Отрисовка поля
    for c in range(cols):
        for r in range(rows):
            pygame.draw.rect(screen, FIELD, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BG, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    for c in range(cols):
        for r in range(rows):
            if board[r][c] == 1:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), CHIP_RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), CHIP_RADIUS)


def display_winner(player: int):
    # Отображение сообщения о победителе
    text = ""
    if player == 2:
        text = "Игрок"
    else: 
        text = "Компьютер"
    font = pygame.font.SysFont("monospace", 75)
    font.set_bold(True)
    label = font.render(text, True, BLACK)
    screen.blit(label, (WIDTH // 6, HEIGHT // 3))
    label1 = font.render("победил!", True, BLACK)
    screen.blit(label1, (WIDTH // 6, HEIGHT // 2))


def play_game(depth: int):
    ab = AlphaBeta()
    game_over = False
    is_break = False
    turn = 0

    pygame.draw.rect(screen, BG, (0, 0, WIDTH, SQUARESIZE))

    while not game_over:
        draw_board(ab.board, ab.cols, ab.rows)
        pygame.display.update()

        if turn == 1:
            col, _ = ab.alpha_beta(ab.board, depth=depth)
            if ab.is_valid_location(ab.board, col):
                row = ab.get_next_open_row(ab.board, col)
                ab.drop_piece(ab.board, row, col, 2)

                if ab.winning_move(ab.board, 2):
                    print("Компьютер выиграл!")
                    game_over = True

                turn += 1
                turn %= 2
        
        if turn == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    is_break = True

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BG, (0, 0, WIDTH, SQUARESIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BG, (0, 0, WIDTH, SQUARESIZE))
                    # Позиция курсора мыши
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)

                    if ab.is_valid_location(ab.board, col):
                        row = ab.get_next_open_row(ab.board, col)
                        ab.drop_piece(ab.board, row, col, 1)

                        if ab.winning_move(ab.board, 1):
                            print("Игрок выиграл!")
                            game_over = True

                        turn += 1
                        turn %= 2
            
        if game_over:
            draw_board(ab.board, ab.cols, ab.rows)
            display_winner(turn + 1)
            pygame.display.update()

            while not is_break:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_break = True

if __name__ == "__main__":
    depth = 6
    play_game(depth)