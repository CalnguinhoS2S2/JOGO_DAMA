import asyncio
import pygame
from constants import *
from board import Board

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo de Damas')
pygame.font.init()
font = pygame.font.SysFont('arial', 30)

def draw_score(board):
    red_count = sum(1 for row in board.board for piece in row if piece != 0 and piece.color == RED)
    black_count = sum(1 for row in board.board for piece in row if piece != 0 and piece.color == BLACK)

    red_text = font.render(f'Vermelho: {red_count}', True, RED)
    black_text = font.render(f'Preto: {black_count}', True, BLACK)

    WIN.blit(red_text, (10, HEIGHT - 35))
    WIN.blit(black_text, (WIDTH - black_text.get_width() - 10, HEIGHT - 35))

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def menu():
    run = True
    while run:
        WIN.fill(BEIGE)
        title = font.render("Jogo de Damas", True, BLACK)
        play = font.render("Clique para Jogar", True, RED)

        WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))
        WIN.blit(play, (WIDTH//2 - play.get_width()//2, HEIGHT//2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

async def main_async():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    valid_moves = []
    selected_piece = None
    turno = BLACK
    forcando_captura = False

    while run:
        clock.tick(FPS)
        board.draw(WIN)
        board.draw_valid_moves(WIN, valid_moves)
        draw_score(board)
        pygame.display.update()

        winner = board.check_winner()
        if winner:
            print("Vitória de:", "PRETO" if winner == BLACK else "VERMELHO")
            await asyncio.sleep(2)
            run = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                piece = board.get_piece(row, col)

                if selected_piece:
                    if board.valid_move(selected_piece, row, col):
                        old_row = selected_piece.row
                        old_col = selected_piece.col

                        board.move_piece(selected_piece, row, col)
                        was_capture = abs(row - old_row) == 2 and abs(col - old_col) == 2

                        if was_capture and board.has_capture(selected_piece):
                            valid_moves = board.get_valid_moves(selected_piece)
                            forcando_captura = True
                        else:
                            selected_piece = None
                            valid_moves = []
                            forcando_captura = False
                            turno = RED if turno == BLACK else BLACK
                    else:
                        if not forcando_captura:
                            if piece != 0 and piece.color == turno:
                                selected_piece = piece
                                valid_moves = board.get_valid_moves(piece)
                            else:
                                selected_piece = None
                                valid_moves = []
                else:
                    if piece != 0 and piece.color == turno:
                        if not forcando_captura or piece == selected_piece:
                            selected_piece = piece
                            valid_moves = board.get_valid_moves(piece)

        await asyncio.sleep(0)  # 🟢 Integração com asyncio

    pygame.quit()

if __name__ == "__main__":
    menu()
    asyncio.run(main_async())
