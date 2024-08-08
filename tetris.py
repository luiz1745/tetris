import pygame
import random

# Configurações da tela
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Definindo as formas das peças
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

COLORS = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.current_position = [0, 0]
        self.game_over = False
        self.fall_time = 0

    def draw_board(self):
        self.screen.fill(BLACK)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                pygame.draw.rect(self.screen, self.board[y][x],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        if self.current_piece:
            for y, row in enumerate(self.current_piece):
                for x, color in enumerate(row):
                    if color:
                        pygame.draw.rect(self.screen, COLORS[color - 1],
                                         ((self.current_position[1] + x) * BLOCK_SIZE,
                                          (self.current_position[0] + y) * BLOCK_SIZE,
                                          BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()

    def create_piece(self):
        shape = random.choice(SHAPES)
        color = COLORS.index(random.choice(COLORS)) + 1
        return [[color if cell else 0 for cell in row] for row in shape]

    def check_collision(self, offset):
        for y, row in enumerate(self.current_piece):
            for x, color in enumerate(row):
                if color:
                    board_x = self.current_position[1] + x + offset[1]
                    board_y = self.current_position[0] + y + offset[0]
                    if (board_x < 0 or board_x >= BOARD_WIDTH or
                        board_y >= BOARD_HEIGHT or
                        (board_y >= 0 and self.board[board_y][board_x] != BLACK)):
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, color in enumerate(row):
                if color:
                    self.board[self.current_position[0] + y][self.current_position[1] + x] = COLORS[color - 1]

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.board) if all(cell != BLACK for cell in row)]
        for i in lines_to_clear:
            self.board.pop(i)
            self.board.insert(0, [BLACK] * BOARD_WIDTH)

    def run(self):
        self.current_piece = self.create_piece()
        self.current_position = [0, BOARD_WIDTH // 2 - len(self.current_piece[0]) // 2]
        while not self.game_over:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self.check_collision((0, -1)):
                            self.current_position[1] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if not self.check_collision((0, 1)):
                            self.current_position[1] += 1
                    elif event.key == pygame.K_DOWN:
                        if not self.check_collision((1, 0)):
                            self.current_position[0] += 1
                    elif event.key == pygame.K_UP:
                        self.current_piece = self.rotate_piece(self.current_piece)
                        if self.check_collision((0, 0)):
                            self.current_piece = self.rotate_piece(self.current_piece, -1)

            if self.fall_time > 500:  # Velocidade de queda
                self.fall_time = 0
                if not self.check_collision((1, 0)):
                    self.current_position[0] += 1
                else:
                    self.merge_piece()
                    self.clear_lines()
                    self.current_piece = self.create_piece()
                    self.current_position = [0, BOARD_WIDTH // 2 - len(self.current_piece[0]) // 2]
                    if self.check_collision((0, 0)):
                        self.game_over = True

            self.draw_board()

        pygame.quit()

    def rotate_piece(self, piece, times=1):
        for _ in range(times):
            piece = list(zip(*piece[::-1]))
        return [list(row) for row in piece]

if __name__ == "__main__":
    Tetris().run()

