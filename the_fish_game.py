import pygame
import sys
import random

pygame.init()

"this code creates the floor and the roof of the game twice in different positions"
def draw_roof_floor():
    screen.blit(floor_surface, (floor_roof_x_pos, 480))
    screen.blit(roof_surface, (floor_roof_x_pos, -40))
    screen.blit(floor_surface, (floor_roof_x_pos + 1045, 480))
    screen.blit(roof_surface, (floor_roof_x_pos + 1010, -40))

"this code chooses a height for the peelers and saves the bottom and the top"
def create_pil():
    random_pil_y = random.choice(pil_height)
    bottom_pil = pil.get_rect(center=(1200, random_pil_y))
    top_pil = pil.get_rect(center=(1200, random_pil_y + 512))
    return bottom_pil, top_pil

"this code moves the peelers according to their speed"
def move_pil(pil_list, pil_speed):
    for pile in pil_list:
        pile.centerx += pil_speed
    return pil_list


def draw_pil(pil_list):
    for pile in pil_list:
        screen.blit(pil, pile)

"this code checks if there was a collision between the peelers the roof or the floor"
def check_collision(pil_list):
    for pile in pil_list:
        if fish_rect.colliderect(pile):
            return False

    if fish_rect.bottom >= 480 or fish_rect.top <= 70:
        return False

    return True

"this code creates a font to be used in the game"
def font_maker(game_active):
    if game_active:
        score_surface = score_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(512, 120))
        screen.blit(score_surface, score_rect)

    else:
        score_surface = score_font.render(f'score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(512, 120))
        screen.blit(score_surface, score_rect)

        the_fish_game_title = title_font.render("the fish game", True, (100, 255, 50))
        the_fish_game_surface = the_fish_game_title.get_rect(center=(512, 256))
        screen.blit(the_fish_game_title, the_fish_game_surface)

        p_space = space_font.render("'click space to start'", True, (0, 0, 0))
        p_space_rect = p_space.get_rect(center=(512, 340))
        screen.blit(p_space, p_space_rect)

        high_score_surface = score_font.render(f'high score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(510, 450))
        screen.blit(high_score_surface, high_score_rect)

"this code saves the previous high score"
def the_high_score():
    open_high_score = open(r"the fish game sec\the best score.txt", "r")
    the_old_high_score = open_high_score.read()
    open_high_score.close()
    return the_old_high_score

"this code saves the highest score in a text file"
def new_high_score(high_score):
    open_high_score = open(r"the fish game sec\the best score.txt", "w")
    open_high_score.write(high_score)
    open_high_score.close()

"Saves general values that are important to the operation of the game"
game_active = False
screen = pygame.display.set_mode((1024, 562))
clock = pygame.time.Clock()
game_song = pygame.mixer.Sound(r"the fish game sec\ForestWalk-320bit.mp3")

score_font = pygame.font.SysFont("MV Boli", 40)
title_font = pygame.font.SysFont("Algerian", 120)
space_font = pygame.font.SysFont("Arial", 30)
score = 0
high_score = the_high_score()

bg_surface = pygame.image.load(r"the fish game sec\the fish game back rond.png").convert_alpha()
bg_surface = pygame.transform.scale(bg_surface, (1100, 600))

floor_surface = pygame.image.load(r"the fish game sec\the fish game floor.png").convert_alpha()
floor_surface = pygame.transform.scale(floor_surface, (1064, 100))
roof_surface = pygame.image.load(r"the fish game sec\the fish game roof.png").convert_alpha()
roof_surface = pygame.transform.scale(roof_surface, (1064, 130))
floor_roof_x_pos = -20
floor_roof_pil_speed = -1

fish = pygame.image.load(r"the fish game sec\the fish game fish.png").convert_alpha()
fish = pygame.transform.scale(fish, (120, 60))
fish_rect = fish.get_rect(center=(100, 256))
ind_up = 0
ind_down = 0

pil = pygame.image.load(r"the fish game sec\the fish game pil.png").convert_alpha()
pil = pygame.transform.scale(pil, (180, 350))
pil_list = []
SPAWNPIL = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIL, 3600)
pil_height = [-50, 0, 50, 100, 150]

"making a lop to start the game"
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        "Checks what the player clicks on and acts accordingly"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:
                ind_up = 0
            if event.key == pygame.K_DOWN and game_active:
                ind_down = 0
            if not game_active and event.key == pygame.K_SPACE:
                pil_list.clear()
                fish_rect.center = (100, 256)
                ind_up = 51
                ind_down = 51
                floor_roof_pil_speed = -1
                score = 0
                game_active = True


        if event.type == SPAWNPIL:
            pil_list.extend(create_pil())

    screen.blit(bg_surface, (-40, -10))

    "Performs all necessary actions when starting the game"
    if game_active:
        game_song.play()
        screen.blit(fish, fish_rect)

        floor_roof_x_pos += floor_roof_pil_speed
        if ind_up <= 50:
            fish_rect.centery -= 5
            ind_up += 5
        if ind_down <= 50:
            fish_rect.centery += 5
            ind_down += 5

        pil_list = move_pil(pil_list, floor_roof_pil_speed)
        draw_pil(pil_list)

        floor_roof_pil_speed -= 0.002
        score += 0.01
        font_maker(game_active)

    else:
        game_song.play()
        floor_roof_x_pos -= 1
        if score > int(high_score):
            high_score = int(score)
            new_high_score(str(high_score))
        font_maker(game_active)

    draw_roof_floor()

    game_active = check_collision(pil_list)
    if floor_roof_x_pos <= -1044:
        floor_roof_x_pos = -20

    pygame.display.update()
    clock.tick(120)
