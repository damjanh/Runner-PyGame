import pygame
from sys import exit
from random import randint


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = font.render(f'{int(current_time / 1000)}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return int(current_time / 1000)


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > - 100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surface, player_index

    if player_rectangle.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Obstacles
snail_start_pos_x = 800
snail_frame_1 = pygame.image.load('graphics/enemy/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/enemy/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/enemy/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/enemy/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rectangle_list = []

# Player
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 2)
player_stand_rectangle = player_stand_surface.get_rect(center=(400, 200))

# Text
game_name_surface = font.render('Runner', False, (111, 196, 169))
game_name_rectangle = game_name_surface.get_rect(center=(400, 80))

game_message_surface = font.render("Press SPACE to start!", False, (111, 196, 169))
game_message_rectangle = game_message_surface.get_rect(center=(400, 330))

# Timers
obstacle_timer = pygame.USEREVENT + 1
snail_animation_timer = pygame.USEREVENT + 2
fly_animation_timer = pygame.USEREVENT + 3

pygame.time.set_timer(obstacle_timer, 1400)
pygame.time.set_timer(snail_animation_timer, 500)
pygame.time.set_timer(fly_animation_timer, 200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if player_rectangle.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rectangle_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rectangle_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 210)))
            elif event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            elif event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rectangle)

        # Obstacle movement
        obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)

        # Collision
        game_active = collisions(player_rectangle, obstacle_rectangle_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_surface, player_stand_rectangle)
        screen.blit(game_name_surface, game_name_rectangle)

        # Reset
        obstacle_rectangle_list.clear()
        player_rectangle.midbottom = (80, 300)
        player_gravity = 0

        if score == 0:
            screen.blit(game_message_surface, game_message_rectangle)
        else:
            score_message_surface = font.render(f'Your score: {score}', False, (111, 196, 169))
            score_message_rectangle = score_message_surface.get_rect(center=(400, 330))
            screen.blit(score_message_surface, score_message_rectangle)

    pygame.display.update()
    clock.tick(60)
