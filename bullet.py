import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, gun):
        """"Создание пули в позиции пушки"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 2, 12)
        self.color = 168, 230, 29
        self.speed = 3.5
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top
        self.y = float(self.rect.y)

    def update(self):
        """"Перемещение пули вверх"""
        self.y -= self.speed
        self.rect.y = self.y

    def drawing_bullet(self):
        """"Отрисовка пули на экране"""
        pygame.draw.rect(self.screen, self.color, self.rect)