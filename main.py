import pygame
import random
import time
import os

pygame.init()

pygame.mixer.init()
jump_sound = pygame.mixer.Sound(os.path.join("jump.wav"))
gameover_sound = pygame.mixer.Sound(os.path.join("game_over.wav"))





player_stand = pygame.image.load(("standing.png"))
player_jump = pygame.image.load(("jumping.png"))
player_run1 = pygame.image.load(("running.png"))
player_run2 = pygame.image.load(("running2.png"))
player_shoot = pygame.image.load(("punch.png"))
enemy_image = pygame.image.load(("enemy.png"))
bullet_image = pygame.image.load(("fireball.png"))

class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.standing_frames = [player_stand]
            self.running_frames = [player_run1, player_run2]
            self.jump_frames = [player_jump]
            self.shoot_frame = player_shoot
            self.image = self.standing_frames[0]
            self.rect = self.image.get_rect()
            self.rect.center = (100, SCREEN_HEIGHT // 2)
            self.speed = 5
            self.jump_power = 0
            self.gravity = 0.8
            self.shooting = False
            self.is_jumping = False
            self.last_shot_time = 0  
            self.shoot_cooldown = 0.5  
            self.direction = 1  
            self.is_running = False
            self.max_health = 100
            self.health = self.max_health
            self.health_bar_surface = pygame.Surface((100, 10))
            self.health_bar_surface.fill((0, 0, 0))

        def jump(self):
            if not self.is_jumping:
                self.is_jumping = True
                self.jump_power = -12
                jump_sound.play()

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.jump()
            if pygame.sprite.spritecollide(self, enemies, False):
                self.health -= 10
                if self.health <= 0:
                    print("game over!")
                    gameover_sound.play()
                    running = False

                self.health_bar_surface.fill(0, 0, 0)
                health_bar_width = int(self.health / self.max_health * 100)
                pygame.draw.rect(self.health_bar_surface, (0, 255, 0), (0, 0, health_bar_width, 10))

            if self.is_jumping:
                self.rect.y += self.jump_power
                self.jump_power += self.gravity
                if self.rect.bottom >= SCREEN_HEIGHT:
                    self.rect.bottom = SCREEN_HEIGHT
                    self.is_jumping = False

            if keys[pygame.K_a]:
                self.rect.x -= self.speed
                self.direction = -1  
                self.is_running = True
            elif keys[pygame.K_d]:
                self.rect.x += self.speed
                self.direction = 1  
                self.is_running = True
            else:
                self.is_running = False  

        
            if self.is_running:
                if self.direction == 1:  
                    self.image = self.running_frames[(pygame.time.get_ticks() // 100) % 2]
                else:  
                    self.image = pygame.transform.flip(self.running_frames[(pygame.time.get_ticks() // 100) % 2], True, False)
            else:
                self.image = self.standing_frames[0]  

            if keys[pygame.K_e]:  
                current_time = time.time()
                if current_time - self.last_shot_time > self.shoot_cooldown:
                    self.shooting = True
                    self.image = self.shoot_frame
                    mouse_pos = pygame.mouse.get_pos()
                    bullet = Bullet(self.rect.center, mouse_pos)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    self.last_shot_time = current_time
            else:
                self.shooting = False

        def draw_health_bar(self, screen):
            screen.blit(self.health_bar_surface, (10, 10))

class Enemy(pygame.sprite.Sprite):
        def __init__(self, player):
            super().__init__()
            self.image = enemy_image
            self.rect = self.image.get_rect()
            self.player = player
            self.rect.center = (SCREEN_WIDTH, SCREEN_HEIGHT // 2)

        def attack(self, player):
            if self.rect.colliderect(player.rect):
                player.health -= 1

        def update(self):
            self.rect.x = pygame.math.lerp(self.rect.x, self.player.rect.x, 0.01)
            self.rect.y = pygame.math.lerp(self.rect.y, self.player.rect.y, 0.01)
            self.attack(player)

class Bullet(pygame.sprite.Sprite):
        def __init__(self, start_pos, target_pos):
            super().__init__()
            self.image = bullet_image
            self.rect = self.image.get_rect()
            self.rect.center = start_pos
            self.speed = 10
            self.target_pos = target_pos
            self.creation_time = time.time()  
            self.lifetime = 0.7  

        def update(self):
            current_time = time.time()
            if current_time - self.creation_time > self.lifetime:
                self.kill()
                return

            direction = pygame.math.Vector2(self.target_pos) - pygame.math.Vector2(self.rect.center)
            distance = direction.length()
            if distance != 0:
                direction /= distance
                self.rect.center += direction * self.speed

            if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
                self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.type = type
        self.image = pygame.image.load(("powerup_" + type + ".png"))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.duration = 5
    
    def update(self):
        if pygame.sprite.spritecollide(self, player):
            if self.type == "health":
                player.health += 20
                if player.health > player.max_health:
                    player.health = player.max_health
                self.kill()
        self.duration -= 1/60
        if self.duration <= 0:
            self.kill()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

if random.random() < 0.01:
    power_up_type = random.choice(["health", "Speed"])
    power_up = PowerUp(power_up_type, random.randint(0, SCREEN_WIDTH - 32), random.randint(0, SCREEN_HEIGHT - 32))
    all_sprites.add(power_up)

player = Player()

all_sprites.add(player)

running = True
next_enemy_time = time.time()
max_enemies = 2
clock = pygame.time.Clock()
while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if len(enemies) < max_enemies:
            if time.time() > next_enemy_time:
                enemy = Enemy(player)
                enemy.rect.x = random.choice([0, SCREEN_WIDTH])
                enemy.rect.y = random.choice([0, SCREEN_HEIGHT])
                enemies.add
                all_sprites.add(enemy)
                next_enemy_time = time.time() + 5

        all_sprites.update()

        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            for hit in hits:
                bullet.kill()
                enemies.remove(hit)
                all_sprites.remove(hit)
                for hit in hits:
                    hit.kill()


        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            print("Game Over")
            running = False
            gameover_sound.play()

        screen.blit(background_image, (0, 0))
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect)
            player.draw_health_bar(screen)

        hits = pygame.sprite.spritecollide(player, enemies, False)
        for hit in hits:
            player.health -= 1

        pygame.display.flip()

        clock.tick(60)

pygame.quit()