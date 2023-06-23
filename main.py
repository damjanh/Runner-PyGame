import pygame
from sys import exit


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = font.render(f'{int(current_time / 1000)}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return int(current_time / 1000)


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

snail_start_pos_x = 800
snail_surface = pygame.image.load('graphics/enemy/snail1.png').convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom=(snail_start_pos_x, 300))

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 2)
player_stand_rectangle = player_stand_surface.get_rect(center=(400, 200))

game_name_surface = font.render('Runner', False, (111, 196, 169))
game_name_rectangle = game_name_surface.get_rect(center=(400, 80))

game_message_surface = font.render("Press SPACE to start!", False, (111, 196, 169))
game_message_rectangle = game_message_surface.get_rect(center=(400, 330))

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
                snail_rectangle.left = 800
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        snail_rectangle.left -= 4
        if snail_rectangle.right <= 0:
            snail_rectangle.left = snail_start_pos_x
        screen.blit(snail_surface, snail_rectangle)

        # Player
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300
        screen.blit(player_surface, player_rectangle)

        # Collision
        if snail_rectangle.colliderect(player_rectangle):
            game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_surface, player_stand_rectangle)
        screen.blit(game_name_surface, game_name_rectangle)

        if score == 0:
            screen.blit(game_message_surface, game_message_rectangle)
        else:
            score_message_surface = font.render(f'Your score: {score}', False, (111, 196, 169))
            score_message_rectangle = score_message_surface.get_rect(center=(400, 330))
            screen.blit(score_message_surface, score_message_rectangle)

    pygame.display.update()
    clock.tick(60)
