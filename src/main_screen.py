import pygame
from pygame.locals import *
import random
import question
# map class (20 x 20 cells)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

pygame.init()
# initiale screen
font1 = pygame.font.SysFont(None, 48)
font2 = pygame.font.SysFont(None, 32)
font3 = pygame.font.SysFont(None, 20)
player_turn_text = font1.render(f'PLAYER TURN', True, GREEN, BLACK)
gameover_text = font1.render(f'GAME OVER', True, RED, BLACK)
player_action_move_text = font1.render(f'MOVE/ATTACK', True, WHITE, BLACK)
enemy_turn_text = font1.render(f'ENEMY TURN', True, RED, BLACK)
cursor = pygame.transform.scale(pygame.image.load("images/cursor.webp"), (100, 100))
ship_side = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("images/ship2.webp"), (200, 200)), 270)
alien_side = pygame.transform.scale(pygame.image.load("images/alien_side.png"), (200, 200))
explosion_large = pygame.transform.scale(pygame.image.load("images/explosion.png"), (200, 200))
explosion_small = pygame.transform.scale(pygame.image.load("images/explosion.png"), (100, 100))

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 640
FPS = 60
GRID_LENGTH = 90
FramePerSec = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
map_background = pygame.transform.scale(pygame.image.load("images/map_background.webp"), (SCREEN_WIDTH * 1.8, SCREEN_HEIGHT * 2.4))
DISPLAYSURF.fill(BLACK)
DISPLAYSURF.blit(map_background, (0, -SCREEN_HEIGHT))

# ship class
class Ship:
    destroyed = False
    current_pos = (0, 0)
    def __init__(self, image_loc, start_pos, hp):
        self.image = pygame.transform.scale(pygame.image.load(image_loc), (85, 85))
        self.current_pos = start_pos
        self.hp = hp

# enemy class
class Enemy:
    def __init__(self):
        self.ship_array = []
        # make ship classes and own them
        self.ship_array.append(Ship("images/alien1.webp", (2, 2), 3))
        self.ship_array.append(Ship("images/alien2.webp", (5, 4), 2))
        self.ship_array.append(Ship("images/alien3.webp", (2, 3), 4))
        self.ship_array.append(Ship("images/alien4.webp", (9, 0), 3))
        self.ship_array.append(Ship("images/alien2.webp", (1, 0), 3))
        self.ship_array.append(Ship("images/alien3.webp", (2, 9), 3))

# player class
class Player:
    def __init__(self):
        self.ship_array = []
        # make ship classes and own them
        self.ship_array.append(Ship("images/ship1.webp", (3, 9), 6))
        self.ship_array.append(Ship("images/ship2.webp", (4, 9), 6))
        self.ship_array.append(Ship("images/ship3.webp", (5, 9), 6))

def update_question(subject_diff, level_diff):
    # update the current question
    q, option_a, option_b, option_c, option_d, correct_answer = question.generate_question(subject_diff, level_diff)
    answers = [option_a, option_b, option_c, option_d]
    return q, answers, correct_answer

