import pygame
import chess
import chess.engine

pygame.init()

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
SQUARE_SIZE = SCREEN_WIDTH // 8
RED = (255, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREEN = (0, 128, 0)

chessboard_img = pygame.image.load('chessboard.png')
chessboard_img = pygame.transform.scale(chessboard_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

engine = chess.engine.SimpleEngine.popen_uci("C:\\Users\\Meet\\Desktop\\Stockfish\\stockfish-windows-x86-64-avx2.exe")
board = chess.Board()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pieces_dir = '/Users/Meet/Desktop/chessAI-main/my_chess/'
pieces_images = {
    "R": pygame.image.load(pieces_dir + "white_rook.png"),
    "N": pygame.image.load(pieces_dir + "white_knight.png"),
    "B": pygame.image.load(pieces_dir + "white_bishop.png"),
    "Q": pygame.image.load(pieces_dir + "white_queen.png"),
    "K": pygame.image.load(pieces_dir + "white_king.png"),
    "P": pygame.image.load(pieces_dir + "white_pawn.png"),
    "r": pygame.image.load(pieces_dir + "black_rook.png"),
    "n": pygame.image.load(pieces_dir + "black_knight.png"),
    "b": pygame.image.load(pieces_dir + "black_bishop.png"),
    "q": pygame.image.load(pieces_dir + "black_queen.png"),
    "k": pygame.image.load(pieces_dir + "black_king.png"),
    "p": pygame.image.load(pieces_dir + "black_pawn.png"),
}

def draw_board():
    screen.blit(chessboard_img, (0, 0))
    for square in chess.SQUARES:
        file, rank = chess.square_file(square), chess.square_rank(square)
        x, y = file * SQUARE_SIZE, (7 - rank) * SQUARE_SIZE
        piece = board.piece_at(square)
        if piece is not None:
            screen.blit(pieces_images.get(piece.symbol()), (x, y))
        if square in valid_moves:
            pygame.draw.circle(screen, RED, (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2), 10)

def handle_player_move(f, t):
    move = chess.Move(f, t)
    if move in board.legal_moves:
        board.push(move)
        draw_board()
        pygame.display.flip()
        valid_moves.clear()
        handle_ai_move()

def handle_ai_move():
    result = engine.play(board, chess.engine.Limit(time = 0.1))
    board.push(result.move)
    draw_board()
    pygame.display.flip()

clock = pygame.time.Clock()
running = True
selected_square = None
valid_moves = []
dragging_piece = None

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not board.turn or board.is_game_over():
                continue
            x, y = event.pos
            file, rank = x // SQUARE_SIZE, 7 - y // SQUARE_SIZE
            selected_square = chess.square(file, rank)
            dragging_piece = pieces_images.get(board.piece_at(selected_square).symbol())
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_square is not None:
                x, y = event.pos
                file, rank = x // SQUARE_SIZE, 7 - y // SQUARE_SIZE
                target_square = chess.square(file, rank)
                handle_player_move(selected_square, target_square)
                selected_square = None
                dragging_piece = None

    if selected_square is not None:
        valid_moves = [move.to_square for move in board.legal_moves if move.from_square == selected_square]

    draw_board()

    if dragging_piece is not None:
        x, y = event.pos
        screen.blit(dragging_piece, (x - SQUARE_SIZE // 2, y - SQUARE_SIZE // 2))

    pygame.display.flip()

engine.quit()
pygame.quit()
    