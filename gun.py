import pygame


class Gun:
    def __init__(self, screen):
        """"Инициализация пушки"""

        self.screen = screen
        self.image = pygame.image.load('images/pixilart-drawing.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.movement_right = False
        self.movement_left = False

    def output(self):
        """"Отрисовка пушки"""

        self.screen.blit(self.image, self.rect)

    def update_gun(self):
        """"Обновление позиции пушки"""

        if self.movement_right and self.rect.right < self.screen_rect.right:
            self.center += 1.5
        elif self.movement_left and self.rect.left > 0:
            self.center -= 1.5

        self.rect.centerx = self.center

    def recreate_gun(self):
        """Пересоздание пушки"""
        self.center = self.screen_rect.centerx
