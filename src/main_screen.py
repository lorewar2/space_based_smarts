import pygame
from pygame.locals import *
# map class (20 x 20 cells)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)


# initiale screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 640
FPS = 60
GRID_LENGTH = 90
FramePerSec = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
map_background = pygame.transform.scale(pygame.image.load("images/map_background.webp"), (SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 3))
DISPLAYSURF.fill(BLACK)
DISPLAYSURF.blit(map_background, (0, -SCREEN_HEIGHT))

# ship class
class Ship:
    destroyed = False
    current_position = (0, 0)
    def __init__(self, image_loc, start_pos, hp):
        self.image = pygame.transform.scale(pygame.image.load(image_loc), (90, 90))
        self.current_position = start_pos
        self.hp = hp

# enemy class
class Enemy:
    def __init__(self):
        self.ship_array = []
        # make ship classes and own them
        self.ship_array.append(Ship("images/alien1.webp", (2, 2), 3))
        self.ship_array.append(Ship("images/alien2.webp", (5, 4), 2))
        self.ship_array.append(Ship("images/alien3.webp", (2, 3), 4))
        self.ship_array.append(Ship("images/alien4.webp", (8, 2), 3))

# player class
class Player:
    def __init__(self):
        self.ship_array
        # make ship classes and own them
        self.ship_array.append(Ship("images/ship1.webp", (3, 9), 6))
        self.ship_array.append(Ship("images/ship2.webp", (4, 4), 6))
        self.ship_array.append(Ship("images/ship3.webp", (5, 3), 6))

# input difficulty
def run_map(subject_diff, level_diff):
    current_pos = (5, 5)
    player = Player()
    enemy = Enemy()
    while True:
        for event in pygame.event.get():           
            if event.type == QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    current_pos = change_current_position(current_pos, 0)
                if event.key == pygame.K_DOWN:
                    current_pos = change_current_position(current_pos, 2)
                if event.key == pygame.K_RIGHT:
                    current_pos = change_current_position(current_pos, 1)
                if event.key == pygame.K_LEFT:
                    current_pos = change_current_position(current_pos, 3)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    break
        # draw the new image
        draw_everything(current_pos)
        pygame.display.update()
        FramePerSec.tick(FPS)

    if start:
        return True
    else:
        return False

# change current_position
def change_current_position(current_pos, type):
    # limit is 20
    current_x, current_y = current_pos
    if type == 0:
        print("up")
        if current_y == 0:
            current_y = 0
        else:
            current_y = current_y - 1
    elif type == 1:
        print("right")
        if current_x == 9:
            current_x = 9
        else:
            current_x = current_x + 1
    elif type == 2:
        print("down")
        if current_y == 9:
            current_y = 9
        else:
            current_y = current_y + 1
    elif type == 3:
        print("left")
        if current_x == 0:
            current_x = 0
        else:
            current_x = current_x - 1
    return (current_x, current_y)
# draw function to draw all the stuff grid background etc
def draw_everything(current_pos):
    x_cells = 10
    y_cells = 10
    # clear the screen
    DISPLAYSURF.fill(BLACK)
    # draw the background
    # get top left grid location
    background_anchor_x, background_anchor_y = calculate_center_grid_locations(current_pos, (0, 0))
    # draw the background depending on that
    DISPLAYSURF.blit(map_background, (background_anchor_x - SCREEN_WIDTH / 2.2, background_anchor_y - SCREEN_HEIGHT / 2))
    # draw the grid
    for x in range(0, x_cells):
            for y in range(0, y_cells):
                real_pos = calculate_center_grid_locations(current_pos, (x, y))
                draw_grid_lines(real_pos)
    # draw the background, place the image between (0 and -screen height)

    return

def calculate_center_grid_locations(current_pos, required_location):
    # current grid is at center therefore screen_width / 2 and screen_height / 2 1 grid is 120 x 120
    current_x, current_y = current_pos
    required_x, required_y = required_location

    diff_x = current_x - required_x
    diff_y = current_y - required_y
    required_x_real = -diff_x * 90 + (SCREEN_WIDTH / 2)
    required_y_real = -diff_y * 90 + (SCREEN_HEIGHT / 2)
    return required_x_real, required_y_real

def draw_grid_lines(real_pos):
    real_pos_x, real_pos_y = real_pos
    # top
    pygame.draw.line(DISPLAYSURF, PURPLE, (real_pos_x - 45, real_pos_y - 45), (real_pos_x + 45, real_pos_y - 45))
    # bottom
    pygame.draw.line(DISPLAYSURF, PURPLE, (real_pos_x - 45, real_pos_y + 45), (real_pos_x + 45, real_pos_y + 45))
    # left
    pygame.draw.line(DISPLAYSURF, PURPLE, (real_pos_x - 45, real_pos_y - 45), (real_pos_x - 45, real_pos_y + 45))
    # right
    pygame.draw.line(DISPLAYSURF, PURPLE, (real_pos_x + 45, real_pos_y - 45), (real_pos_x + 45, real_pos_y + 45))
    return
