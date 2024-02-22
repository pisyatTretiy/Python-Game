import pygame
import random

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

screen_width = 800
screen_height = 600

class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.bullets = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()  

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > 500:  
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            self.last_shot = current_time

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed

        if self.rect.top < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height // 2)
        self.speed = random.randint(1, 3)
        self.health = 3 

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > screen_height:
            self.rect.top = 0
            self.rect.x = random.randint(0, screen_width - self.rect.width)
        if pygame.sprite.spritecollide(self, player.bullets, True):
            self.health -= 1
            if self.health <= 0:
                self.kill()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

background = pygame.image.load("bg.jpg")
background = pygame.transform.scale(background, (800, 600)) 

max_screen_size = (1024, 768)

if background.get_width() > max_screen_size[0] or background.get_height() > max_screen_size[1]:
    background = pygame.transform.scale(background, max_screen_size)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Escape from Caffeine Lab")
clock = pygame.time.Clock()
player = Robot()
all_sprites.add(player)

powerup_group = pygame.sprite.Group()
powerup_spawn_timer = random.randint(5000, 10000)  

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    if len(enemies) < 5:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    hits = pygame.sprite.groupcollide(enemies, player.bullets, True, True)
    for enemy in hits:
        enemy_type = enemy.type
        if enemy_type == "basic":
            player.score += 100
        elif enemy_type == "elite":
            player.score += 200
        elif enemy_type == "boss":
            player.score += 500
        else:
            print(f"Unknown enemy type: {enemy_type}")
        enemy.kill()

    for powerup in powerup_group:
        if pygame.sprite.collide_rect(player, powerup):
            apply_powerup_effect(player, powerup)
            powerup.kill()
        def apply_powerup_effect(player, powerup):
            powerup_type = powerup.type
            if powerup_type == "shield":
                player.invicible = True
                pygame.time.delay(8000)
                player.invicible = False
            elif powerup_type == "multishot":
                player.multishot_active = True
                player.multishot_duration = 5000
                player.multishot_count = 3
            else:
                print(f"Unknown powerUp type: {powerup_type}")
            
            def shoot(self):
                if self.multishot_active:
                    for _ in range(self.multishot_count + 1):
                        bullet = Bullet(self.rect.centerx, self.rect.top)
                        bullet.rect.x -= (self.multishot_count - 1) * 10
                        self.bullets.add(bullet)
                    self.multishot_duration -= 10
                if self.multishot_duration <= 0:
                    self.multishot_active = False
                else:
                    print("Error")
                player.shoot = shoot

    if pygame.time.get_ticks() > powerup_spawn_timer:
        powerup = PowerUp()  
        powerup_group.add(powerup)
        all_sprites.add(powerup)
        powerup_spawn_timer = pygame.time.get_ticks() + random.randint(5000, 10000)

    class PowerUp(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((20, 20))
            self.image.fill((0, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, screen_width = self.rect.width)
            self.rext.y = random.randint(0, screen_height // 2)
            self.type = random.choice(["speed", "fire_rate"])

        def update(self):
            self.rect.y += 1
            if self.rect.bottom > screen_height:
                self.kill()
            
        def apply_effect(self, player):
            if self.type == "speed":
                player.speed += 2
                pygame.time.delay(5000)
                player.speed -= 2
            elif self.type == "fire_rate":
                player.last_shot -= 200
                pygame.time.delay(3000)
                player.last_shot += 200


    screen.fill(white)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

