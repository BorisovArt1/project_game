from pygame.sprite import Group
from life import Life

import pygame.font

pygame.font.init()


class Score:
    """Вывод игровой информации"""

    def __init__(self, screen, stats):
        """Инициализация подсчета очков"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = 168, 230, 29
        self.font = pygame.font.Font(None, 28)
        self.drawing_score()
        self.drawing_record()
        self.drawing_lifes()

    def drawing_score(self):
        """Преобразование текста счета в графическое изображение"""
        self.score_image = self.font.render('Score: ' + str(self.stats.value_score), True, 'WHITE',
                                            (0, 0, 0))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 40
        self.score_rect.top = 20

    def drawing_record(self):
        """Преобразование рекорда в графическое изображение"""
        self.record_image = self.font.render('Record: ' + str(self.stats.record), True, 'WHITE',
                                             (0, 0, 0))
        self.record_rect = self.record_image.get_rect()
        self.record_rect.centerx = self.screen_rect.centerx
        self.record_rect.top = self.screen_rect.top + 20

    def drawing_lifes(self):
        """Количество жизней"""
        self.lifes = Group()
        for life_number in range(self.stats.guns_left):
            life = Life(self.screen)
            life.rect.x = 15 + life_number * life.rect.width
            life.rect.y = 20
            self.lifes.add(life)

    def drawing_level(self):
        """Преобразование текста уровня в графическое изображение"""
        self.level_image = self.font.render('Level: ' + str(self.stats.level), True, 'WHITE',
                                            (0, 0, 0))
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 40
        self.level_rect.top = self.score_rect.top + 20

    def show_score(self):
        """Отображение счета на экране"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.record_image, self.record_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.lifes.draw(self.screen)



