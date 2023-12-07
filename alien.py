import random
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """"Класс одного пришельца"""

    def __init__(self, screen):
        """"Инициализация и установка начальной позиции"""
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/Alienp.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = 0.07

    def draw(self):
        """"Отрисовка пришельцев на экране"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """"Перемещение пришельцев"""
        self.y += self.speed
        self.rect.y = self.y
        if self.rect.bottom >= self.screen.get_height():
            self.kill()


class AlienLvl3(Sprite):
    image = pygame.image.load('images/alienLvl3.png')

    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.rect = AlienLvl3.image.get_rect()
        self.rect.x = random.randint(0, self.screen.get_width() - self.rect.width)
        self.rect.y = random.randint(-100, -self.rect.height)
        self.speed_y = random.uniform(0.05, 1)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > self.screen.get_height():
            self.kill()

    def reset_position(self):
        self.rect.x = random.randint(0, self.screen.get_width() - self.rect.width)
        self.rect.y = random.randint(-100, -self.rect.height)
        self.speed_y = random.uniform(0.05, 1)