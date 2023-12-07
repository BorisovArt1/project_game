import pygame
from pygame.sprite import Sprite


class Life(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.image.load('images/life_image.png')
        self.rect = self.image.get_rect()
        self.screen = screen

    def output_life(self):
        self.screen.blit(self.image, self.rect)