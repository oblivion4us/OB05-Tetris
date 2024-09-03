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
    (0, 255, 0),  # Зеленый
    (0, 0, 255),  # Синий
    (128, 0, 128),  # Фиолетовый
    (255, 0, 0)  # Красный
]

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Тетрис')
clock = pygame.time.Clock()

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

current_theme = 'dark'  # По умолчанию темная тема


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
    border_color = WHITE if current_theme == 'dark' else BLACK
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, cell, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, border_color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def draw_tetromino(surface, tetromino):
    border_color = WHITE if current_theme == 'dark' else BLACK
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, tetromino.color,
                                 ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE,
                                  BLOCK_SIZE))
                pygame.draw.rect(surface, border_color,
                                 ((tetromino.x + x) * BLOCK_SIZE, (tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE,
                                  BLOCK_SIZE), 1)


def main_menu():
    global screen
    # Увеличиваем размеры экрана для меню
    menu_width, menu_height = WIDTH + 100, HEIGHT + 100
    screen = pygame.display.set_mode((menu_width, menu_height))

    while True:
        screen.fill(BLACK if current_theme == 'dark' else WHITE)

        font = pygame.font.SysFont(None, 75)
        title = font.render('Тетрис', True, WHITE if current_theme == 'dark' else BLACK)
        screen.blit(title, (menu_width // 2 - title.get_width() // 2, menu_height // 4))

        button_font = pygame.font.SysFont(None, 40)

        start_button = pygame.Rect(menu_width // 4, menu_height // 2 - 80, menu_width // 2, 50)
        theme_button = pygame.Rect(menu_width // 4, menu_height // 2, menu_width // 2, 50)
        quit_button = pygame.Rect(menu_width // 4, menu_height // 2 + 80, menu_width // 2, 50)

        pygame.draw.rect(screen, WHITE if current_theme == 'dark' else BLACK, start_button)
        pygame.draw.rect(screen, WHITE if current_theme == 'dark' else BLACK, theme_button)
        pygame.draw.rect(screen, WHITE if current_theme == 'dark' else BLACK, quit_button)

        start_text = button_font.render('Начать игру', True, BLACK if current_theme == 'dark' else WHITE)
        theme_text = button_font.render('Сменить тему', True, BLACK if current_theme == 'dark' else WHITE)
        quit_text = button_font.render('Выйти', True, BLACK if current_theme == 'dark' else WHITE)

        screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, start_button.y + 5))
        screen.blit(theme_text, (theme_button.x + (theme_button.width - theme_text.get_width()) // 2, theme_button.y + 5))
        screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2, quit_button.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Возвращаемся к игровому размеру экрана
                    return  # Начать игру
                if theme_button.collidepoint(event.pos):
                    change_theme()  # Сменить тему
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def change_theme():
    global current_theme, BLACK, WHITE
    if current_theme == 'dark':
        current_theme = 'light'
    else:
        current_theme = 'dark'


def pause_menu():
    while True:
        screen.fill(BLACK if current_theme == 'dark' else WHITE)

        font = pygame.font.SysFont(None, 55)
        pause_text = font.render('Пауза', True, WHITE if current_theme == 'dark' else BLACK)
        instruction_text = font.render('Нажмите любую клавишу', True, WHITE if current_theme == 'dark' else BLACK)

        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return  # Вернуться к игре


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
                if event.key == pygame.K_ESCAPE:
                    pause_menu()

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

        screen.fill(BLACK if current_theme == 'dark' else WHITE)
        draw_grid(screen, grid)
        draw_tetromino(screen, current_tetromino)
        pygame.display.flip()

if __name__ == '__main__':
    main_menu()
    main()