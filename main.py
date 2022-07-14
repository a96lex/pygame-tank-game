from random import random
import pygame

from game.bullet import Bullet, Explosion
from game.constants import Colors
from game.helpers import DelayedBoolean, check_quit_condition, handle_collision_if_exist
from game.levels import load_level
from game.player import Player

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.init()
pygame.display.set_caption("Tank game")
pygame.font.init()
font = pygame.font.Font("assets/pixeloid-font/PixeloidMono-1G8ae.ttf", 32)

player = Player(screen)

lvl = 0
bullets = pygame.sprite.Group()
particles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
explosions = pygame.sprite.Group()


class GameConfig:
    friendly_fire = False
    bouncy_bullets = False


REST_BETWEEN_LEVELS = 50
score = 0

auto_fire = DelayedBoolean()
paused = DelayedBoolean()
while True:
    pygame.time.delay(40)

    check_quit_condition()

    key = pygame.key.get_pressed()

    if key[pygame.K_p]:
        paused.switch()
    if key[pygame.K_e]:
        auto_fire.switch()

    if paused:
        continue

    if auto_fire or key[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
        if player.shooting_reload == 0:
            player.shoot()
            bullets.add(Bullet(player, GameConfig.bouncy_bullets))
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
            bullet.kill()
        else:
            if random() > 0.9:
                particles.add(Bullet(bullet))

            if bullet.from_player or GameConfig.friendly_fire:
                for enemy in enemies:
                    hit_score = handle_collision_if_exist(bullet, enemy)
                    if hit_score:
                        explosions.add(Explosion(bullet))
                        if enemy.health < 0:
                            enemy.kill()
                            explosions.add(Explosion(enemy))
                        break
                    else:
                        score += hit_score

        if not bullet.from_player or GameConfig.friendly_fire:
            hit_score = handle_collision_if_exist(bullet, player)
            if hit_score:
                explosions.add(Explosion(bullet))
            else:
                score += hit_score

    for enemy in enemies:
        enemy.update()
        if enemy.is_active() and enemy.shooting_reload == 0:
            enemy.shoot()
            bullets.add(Bullet(enemy, GameConfig.bouncy_bullets))

    player.update()

    for explosion in explosions:
        explosion.update()

    if not enemies:
        enemies = load_level(lvl, player, REST_BETWEEN_LEVELS)
        lvl += 1

    screen.blit(
        font.render(f"Current level: {lvl}", 5, Colors.UI),
        (10, 5),
    )
    screen.blit(
        font.render(f"Score: {score}", 5, Colors.UI),
        (10, 37),
    )

    pygame.display.update()
