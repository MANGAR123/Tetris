import pygame
import random

pygame.init()

# Configuración del juego
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
FPS = 10

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definición de formas
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1],
     [1]],
    [[1, 1, 1],
     [0, 0, 1]],
    [[1, 1, 1],
     [0, 1]],
    [[1, 1],
     [1, 1]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1]],
]

# Inicialización de la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

class Tetris:
    def __init__(self):
        self.grid = [[0] * (WIDTH // GRID_SIZE) for _ in range(HEIGHT // GRID_SIZE)]
        self.current_shape = self.spawn_shape()
        self.score = 0

    def spawn_shape(self):
        shape = random.choice(SHAPES)
        color = random.choice([RED, CYAN, MAGENTA, YELLOW, GREEN, BLUE])
        return {'shape': shape, 'color': color, 'x': 0, 'y': 0}

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_shape(self, shape):
        for y, row in enumerate(shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, shape['color'],
                                     (shape['x'] * GRID_SIZE + x * GRID_SIZE,
                                      shape['y'] * GRID_SIZE + y * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE))

    def move_down(self):
        self.current_shape['y'] += 1
        if self.collision():
            self.current_shape['y'] -= 1
            self.merge_shape()
            self.clear_lines()
            self.current_shape = self.spawn_shape()

    def move_left(self):
        self.current_shape['x'] -= 1
        if self.collision():
            self.current_shape['x'] += 1

    def move_right(self):
        self.current_shape['x'] += 1
        if self.collision():
            self.current_shape['x'] -= 1

    def rotate(self):
        self.current_shape['shape'] = list(zip(*reversed(self.current_shape['shape'])))
        if self.collision():
            self.current_shape['shape'] = list(zip(*reversed(self.current_shape['shape'])))

    def collision(self):
        for y, row in enumerate(self.current_shape['shape']):
            for x, cell in enumerate(row):
                if cell and (self.current_shape['x'] + x < 0 or
                             self.current_shape['x'] + x >= WIDTH // GRID_SIZE or
                             self.current_shape['y'] + y >= HEIGHT // GRID_SIZE or
                             self.grid[self.current_shape['y'] + y][self.current_shape['x'] + x]):
                    return True
        return False

    def merge_shape(self):
        for y, row in enumerate(self.current_shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_shape['y'] + y][self.current_shape['x'] + x] = self.current_shape['color']

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0] * (WIDTH // GRID_SIZE))
        self.score += len(lines_to_clear)

# Inicialización del juego
tetris = Tetris()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                tetris.move_down()
            elif event.key == pygame.K_LEFT:
                tetris.move_left()
            elif event.key == pygame.K_RIGHT:
                tetris.move_right()
            elif event.key == pygame.K_UP:
                tetris.rotate()

    screen.fill(BLACK)
    tetris.move_down()
    tetris.draw_grid()
    tetris.draw_shape(tetris.current_shape)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
