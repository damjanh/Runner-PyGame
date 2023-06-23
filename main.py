import random

import pygame
from sys import exit
from random import choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

    def reset(self):
        self.gravity = 0
        self.rect.bottom = 300


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()
        if obstacle_type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/enemy/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/enemy/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            start_pos_y = 210
        else:
            snail_frame_1 = pygame.image.load('graphics/enemy/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/enemy/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            start_pos_y = 300

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), start_pos_y))

    def animate(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = font.render(f'{int(current_time / 1000)}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return int(current_time / 1000)


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.7)
bg_music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 2)
player_stand_rectangle = player_stand_surface.get_rect(center=(400, 200))

# Text
game_name_surface = font.render('Runner', False, (111, 196, 169))
game_name_rectangle = game_name_surface.get_rect(center=(400, 80))

game_message_surface = font.render("Press ENTER to start!", False, (111, 196, 169))
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
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                start_time = pygame.time.get_ticks()
        else:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(obstacle_type=choice(['fly', 'snail', 'snail'])))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_surface, player_stand_rectangle)
        screen.blit(game_name_surface, game_name_rectangle)

        # Reset
        player.sprite.reset()

        if score == 0:
            screen.blit(game_message_surface, game_message_rectangle)
        else:
            score_message_surface = font.render(f'Your score: {score}', False, (111, 196, 169))
            score_message_rectangle = score_message_surface.get_rect(center=(400, 330))
            screen.blit(score_message_surface, score_message_rectangle)

    pygame.display.update()
    clock.tick(60)
