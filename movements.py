import pygame
import sys
import bullet
from bullet import Bullet
from alien import Alien, AlienLvl3
import time
from stats import Stats


def update_screen(bg_color, screen, stats, score, gun, aliens, bullets):
    """"Обновление экрана"""
    screen.fill(bg_color)
    score.drawing_level()
    score.show_score()
    for bullet_s in bullets.sprites():
        bullet_s.drawing_bullet()
    gun.output()
    aliens.draw(screen)
    pygame.display.flip()


def update_bullets(screen, stats, score, aliens, bullets):
    """"Обновление позиции пуль"""
    bullets.update()
    for bullet_s in bullets.copy():
        if bullet_s.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.value_score += 5 * len(aliens)
        score.drawing_score()
        checking_record(stats, score)
        score.drawing_lifes()
    if not aliens:
        stats.level_up()
        create_army(screen, aliens, stats)


def destroying_gun(stats, screen, score, gun, aliens, bullets):
    """Столкновение пушки и армии"""
    if stats.guns_left > 0:
        stats.guns_left -= 1
        score.drawing_lifes()
        aliens.empty()
        bullets.empty()
        create_army(screen, aliens, stats)
        gun.recreate_gun()
        pygame.display.flip()
        pygame.time.wait(500)
    else:
        stats.continuing_game = False
        sys.exit()


def update_aliens(stats, screen, score, gun, aliens, bullets):

    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        alien.update()
        if stats.level < 3 and alien.rect.bottom >= screen_rect.bottom:
            destroying_gun(stats, screen, score, gun, aliens, bullets)
            break

    if pygame.sprite.spritecollideany(gun, aliens):
        destroying_gun(stats, screen, score, gun, aliens, bullets)


def checking_low_line(stats, screen, score, gun, aliens, bullets):
    """Проверка достижения армии нижней части экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            destroying_gun(stats, screen, score, gun, aliens, bullets)
            break


def check_collisions(screen, bullets, aliens, stats, score):
    collections = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collections:
        for aliens in collections.values():
            stats.value_score += 10 * len(aliens)
            score.drawing_score()
            checking_record(stats, score)

    if len(aliens) == 0:
        stats.level_up()
        create_army(screen, aliens, stats)


def create_army(screen, aliens, stats):
    if stats.level < 3:
        alien = Alien(screen)
        alien_width = alien.rect.width
        number_of_aliens_x = 10  # Количество пришельцев в длину
        alien_height = alien.rect.height
        number_of_aliens_y = 6  # Количество пришельцев в высоту

        # Ширина и высота армии пришельцев
        army_width = number_of_aliens_x * alien_width
        army_height = number_of_aliens_y * alien_height

        # Определение начальной позиции армии пришельцев, чтобы она была посередине экрана
        start_x = (screen.get_width() - army_width) // 2
        start_y = 100  # Начальная высота армии пришельцев

        for row_number in range(number_of_aliens_y):
            for alien_number in range(number_of_aliens_x):
                alien = Alien(screen)
                alien.x = start_x + alien_width * alien_number
                alien.y = start_y + alien_height * row_number
                alien.rect.x = alien.x
                alien.rect.y = alien.y
                aliens.add(alien)

    else:
        while len(aliens) < 7:
            new_alien = AlienLvl3(screen)
            alien_collides = any(new_alien.rect.colliderect(alien.rect) for alien in aliens)
            if not alien_collides:
                aliens.add(new_alien)


def checking_record(stats, score):
    """Проверка рекорда"""
    if stats.value_score > stats.record:
        stats.record = stats.value_score
        score.drawing_record()
        with open('txt_files/record.txt', 'w') as file:
            file.write(str(stats.record))


def check_keydown_events(event, screen, gun, bullets):
    """Обработка нажатий клавиш."""
    if event.key == pygame.K_d:
        gun.movement_right = True
    elif event.key == pygame.K_a:
        gun.movement_left = True
    elif event.key == pygame.K_SPACE:
        new_bullet = Bullet(screen, gun)
        bullets.add(new_bullet)


def check_keyup_events(event, gun):
    """Обработка отпускания клавиш."""
    if event.key == pygame.K_d:
        gun.movement_right = False
    elif event.key == pygame.K_a:
        gun.movement_left = False
