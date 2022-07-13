from random import random
import pygame

from game.bullet import Bullet
from game.constants import Colors
from game.helpers import check_quit_condition, cirlce_collision
from game.levels import load_level
from game.player import Player

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.init()
pygame.display.set_caption("Tank game")

player = Player(screen)

lvl = 0
enemies = load_level(lvl, player)

bullets = pygame.sprite.Group()
particles = pygame.sprite.Group()

while True:
    pygame.time.delay(40)

    check_quit_condition()
    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
        if player.shooting_reload == 0:
            player.shoot()
            bullets.add(Bullet(player))
    if key[pygame.K_UP] or key[pygame.K_w]:
        player.update_speed(pygame.Vector2(0, -1))
    if key[pygame.K_LEFT] or key[pygame.K_a]:
        player.update_speed(pygame.Vector2(-1, 0))
    if key[pygame.K_DOWN] or key[pygame.K_s]:
        player.update_speed(pygame.Vector2(0, +1))
    if key[pygame.K_RIGHT] or key[pygame.K_d]:
        player.update_speed(pygame.Vector2(+1, 0))

    screen.fill(Colors.Background)

    for particle in particles:
        particle.update()
        if particle.lifespan == 0:
            particles.remove(particle)

    for bullet in bullets:
        bullet.update()
        if bullet.lifespan == 0:
            bullets.remove(bullet)
        else:
            if random() > 0.9:
                particles.add(Bullet(bullet))

        if bullet.from_player:
            for enemy in enemies:
                collided, direction = cirlce_collision(enemy, bullet)
                if collided:
                    enemy.take_damage(bullet.damage, direction)
                    bullets.remove(bullet)
        else:
            collided, direction = cirlce_collision(player, bullet)
            if collided:
                player.take_damage(bullet.damage, direction)
                bullets.remove(bullet)

    for enemy in enemies:
        enemy.update()
        if enemy.shooting_reload == 0:
            enemy.shoot()
            bullets.add(Bullet(enemy))

    player.update()

    if not enemies:
        lvl += 1
        enemies = load_level(lvl, player)

    pygame.display.update()
