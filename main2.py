import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import random
import pygame.sprite.animation as animation
from PIL import Image
from math import sqrt
from time import time
from playsound import playsound

# Игрок
player = pygame.sprite.Sprite()

# Анимация ходьбы
walk_animation = animation.Animation()

# Анимация прыжка
jump_animation = animation.Animation()

# Текстура
texture = glGenTextures(1)

# Частицы
particles = []

# Игровой мир
world = []

# Флаги
is_jumping = False
is_falling = False
is_game_over = False

# Звук
jump_sound = pygame.mixer.Sound("jump.wav")
coin_sound = pygame.mixer.Sound("coin.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Время
start_time = time()

# Отрисовка куба
def draw_cube():
    glBegin(GL_QUADS)
    glVertex3f(1, 1, -1)
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    glEnd()

# Обновление игрового мира
def update_world():
    for block in world:
        block.update()
    for coin in world:
        coin.update()

# Отрисовка игрового мира
def draw_world():
    for block in world:
        block.draw()
    for coin in world:
        coin.draw()

# Обработка событий
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                is_jumping = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                is_jumping = False

# Обновление игры
def update():
    global is_falling, is_game_over, is_jumping

    update_world()

    # Прыжок
    if is_jumping and not is_falling:
        playsound(jump_sound)
        is_falling = True
        player.vel_y = 10

    # Падение
    if is_falling:
        player.vel_y -= 0.5
        player.rect.y += player.vel_y

        if player.rect.y > 400:
            is_falling = False
            player.rect.y = 400

    # Проверка столкновений
    for block in world:
        if player.rect.colliderect(block.rect):
            if player.vel_y > 0:
                player.rect.y = block.rect.top + 1
                is_falling = False
            elif player.vel_y < 0:
                player.rect.y = block.rect.bottom - player.rect.height
                is_jumping = False

    # Сбор монет
    for coin in world:
        if player.rect.colliderect(coin.rect):
            world.remove(coin)
            playsound(coin_sound)

    # Проверка конца игры
    if player.rect.y > 500:
        is_game_over = True
        playsound(game_over_sound)

# Отрисовка кадра
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_world()

    # Отрисовка игрока
    player.animation.update()
    screen.blit(player.image, player.rect)

    # Отрисовка частиц
    # ...

    glutSwapBuffers()

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("block.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

glutInit()
pygame.init()
glutCreateWindow("Пиратские Сокровища")
gluPerspective(45, 800/600, 0.1, 100)

# Загрузка текстуры
glBindTexture(GL_TEXTURE_2D, texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

# Инициализация игрока
player.image = pygame.image.load("player.png")
player.rect = player.image.get_rect()
player.animation = walk_animation
player.vel_y = 0

# Инициализация мира
for i in range(10):
    world.append(Block(i * 100, 400))
    world.append(Coin(random.randint(0, 800), random.randint(100, 400)))

while True:
    handle_events()
    update()
    render()

    # Отображение времени
    time_text = "Время: " + str(int(time() - start_time))
    font = pygame.font.SysFont("Arial", 24)
    text_surface = font.render(time_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))

# Отображение информации о конце игры
    if is_game_over:
        game_over_text = "Игра окончена!"
        font = pygame.font.SysFont("Arial", 48)
        text_surface = font.render(game_over_text, True, (255, 255, 255))
        screen.blit(text_surface, (200, 300))

    pygame.display.flip()