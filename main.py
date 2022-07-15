from random import random
import pygame

from game.bullet import Bullet, Explosion
from game.constants import Colors
from game.helpers import (
    DelayedBoolean,
    DelayedValue,
    check_quit_condition,
    handle_collision_if_exist,
)
from game.levels import load_level
from game.player import Player
from game.upgrade_constants import UPGRADEABLE_STATS

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.init()
pygame.display.set_caption("Tank game")
pygame.font.init()
font = pygame.font.Font("assets/pixeloid-font/PixeloidMono-1G8ae.ttf", 32)

player = Player(screen)
player.load_stats()

lvl = 0
bullets = pygame.sprite.Group()
particles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
explosions = pygame.sprite.Group()


class Scenes:
    LEVEL = "level"
    UPGRADES = "upgrades"


class GameConfig:
    friendly_fire = False
    bouncy_bullets = False
    scene = Scenes.LEVEL


REST_BETWEEN_LEVELS = 50
score = 0
money = DelayedValue(0)

auto_fire = DelayedBoolean()
paused = DelayedBoolean()
while True:
    pygame.time.delay(40)

    check_quit_condition()

    key = pygame.key.get_pressed()

    if GameConfig.scene == Scenes.LEVEL:
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
                if random() > 0.6:
                    particles.add(Bullet(bullet))

                if bullet.from_player or GameConfig.friendly_fire:
                    for enemy in enemies:
                        hit_score = handle_collision_if_exist(bullet, enemy)
                        if hit_score:
                            explosions.add(Explosion(bullet))
                            score += hit_score
                            if enemy.health <= 0:
                                enemy.kill()
                                explosions.add(Explosion(enemy))
                            break

            if not bullet.from_player or GameConfig.friendly_fire:
                hit_score = handle_collision_if_exist(bullet, player)
                if hit_score:
                    explosions.add(Explosion(bullet))
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

        if player.health <= 0:
            GameConfig.scene = Scenes.UPGRADES
            bullets.empty()
            particles.empty()
            enemies.empty()
            explosions.empty()
            paused.force_update(False)
            auto_fire.force_update(False)
            money.force_update(money.value + score)

    elif GameConfig.scene == Scenes.UPGRADES:
        screen.fill(Colors.Background)

        stats = [v for k, v in UPGRADEABLE_STATS.__dict__.items() if k[0] != "_"]

        if key[pygame.K_x]:
            del player
            player = Player(screen)
            player.load_stats()
            GameConfig.scene = Scenes.LEVEL
            score = 0
            lvl = 0
            continue

        for idx, stat in enumerate(stats):
            key_idx = idx + 49  # 49 is 1
            stat_lvl = player.levels[stat]
            cost = int(stat_lvl**2)

            if (
                key[key_idx]
                and cost < money.value
                and money.can_update()
                and player.can_update(stat)
            ):
                money.update(money.value - cost)
                player.increase_stat_level(stat)

            screen.blit(
                font.render(f"Money: {money.value}", 5, Colors.UI),
                (10, 37),
            )

            if player.can_update(stat):
                screen.blit(
                    font.render(
                        f"{stat}: {stat_lvl}. Cost: {cost}. Press {idx} to upgrade",
                        5,
                        Colors.UI,
                    ),
                    (150, 240 + 35 * idx),
                )

            else:
                screen.blit(
                    font.render(
                        f"{stat}: {stat_lvl}. (Maximum level)",
                        5,
                        Colors.UI,
                    ),
                    (150, 240 + 35 * idx),
                )

            screen.blit(
                font.render(
                    f"Press x to exit",
                    5,
                    Colors.UI,
                ),
                (150, 600),
            )

    pygame.display.update()
