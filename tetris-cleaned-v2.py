import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
COLORS = [
    (255, 0, 0),   # Red
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 255, 0), # Yellow
    (255, 165, 0), # Orange
    (128, 0, 128), # Purple
]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1], [1, 1]], # O-shape
    [[0, 1, 0], [1, 1, 1]], # T-shape
    [[1, 0, 0], [1, 1, 1]], # L-shape
    [[0, 0, 1], [1, 1, 1]], # J-shape
    [[0, 1, 1], [1, 1, 0]], # S-shape
    [[1, 1, 0], [0, 1, 1]], # Z-shape
]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crazy Tetris")
clock = pygame.time.Clock()

# Grid
GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE

def create_grid(locked_positions=None):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    if locked_positions:
        for (x, y), color in locked_positions.items():
            grid[y][x] = color
    return grid

def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for x in range(GRID_WIDTH):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))
    for y in range(GRID_HEIGHT):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))

def clear_rows(grid, locked_positions):
    rows_to_clear = []
    for y in range(GRID_HEIGHT):
        if BLACK not in grid[y]:
            rows_to_clear.append(y)

    for row in rows_to_clear:
        for x in range(GRID_WIDTH):
            del locked_positions[(x, row)]

    for row in sorted(rows_to_clear):
        for y in range(row, 0, -1):
            for x in range(GRID_WIDTH):
                locked_positions[(x, y)] = locked_positions.get((x, y - 1), BLACK)

    return len(rows_to_clear)

class Tetrimino:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def draw(self, surface):
        for i, row in enumerate(self.shape):
            for j, col in enumerate(row):
                if col:
                    pygame.draw.rect(
                        surface,
                        self.color,
                        (
                            (self.x + j) * BLOCK_SIZE,
                            (self.y + i) * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        ),
                    )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

def check_collision(grid, shape, offset):
    off_x, off_y = offset
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                x, y = off_x + j, off_y + i
                if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or grid[y][x] != BLACK:
                    return True
    return False

def place_tetrimino(grid, tetrimino):
    for i, row in enumerate(tetrimino.shape):
        for j, cell in enumerate(row):
            if cell:
                grid[tetrimino.y + i][tetrimino.x + j] = tetrimino.color

def game_over(locked_positions):
    for x, y in locked_positions.keys():
        if y < 1:
            return True
    return False

# Main loop
def main():
    grid = create_grid()
    locked_positions = {}

    current_piece = Tetrimino(random.choice(SHAPES))
    next_piece = Tetrimino(random.choice(SHAPES))

    fall_time = 0
    fall_speed = 0.5  # Adjust speed here (lower is slower)

    score = 0
    running = True
    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(grid, current_piece.shape, (current_piece.x - 1, current_piece.y)):
                        current_piece.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if not check_collision(grid, current_piece.shape, (current_piece.x + 1, current_piece.y)):
                        current_piece.move(1, 0)
                if event.key == pygame.K_DOWN:
                    if not check_collision(grid, current_piece.shape, (current_piece.x, current_piece.y + 1)):
                        current_piece.move(0, 1)

        # Move piece down
        if fall_time / 1000 > fall_speed:
            if not check_collision(grid, current_piece.shape, (current_piece.x, current_piece.y + 1)):
                current_piece.move(0, 1)
            else:
                for i, row in enumerate(current_piece.shape):
                    for j, cell in enumerate(row):
                        if cell:
                            locked_positions[(current_piece.x + j, current_piece.y + i)] = current_piece.color
                current_piece = next_piece
                next_piece = Tetrimino(random.choice(SHAPES))

                # Ensure the I-shape gets equal probability
                next_piece.shape = random.choice(SHAPES)

                cleared_rows = clear_rows(grid, locked_positions)
                score += cleared_rows * 10

                if game_over(locked_positions):
                    print("Game Over! Your score:", score)
                    running = False

            fall_time = 0

        screen.fill(BLACK)
        draw_grid(screen, grid)
        current_piece.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
