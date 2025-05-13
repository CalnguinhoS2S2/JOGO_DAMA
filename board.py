import pygame
from constants import *
from piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def draw_squares(self, win):
        win.fill(BEIGE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row < 3 and (row + col) % 2 == 1:
                    self.board[row].append(Piece(row, col, RED))
                elif row > 4 and (row + col) % 2 == 1:
                    self.board[row].append(Piece(row, col, BLACK))
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in self.board:
            for piece in row:
                if piece != 0:
                    piece.draw(win)

    def get_piece(self, row, col):
        return self.board[row][col]

    def move_piece(self, piece, row, col):
        old_row = piece.row
        old_col = piece.col

        self.board[old_row][old_col], self.board[row][col] = 0, piece
        piece.move(row, col)

        # ✅ Remoção da peça capturada
        if abs(row - old_row) == 2 and abs(col - old_col) == 2:
            mid_row = (row + old_row) // 2
            mid_col = (col + old_col) // 2
            self.board[mid_row][mid_col] = 0  # Apaga a peça capturada

        # ✅ Promoção para dama
        if row == 0 and piece.color == BLACK:
            piece.make_king()
        elif row == 7 and piece.color == RED:
            piece.make_king()

    def valid_move(self, piece, row, col):
        return (row, col) in self.get_valid_moves(piece)

    def get_valid_moves(self, piece):
        moves = []
        captures = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            row = piece.row + dr
            col = piece.col + dc

            # Movimento simples
            if 0 <= row < ROWS and 0 <= col < COLS and self.board[row][col] == 0:
                if piece.king:
                    moves.append((row, col))
                elif piece.color == BLACK and dr == -1:
                    moves.append((row, col))
                elif piece.color == RED and dr == 1:
                    moves.append((row, col))

            # Captura
            row2 = piece.row + 2 * dr
            col2 = piece.col + 2 * dc
            if 0 <= row2 < ROWS and 0 <= col2 < COLS:
                mid_row = piece.row + dr
                mid_col = piece.col + dc
                middle_piece = self.get_piece(mid_row, mid_col)
                if self.board[row2][col2] == 0 and middle_piece != 0 and middle_piece.color != piece.color:
                    captures.append((row2, col2))

        return captures if captures else moves

    def has_capture(self, piece):
        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
        for dr, dc in directions:
            row = piece.row + dr
            col = piece.col + dc
            if 0 <= row < ROWS and 0 <= col < COLS:
                mid_row = (row + piece.row) // 2
                mid_col = (col + piece.col) // 2
                middle = self.get_piece(mid_row, mid_col)
                target = self.get_piece(row, col)
                if target == 0 and middle != 0 and middle.color != piece.color:
                    return True
        return False

    def draw_valid_moves(self, win, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(win, GREY, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def check_winner(self):
        red_pieces = 0
        black_pieces = 0
        red_moves = 0
        black_moves = 0

        for row in self.board:
            for piece in row:
                if piece != 0:
                    if piece.color == RED:
                        red_pieces += 1
                        red_moves += len(self.get_valid_moves(piece))
                    elif piece.color == BLACK:
                        black_pieces += 1
                        black_moves += len(self.get_valid_moves(piece))

        if red_pieces == 0 or red_moves == 0:
            return BLACK
        elif black_pieces == 0 or black_moves == 0:
            return RED
        return None
