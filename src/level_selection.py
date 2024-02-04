
import sys
from typing import List, Tuple
import pygame
import random
from pygame.locals import *


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)

def selection_menu():
    # Initiliaze
    pygame.init()
    FPS = 60
    FramePerSec = pygame.time.Clock()
    # Text and stuff surface
    button_font = pygame.font.SysFont(None, 72)
    subject_text_1 = button_font.render(f'BIOLOGY', True, WHITE, BLACK)
    subject_text_2 = button_font.render(f'MATHEMATICS', True, WHITE, BLACK)
    subject_text_3 = button_font.render(f'CHEMISTRY', True, WHITE, BLACK)
    subject_text_4 = button_font.render(f'PHYSICS', True, WHITE, BLACK)
    subject_text_5 = button_font.render(f'COMPUTER SCIENCE', True, WHITE, BLACK)

    level_text_1 = button_font.render(f'ELEMENTARY', True, WHITE, BLACK)
    level_text_2 = button_font.render(f'MIDDLE SCHOOL', True, WHITE, BLACK)
    level_text_3 = button_font.render(f'HIGH SCHOOL', True, WHITE, BLACK)
    level_text_4 = button_font.render(f'UNDERGRAD', True, WHITE, BLACK)
    level_text_5 = button_font.render(f'GRAD', True, WHITE, BLACK)

    # cursor
    cursor = pygame.transform.scale(pygame.image.load("images/cursor.webp"), (100, 100))
    # Main display
    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")

    DISPLAYSURF.fill(BLACK)
    # make the point list for stars background
    point_list = []
    for i in range(0, 500):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        point_list.append((x,y))

    for point in point_list:
        pygame.draw.circle(DISPLAYSURF, WHITE, point, 1)

    start = False
    go_to_next_section = False
    cursor_position = 0
    subject_position = 0
    difficulty_position = 0 

    while True:
        for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    cursor_position -= 1
                    print("UP")
                if event.key == pygame.K_DOWN:
                    cursor_position += 1
                if event.key == pygame.K_SPACE:
                    print("SSS")
                    if go_to_next_section == True:
                        start = True
                        difficulty_position = cursor_position % 5
                    else:
                        subject_position = cursor_position % 5
                    go_to_next_section = True
                    print("ENTER")

        if start == True:
            break
        # update point
        point_list = update_points(point_list)
        # update screen
        DISPLAYSURF.fill(BLACK)
        
        for point in point_list:
            pygame.draw.circle(DISPLAYSURF, WHITE, point, 1)
        if go_to_next_section:
            DISPLAYSURF.blit(cursor, (700, 100 * ((cursor_position % 5) + 1) - 25))
        else:
            DISPLAYSURF.blit(cursor, (0, 100 * ((cursor_position % 5) + 1) - 25))
        
        DISPLAYSURF.blit(subject_text_1, (100, 100))
        DISPLAYSURF.blit(subject_text_2, (100, 200))
        DISPLAYSURF.blit(subject_text_3, (100, 300))
        DISPLAYSURF.blit(subject_text_4, (100, 400))
        DISPLAYSURF.blit(subject_text_5, (100, 500))
        if go_to_next_section:
            DISPLAYSURF.blit(level_text_1, (800, 100))
            DISPLAYSURF.blit(level_text_2, (800, 200))
            DISPLAYSURF.blit(level_text_3, (800, 300))
            DISPLAYSURF.blit(level_text_4, (800, 400))
            DISPLAYSURF.blit(level_text_5, (800, 500))
        pygame.display.update()
        FramePerSec.tick(FPS)
    if start:
        return (subject_position, difficulty_position)
    else:
        return (-1, -1)

def update_points(points):
    new_points = []
    for point_x, point_y in points:
        if point_y > SCREEN_HEIGHT:
            point_y = point_y - SCREEN_HEIGHT
            point_x = random.randint(0, SCREEN_WIDTH)
            new_points.append((point_x, point_y))
        else:
            point_y = point_y + 2
            new_points.append((point_x, point_y))
    return new_points
