import sys
import pygame
import movements
from pygame.sprite import Group
from stats import Stats
from scores import Score
import pygame_menu
import pygame_menu.themes
import pygame.font
from gun import Gun
from alien import Alien, AlienLvl3

pygame.font.init()
pygame.init()

picture = pygame.image.load('images/icon.jpeg')
pygame.display.set_icon(picture)

ALIEN_LVL3_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ALIEN_LVL3_EVENT, 1000)

pygame.mixer.music.load('music/game_music.mp3')
pygame.mixer.music.play(-1)

music_paused = False #Флаг для отслеживания музыки


def toggle_music():
    global music_paused
    if music_paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
    music_paused = not music_paused


def game_over(screen):
    font = pygame.font.Font(None, 36)
    text_lines = ["Вы проиграли", "Вернуться в меню"]
    y_start = 300

    menu_rect = pygame.Rect(300, 400, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if menu_rect.collidepoint(mouse_pos):
                    return "menu"

        screen.fill((0, 0, 0))

        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(350, y_start + i * 100))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()


def run():
    screen = pygame.display.set_mode((700, 750))
    pygame.display.set_caption("Space guards")
    bg_color = (0, 0, 0)
    gun = Gun(screen)
    bullets = Group()
    aliens = Group()
    stats = Stats()
    score = Score(screen, stats)

    movements.create_army(screen, aliens, stats)

    paused = False

    def show_pause_menu():
        font = pygame.font.Font(None, 36)
        text_lines = ["Продолжить", "Вернуться в меню"]
        y_start = 300

        continue_rect = pygame.Rect(300, 300, 200, 50)
        menu_rect = pygame.Rect(300, 400, 200, 50)

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "continue"
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    if continue_rect.collidepoint(mouse_pos):
                        return "continue"
                    elif menu_rect.collidepoint(mouse_pos):
                        return "menu"

            screen.fill(bg_color)

            for i, line in enumerate(text_lines):
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(350, y_start + i * 100))
                screen.blit(text_surface, text_rect)

            pygame.display.flip()

    while True:
        if stats.guns_left <= 0:
            result = game_over(screen)
            if result == "menu":
                global game_state
                game_state = "menu"
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == ALIEN_LVL3_EVENT and stats.level >= 3:
                for _ in range(7):
                    new_alien = AlienLvl3(screen)
                    aliens.add(new_alien)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        result = show_pause_menu()
                        if result == "continue":
                            paused = False
                        elif result == "menu":
                            return
                    continue
                elif event.key == pygame.K_e:
                    pygame.mixer.music.pause()
                elif event.key == pygame.K_q:
                    pygame.mixer.music.unpause()

                movements.check_keydown_events(event, screen, gun, bullets)
            elif event.type == pygame.KEYUP:
                movements.check_keyup_events(event, gun)

        if not paused:
            gun.update_gun()
            bullets.update()
            for alien in aliens:
                alien.update()
            movements.check_collisions(screen, bullets, aliens, stats, score)
            movements.update_aliens(stats, screen, score, gun, aliens, bullets)

            if stats.level >= 3:
                movements.create_army(screen, aliens, stats)
                movements.update_aliens(stats, screen, score, gun, aliens, bullets)

            movements.update_screen(bg_color, screen, stats, score, gun, aliens, bullets)
        pygame.display.flip()


class Menu:
    def __init__(self, width, height):
        self.menu_width = width
        self.menu_height = height
        self.screen = pygame.display.set_mode((self.menu_width, self.menu_height))
        self.running = False
        self.main_menu = pygame_menu.Menu('Меню',
                                          self.menu_width,
                                          self.menu_height,
                                          theme=pygame_menu.themes.THEME_DARK)
        self.stats = Stats()  # Добавление атрибута stats

        self.main_menu.add.button('Начать игру', self.start_game)
        self.main_menu.add.button('Управление', self.show_controls)
        self.main_menu.add.button('Про что игра', self.show_inf)
        self.main_menu.add.button('Выход', pygame_menu.events.EXIT)

    def start_game(self):
        self.main_menu.disable()
        global game_state
        game_state = "playing"
        run()
        self.return_to_menu()  # Включаем меню обратно

    def show_controls(self):
        self.main_menu.disable()
        pygame.event.clear()
        pygame.display.set_caption("Управление")
        clock = pygame.time.Clock()

        text_lines = [
            "Движение вправо - A (английская раскладка)",
            "Движение влево - D (английская раскладка)",
            "Стрельба - пробел",
            "Нажмите esc для возврата в главное меню",
            "Нажмите esc во время игры, чтобы поставить игру на паузу",
            "e - пауза музыки, q - возобновить музыку (английская раскладка)",
            "Переключать состояние музыки можно только во время игры"
        ]

        font = pygame.font.Font(None, 28)
        line_height = font.get_height()
        total_height = line_height * len(text_lines)
        y_start = (self.menu_height - total_height) // 2

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.main_menu.enable()
                    return
            pygame.event.pump()

            self.screen.fill((0, 0, 0))

            for i, line in enumerate(text_lines):
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.menu_width // 2, y_start + i * line_height))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            clock.tick(60)

    def show_inf(self):
        self.main_menu.disable()
        pygame.event.clear()
        pygame.display.set_caption("Про что игра")
        clock = pygame.time.Clock()

        text_lines = [
            "Данная игра состоит из трех уровней",
            "Первые два уровня разминочные, а третий уже бесконечный",
            "Вам предстоит миссия по защите планеты",
            "В 1 и 2 уровнях нельзя пускать корабли за нижнюю границу экрана",
            "Потому что подмога еще не прибыла",
            "В 3 уровне уже можно",
            "Потому что вас есть кому прикрыть"
        ]

        font = pygame.font.Font(None, 28)
        line_height = font.get_height()
        total_height = line_height * len(text_lines)
        y_start = (self.menu_height - total_height) // 2

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.main_menu.enable()
                    return
            pygame.event.pump()

            self.screen.fill((0, 0, 0))

            for i, line in enumerate(text_lines):
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.menu_width // 2, y_start + i * line_height))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            clock.tick(60)

    def return_to_menu(self):
        self.main_menu.enable()
        global game_state
        game_state = "menu"

    def main(self):
        self.running = True
        while self.running:
            if game_state == "menu":
                self.main_menu.mainloop(self.screen)
            elif game_state == "playing":
                run()


if __name__ == "__main__":
    game_state = "menu"  # Изначально устанавливаем состояние в главное меню
    menu = Menu(700, 750)
    menu.main()
    pygame.quit()
