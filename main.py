import pygame
import random
from pygame.sprite import Sprite, Group
import pygame.font as font
import sys

background_image = pygame.image.load("bg.jpg")

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 600


is_jumping = False
is_falling = False
is_game_over = False

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Caffeine Escape")

player_image = pygame.image.load("player.png").convert_alpha()
block_image = pygame.image.load("block.png").convert_alpha()
coin_image = pygame.image.load("coin.png").convert_alpha()
enemy_image = pygame.image.load("enemy.png")
punch_frames = [pygame.image.load("punch.png")]
kick_frames = [pygame.image.load("kick.png")]
jump_sound = pygame.mixer.Sound("jump.wav")
coin_sound = pygame.mixer.Sound("coin.mp3")
game_over_sound = pygame.mixer.Sound("game_over.wav")

class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.vel_y = 0
        self.move_left = False
        self.move_right = False
        self.attack_area = None

    def handle_attack(self):
        attack_width = 50
        attack_height = 30
        self.attack_area = pygame.Rect(self.rect.x + self.rect.width // 2 - attack_width // 2,
                                       self.rect.y,
                                       attack_width,
                                       attack_height)

    def check_attack_collisions(self, enemy_group):
        if self.attack_area is not None:
            collided_enemies = pygame.sprite.spritecollide(self.attack_area, enemy_group, False)
            for enemy in collided_enemies:
                enemy.health -= 1
                enemy_hit_anim = True

    def move(self, dx):
        if self.rect.left + dx >= 0 and self.rect.right + dx <= SCREEN_WIDTH:
            self.rect.x += dx

    def update(self):
        global is_jumping, is_falling

        if is_jumping and not is_falling:
            jump_sound.play()
            is_falling = False
            self.vel_y = -7

            self.rect.y += self.vel_y

        elif is_falling:
            self.vel_y += 0.5
            self.rect.y += self.vel_y

            if self.rect.bottom >= SCREEN_HEIGHT:
                is_falling = False
                self.rect.bottom = SCREEN_HEIGHT

        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.move(-5)
            elif keys[pygame.K_d]:
                self.move(5)

        for block in block_group:
            if self.rect.colliderect(block.rect):
                if self.vel_y > 0:
                    self.rect.bottom = block.rect.top
                    is_falling = False
                elif self.vel_y < 0:
                    self.rect.top = block.rect.bottom
                    is_jumping = False

        for coin in coin_group:
            if self.rect.colliderect(coin.rect):
                coin_group.remove(coin)
                coin_sound.play()

        if self.rect.bottom >= SCREEN_HEIGHT:
            is_game_over = True
            game_over_sound.play()

class Enemy(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 3
        self.vel_x = 1
        self.move_direction = 1
        enemy_group.add(Enemy(100, 300))
    def update(self):
        self.rect.x += self.vel_x * self.move_direction
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.move_direction *= -1
        if self.health <= 0:
            self.kill()
        elif self.enemy_hit_anim:
            self.enemy_hit_anim = False

player_hit_anim = False
player_hit_frame = 0
enemy_hit_anim = False
enemy_hit_frame = 0

def play_hit_animation(sprite, animation_frames, frame_duration):
    global player_hit_frame, enemy_hit_frame
    if sprite.hit_anim:
        sprite.hit_frame = (sprite.hit_frame + 1) % len(animation_frames)
        screen.blit(animation_frames[sprite.hit_frame], sprite.rect)
        pygame.time.wait(frame_duration)

class Block(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = block_image
        self.rect = self.image.get_rect(topleft=(x, y))


class Coin(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = random.uniform(-2, 2)  
        self.vel_y = random.uniform(-1, 1)  

    def update(self):
        self.rect.x += self.vel_x  
        self.rect.y += self.vel_y

        if self.rect.left < 0:
            self.vel_x *= -1
        elif self.rect.right > SCREEN_WIDTH:
            self.vel_x *= -1

        if self.rect.top < 0:
            self.vel_y *= -1
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.vel_y *= -1


player = Player()
block_group = Group()
coin_group = Group()
enemy_group = Group()

player_hit_frames = []
enemy_hit_frames = []
animation_frames = None
frame_duration = 50

for i in range(10):
    block_group.add(Block(i * 100, 400))
    coin_group.add(Coin(random.randint(0, SCREEN_WIDTH - 50), random.randint(100, 400)))

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                is_jumping = True

    if not is_falling:
        is_jumping = False
    player.update()
    enemy_group.update()
    enemy_hit = pygame.sprite.spritecollide(player.attack_area, enemy_group, False)
    if pygame.mouse.get_pressed()[0]: 
        if player.is_punching:  
            player.is_punching = True
        else:
            player.is_punching = True 
            player.is_kicking = False  
    else:
        player.is_punching = False  

    if not player.is_punching and pygame.mouse.get_pressed()[2]:  
        if player.is_kicking:  
            player.is_kicking = True
        else:
            player.is_kicking = True  
            player.is_punching = False  
    else:
        player.is_kicking = False  
    if enemy_hit:
        for enemy in enemy_hit:
            enemy.health -= 1 
            enemy_hit_anim = True

    play_hit_animation(player, player_hit_frames, 50)
    play_hit_animation(enemy, enemy_hit_frames, 50)

    screen.blit(background_image, (0, 0))

    
    block_group.draw(screen)
    coin_group.draw(screen)
    screen.blit(player.image, player.rect)

    
    pygame.display.flip()

   
    clock.tick(60) 

    is_jumping = False


    player_punch_frame = 0
    player_kick_frame = 0
    punch_frames = [pygame.image.load("punch.png")]
    kick_frames = [pygame.image.load("kick.png")]

    def play_attack_animation(animation_frames, frame_duration):
            global player_punch_frame, player_kick_frame
    if player.is_punching:
            player.punch_frame = (player.punch_frame + 1) % len(animation_frames)
            screen.blit(animation_frames[player.punch_frame], player.rect)
    elif player.is_kicking:
            player.kick_frame = (player.kick_frame + 1) % len(animation_frames)
            screen.blit(animation_frames[player.kick_frame], player.rect)
    pygame.time.wait(frame_duration)