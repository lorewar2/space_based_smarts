

import sys
from typing import List, Tuple
import pygame
from pygame.locals import *

def start_menu():
    # Initiliaze images
    pygame.init()
    
    FPS = 60
    FramePerSec = pygame.time.Clock()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PURPLE = (128, 0, 128)

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")

    background_wallpaper = pygame.transform.scale(pygame.image.load("images/main_menu_wallpaper.webp"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(background_wallpaper, (0, 0))
    title_image = pygame.transform.scale(pygame.image.load("images/logo.webp"), (SCREEN_WIDTH/4, SCREEN_HEIGHT/3))
    DISPLAYSURF.blit(title_image, (SCREEN_WIDTH / 2.7, SCREEN_HEIGHT / 4))
    button_font = pygame.font.SysFont(None, 72)
    button_text = button_font.render(f'Press Space to Start', True, PURPLE, BLACK)
    DISPLAYSURF.blit(button_text, (SCREEN_WIDTH / 3.3, 3 * SCREEN_HEIGHT / 4))

    start = False
    quit = False
    while True: 
        for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                quit = True
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    pygame.quit()
                    break
        if start == True or quit == True:
            break
        pygame.display.update()
        FramePerSec.tick(FPS)

    if start:
        return True
    else:
        return False
        # open the next one