# input difficulty
def run_map(subject_diff, level_diff):
    # make the point list for stars background
    question = "what is the differentiation of x square?"
    answer = ["a) 2x", "b) x", "c) x cube", "d) 99x"]
    correct_answer = 0 # 0~3
    point_list = []
    for i in range(0, 500):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        point_list.append((x,y))
    player_turn = True
    ship_number = 0
    cursor_pos = 0
    fight_number = 0
    cursor_valid_pos = (0, 0)
    lock = False
    game_over = False
    cursor_locked = False
    attacked_ship = 0
    attacker_player = True
    select_location_moving = False
    player = Player()
    enemy = Enemy()
    current_pos = player.ship_array[ship_number].current_pos
    while True:
        if game_over:
            DISPLAYSURF.fill(BLACK)
            DISPLAYSURF.blit(gameover_text, (SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    break
        else:
            for event in pygame.event.get():           
                if event.type == QUIT:
                    pygame.quit()
                    break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        cursor_pos += 1
                    if event.key == pygame.K_DOWN:
                        cursor_pos -= 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if lock == False:
                            attack, attacked_ship = space_check_move (cursor_valid_pos, player, enemy, ship_number)
                            if attack == True:
                                lock = True
                                attacker_player = True
                            if ship_number >= len(player.ship_array) - 1:
                                ship_number = 0
                                current_pos = enemy.ship_array[ship_number].current_pos
                                player_turn = False
                            elif 0 == len(player.ship_array):
                                lock = True
                                game_over = True
                            else:
                                ship_number += 1
                                current_pos = player.ship_array[ship_number].current_pos
                        else:
                            fight_number += 1
            # draw the new image
            draw_everything(current_pos, player, enemy)
            if not lock:
                if player_turn:
                    draw_player_turn_stuff()
                    valid_moves = get_valid_moves(current_pos, player_turn, player, enemy)
                    cursor_valid_pos = draw_grids_on_valid_moves(valid_moves, current_pos, cursor_pos)
                else:
                    DISPLAYSURF.blit(enemy_turn_text, (0, 0))
                    # wait 1 second
                    # do action
                    if ship_number < len(enemy.ship_array):
                        attack, attacked_ship = enemy_move_attack(current_pos, player, enemy, ship_number)
                    pygame.display.update() 
                    pygame.time.wait(1000)
                    if attack == True:
                        lock = True
                        attacker_player = False
                    if ship_number >= len(enemy.ship_array) - 1:
                        ship_number = 0
                        current_pos = player.ship_array[ship_number].current_pos
                        player_turn = True
                    elif 0 == len(enemy.ship_array):
                                lock = True
                                game_over = True
                    else:
                        ship_number += 1
                        current_pos = enemy.ship_array[ship_number].current_pos
            # update this
            if lock == True and game_over == False:
                if attacker_player:
                    done, damage, point_list = draw_player_fire_question(question, answer, correct_answer, point_list, cursor_pos, fight_number)
                    if done == True:
                        # make the hit player damaged or destroy if health is low
                        if damage >= enemy.ship_array[attacked_ship].hp:
                            print("deleted")
                            del enemy.ship_array[attacked_ship]
                        else:
                            enemy.ship_array[attacked_ship].hp -= damage
                        fight_number = 0
                        lock = False

                else:
                    done, damage, point_list = draw_enemy_fire_question(question, answer, correct_answer, point_list, cursor_pos, fight_number)
                    # make the hit player damaged or destroy if health is low
                    if done == True:
                        if damage >= player.ship_array[attacked_ship].hp:
                            print("deleted")
                            del player.ship_array[attacked_ship]
                        else:
                            player.ship_array[attacked_ship].hp -= damage
                            fight_number = 0
                        lock = False
            else:
                pygame.display.update()

    if start:
        return True
    else:
        return False
    
def update_points(points):
    new_points = []
    for point_x, point_y in points:
        if point_x < 0:
            point_x = point_x + SCREEN_WIDTH
            point_y = random.randint(0, SCREEN_WIDTH)
            new_points.append((point_x, point_y))
        else:
            point_x = point_x - 2
            new_points.append((point_x, point_y))
    return new_points

def draw_enemy_fire_question(question, answer, correct_answer, point_list, cursor_position, fight_number):
    point_list = update_points(point_list)
    done = False
    damage = 2
    # draw a blank layer
    DISPLAYSURF.fill(BLACK)
    
    for point in point_list:
        pygame.draw.circle(DISPLAYSURF, WHITE, point, 1)
    # draw the enemy and the player
    DISPLAYSURF.blit(ship_side, (900, 100))
    DISPLAYSURF.blit(alien_side, (200, 200))
    # display the question and answers
    DISPLAYSURF.blit(font2.render(question, True, WHITE, BLACK), (100, 330))
    DISPLAYSURF.blit(font2.render(answer[0], True, WHITE, BLACK), (100, 380))
    DISPLAYSURF.blit(font2.render(answer[1], True, WHITE, BLACK), (100, 430))
    DISPLAYSURF.blit(font2.render(answer[2], True, WHITE, BLACK), (100, 480))
    DISPLAYSURF.blit(font2.render(answer[3], True, WHITE, BLACK), (100, 530))
    # display the cursor
    print(cursor_position)
    DISPLAYSURF.blit(cursor, (0, 50 * ((cursor_position % 4) + 1) + 285))
    if (cursor_position % 4) == correct_answer and fight_number > 0:
        print("correct")
        DISPLAYSURF.blit(font1.render("CORRECT", True, GREEN, BLACK), (500, 530)) 
        DISPLAYSURF.blit(explosion_small, (900, 100))
        pygame.display.update()
        pygame.time.wait(1000)
        done = True
        damage = 1
    elif fight_number > 0:
        print("wrong")
        DISPLAYSURF.blit(font1.render("WRONG", True, RED, BLACK), (500, 530))
        DISPLAYSURF.blit(explosion_large, (900, 100))
        pygame.display.update()
        pygame.time.wait(1000)
        done = True
        damage = 2
    pygame.display.update()
    return done, damage, point_list

def draw_player_fire_question(question, answer, correct_answer, point_list, cursor_position, fight_number):
    point_list = update_points(point_list)
    done = False
    damage = 2
    # draw a blank layer
    DISPLAYSURF.fill(BLACK)
    
    for point in point_list:
        pygame.draw.circle(DISPLAYSURF, WHITE, point, 1)
    # draw the enemy and the player
    DISPLAYSURF.blit(ship_side, (200, 200))
    DISPLAYSURF.blit(alien_side, (900, 100))
    # display the question and answers
    DISPLAYSURF.blit(font2.render(question, True, WHITE, BLACK), (100, 330))
    DISPLAYSURF.blit(font2.render(answer[0], True, WHITE, BLACK), (100, 380))
    DISPLAYSURF.blit(font2.render(answer[1], True, WHITE, BLACK), (100, 430))
    DISPLAYSURF.blit(font2.render(answer[2], True, WHITE, BLACK), (100, 480))
    DISPLAYSURF.blit(font2.render(answer[3], True, WHITE, BLACK), (100, 530))
    # display the cursor
    print(cursor_position)
    DISPLAYSURF.blit(cursor, (0, 50 * ((cursor_position % 4) + 1) + 285))
    if (cursor_position % 4) == correct_answer and fight_number > 0:
        print("correct")
        DISPLAYSURF.blit(font1.render("CORRECT", True, GREEN, BLACK), (500, 530))
        DISPLAYSURF.blit(explosion_large, (900, 100))
        pygame.display.update()
        pygame.time.wait(1000)
        done = True
        damage = 2
    elif fight_number > 0:
        print("wrong")
        DISPLAYSURF.blit(font1.render("WRONG", True, RED, BLACK), (500, 530))
        DISPLAYSURF.blit(explosion_small, (900, 100))
        pygame.display.update()
        pygame.time.wait(1000)
        done = True
        damage = 1
    pygame.display.update()
    return done, damage, point_list

def enemy_move_attack(current_pos, player, enemy, ship_number):
    print(len(enemy.ship_array))
    enemy_current_pos = enemy.ship_array[ship_number].current_pos
    attack = False
    attacked_ship = 0
    enemy_valid_moves = get_valid_moves(enemy_current_pos, False, player, enemy)
    # check if can attack, else just move to a random index
    for i in range(0, len(enemy_valid_moves)):
        for j in range(0, len(player.ship_array)): 
            if player.ship_array[j].current_pos == enemy_valid_moves[i]:
                attack = True
                attacked_ship = j
    if attack == False:
        # move to a random valid index
        move_point = enemy_valid_moves[random.randint(0, len(enemy_valid_moves) - 1)]
        enemy.ship_array[ship_number].current_pos = move_point
        pygame.draw.circle(DISPLAYSURF, RED, (calculate_center_grid_locations(current_pos, move_point)), 30, 5)
    return attack, attacked_ship

def space_check_move (cursor_valid_pos, player, enemy, ship_number):
    attack = False
    attacked_ship = 0
    # check for attack
    for index in range(0, len(enemy.ship_array)):
        if enemy.ship_array[index].current_pos == cursor_valid_pos:
            attack = True
            attacked_ship = index
    if attack == False:
        # move the player ship
        player.ship_array[ship_number].current_pos = cursor_valid_pos
    return attack, attacked_ship

def draw_player_turn_stuff():
    # draw the player turn
    DISPLAYSURF.blit(player_turn_text, (0, 0))
    # draw the player actions
    DISPLAYSURF.blit(player_action_move_text, (0, 50))    
    return

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
def draw_everything(current_pos, player, enemy):
    x_cells = 10
    y_cells = 10
    # clear the screen
    DISPLAYSURF.fill(BLACK)
    # draw the background
    # get top left grid location
    background_anchor_x, background_anchor_y = calculate_center_grid_locations(current_pos, (0, 0))
    # draw the background depending on that
    DISPLAYSURF.blit(map_background, (background_anchor_x - 500, background_anchor_y - 400))
    # draw the grid
    for x in range(0, x_cells):
            for y in range(0, y_cells):
                real_pos = calculate_center_grid_locations(current_pos, (x, y))
                draw_grid_lines(real_pos)
    # draw the enemies and players
    # get locations of enemies and players
    draw_ships(current_pos, player, enemy)

    return

def draw_ships(current_pos, player, enemy):
    for ship in player.ship_array:
        real_pos_x, real_pos_y = calculate_center_grid_locations(current_pos, ship.current_pos)
        DISPLAYSURF.blit(ship.image, (real_pos_x - 40, real_pos_y - 40))
        # draw the hp on top
        current_hp = "hp:{}".format(ship.hp)
        DISPLAYSURF.blit(font3.render(current_hp, True, RED, BLACK),(real_pos_x, real_pos_y - 30)) 
    for ship in enemy.ship_array:
        real_pos_x, real_pos_y = calculate_center_grid_locations(current_pos, ship.current_pos)
        DISPLAYSURF.blit(ship.image, (real_pos_x - 40, real_pos_y - 40))
        # draw the hp on top
        current_hp = "hp:{}".format(ship.hp)
        DISPLAYSURF.blit(font3.render(current_hp, True, RED, BLACK),(real_pos_x, real_pos_y - 30)) 
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

def get_valid_moves(current_pos, player_turn, player, enemy):
    possible_moves_list = []
    filtered_moves_list = []
    current_x, current_y = current_pos
    # consider only 3x3 grid
    possible_moves_list.append((current_x - 1, current_y - 1))
    possible_moves_list.append((current_x, current_y - 1))
    possible_moves_list.append((current_x + 1, current_y - 1))
    possible_moves_list.append((current_x - 1, current_y))
    possible_moves_list.append((current_x + 1, current_y))
    possible_moves_list.append((current_x - 1, current_y + 1))
    possible_moves_list.append((current_x, current_y + 1))
    possible_moves_list.append((current_x + 1, current_y + 1))
    # filter the invalid moves
    # out of range
    for (move_x, move_y) in possible_moves_list:
        not_in_other_location = True
        if player_turn:
            for ship in player.ship_array:
                if ship.current_pos == (move_x, move_y):
                    not_in_other_location = False
        else:
            not_in_other_location = True
            for ship in enemy.ship_array:
                if ship.current_pos == (move_x, move_y):
                    not_in_other_location = False
        if move_x <= 9 and move_x >= 0 and not_in_other_location and move_y <= 9 and move_y >= 0:
            filtered_moves_list.append((move_x, move_y))
    # if player turn players, if enemy turn enemies
    return filtered_moves_list

def draw_grids_on_valid_moves(valid_moves, current_pos, cursor_pos):
    # red on player
    pygame.draw.circle(DISPLAYSURF, RED, (calculate_center_grid_locations(current_pos, current_pos)), 40, 1)
    # blue on cursor selected 
    cursor_valid_pos = valid_moves[cursor_pos % len(valid_moves)]
    pygame.draw.circle(DISPLAYSURF, BLUE, (calculate_center_grid_locations(current_pos, cursor_valid_pos)), 30, 5)
    for grid_pos in valid_moves:
        # draw circle
        pygame.draw.circle(DISPLAYSURF, GREEN, (calculate_center_grid_locations(current_pos, grid_pos)), 40, 1)
    return cursor_valid_pos