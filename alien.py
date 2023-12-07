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
        self.speed = 0.05

    def draw(self):
        """"Отрисовка пришельцев на экране"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """"Перемещение пришельцев"""
        self.y += self.speed
        self.rect.y = self.y