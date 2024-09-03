import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
FPS = 10

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (0, 255, 255),  # Бирюзовый
    (255, 165, 0),  # Оранжевый
    (255, 255, 0),  # Желтый
    (0, 255, 0),    # Зеленый
    (0, 0, 255),    # Синий
    (128, 0, 128),  # Фиолетовый
    (255, 0, 0)     # Красный
]

# Фигуры тетриса
TETROMINOS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1], [1, 1]]  # O
]

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Тетрис')
clock = pygame.time.Clock()

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLUMNS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        new_shape = [list(row) for row in zip(*self.shape[::-1])]
        return new_shape

def check_collision(grid, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                if (x + tetromino.x < 0 or x + tetromino.x >= COLUMNS or
                        y + tetromino.y >= ROWS or grid[y + tetromino.y][x + tetromino.x]):
                    return True
    return False

def merge_grid(grid, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + tetromino.y][x + tetromino.x] = tetromino.color

def remove_full_lines(grid):
    lines_removed = 0
    for y in range(ROWS - 1, -1, -1):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0] * COLUMNS)
            lines_removed += 1
    return lines_removed

def draw_grid(surface, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_tetromino(surface, tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, tetromino.color, ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def main():
    grid = [[0] * COLUMNS for _ in range(ROWS)]
    current_tetromino = Tetromino(random.choice(TETROMINOS), random.choice(COLORS))
    next_tetromino = Tetromino(random.choice(TETROMINOS), random.choice(COLORS))
    last_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.x -= 1
                    if check_collision(grid, current_tetromino):
                        current_tetromino.x += 1
                if event.key == pygame.K_RIGHT:
                    current_tetromino.x += 1
                    if check_collision(grid, current_tetromino):
                        current_tetromino.x -= 1
                if event.key == pygame.K_DOWN:
                    current_tetromino.y += 1
                    if check_collision(grid, current_tetromino):
                        current_tetromino.y -= 1
                if event.key == pygame.K_UP:
                    new_shape = current_tetromino.rotate()
                    old_shape = current_tetromino.shape
                    current_tetromino.shape = new_shape
                    if check_collision(grid, current_tetromino):
                        current_tetromino.shape = old_shape

        current_time = pygame.time.get_ticks()
        if current_time - last_time > 500:
            current_tetromino.y += 1
            if check_collision(grid, current_tetromino):
                current_tetromino.y -= 1
                merge_grid(grid, current_tetromino)
                remove_full_lines(grid)
                current_tetromino = next_tetromino
                next_tetromino = Tetromino(random.choice(TETROMINOS), random.choice(COLORS))
                if check_collision(grid, current_tetromino):
                    grid = [[0] * COLUMNS for _ in range(ROWS)]  # Здесь можно реализовать конец игры и вывод результата
            last_time = current_time

        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_tetromino(screen, current_tetromino)
        pygame.display.flip()

if __name__ == '__main__':
    main()