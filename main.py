import asyncio
from random import random
import pygame

from game.bullet import Bullet, Explosion
from game.constants import Colors
from game.game_data import GameConfig, GameStats, Scenes
from game.helpers import (
    DelayedBoolean,
    DelayedValue,
    check_quit_condition,
    handle_collision_if_exist,
    sanitize_text,
)
from game.levels import load_level
from game.player import Player
from game.screen_shake import ScreenShake
from game.text_renderer import render_text
from game.upgrade_constants import UPGRADEABLE_STATS

WIDTH, HEIGHT = 1280 * 0.8, 720 * 0.8


async def main():
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = pygame.surface.Surface((WIDTH, HEIGHT))
    screen_shake = ScreenShake()

    pygame.display.init()
    pygame.display.set_caption("Tank game")

    player = Player(screen)
    player.load_stats()

    game_stats = GameStats()
    game_stats.load_stats()

    lvl = 0
    bullets = pygame.sprite.Group()
    particles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    REST_BETWEEN_LEVELS = 50
    score = 0
    money = DelayedValue(game_stats.money)

    auto_fire = DelayedBoolean()
    paused = DelayedBoolean()

    while True:
        pygame.time.delay(40)

        check_quit_condition()

        key = pygame.key.get_pressed()

        if GameConfig.scene == Scenes.MENU:
            if key[pygame.K_x]:
                if player:
                    del player
                player = Player(screen)
                player.load_stats()
                GameConfig.scene = Scenes.LEVEL
                score = 0
                lvl = 0
                continue
            if key[pygame.K_c]:
                GameConfig.scene = Scenes.SHOP
                continue

            display.fill(Colors.UI)
            screen.fill(Colors.Background)
            render_text(screen, "Unnamed tank game", 2, 16, 3)
            render_text(screen, "Press x to start", 1, 16, 9)
            render_text(screen, "Press c to visit the shop", 1, 16, 10)
            render_text(
                screen,
                f"High score: {game_stats.high_score} - Highest Level: {game_stats.highest_level} - Money: {game_stats.money}",
                0,
                16,
                15,
            )

            if score:
                render_text(
                    screen,
                    f"last score: {score}",
                    0,
                    16,
                    14,
                )

        if GameConfig.scene == Scenes.LEVEL:
            if key[pygame.K_p]:
                paused.switch()
            if key[pygame.K_e]:
                auto_fire.switch()

            if paused:
                render_text(screen, "||", 2, 16, 9)
                render_text(screen, "press p to unpause", 1, 16, 11)

            else:
                display.fill(Colors.UI)
                screen.fill(Colors.Background)
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
                            screen_shake.shake(bullet)
                            score -= hit_score

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

                render_text(screen, f"Current level: {lvl}", 1, 1, 1, "left")
                render_text(screen, f"Score: {score}", 1, 1, 2, "left")

                if player.health <= 0:
                    GameConfig.scene = Scenes.MENU
                    bullets.empty()
                    particles.empty()
                    enemies.empty()
                    explosions.empty()
                    paused.force_update(False)
                    auto_fire.force_update(False)
                    screen_shake.stop()

                    if score > 0:
                        money.force_update(money.value + score)

                    game_stats.money = money.value
                    game_stats.high_score = max(game_stats.high_score, score)
                    game_stats.highest_level = max(game_stats.highest_level, lvl)

        elif GameConfig.scene == Scenes.SHOP:
            display.fill(Colors.UI)
            screen.fill(Colors.Background)

            stats = [v for k, v in UPGRADEABLE_STATS.__dict__.items() if k[0] != "_"]

            if key[pygame.K_m]:
                GameConfig.scene = Scenes.MENU
                continue

            for idx, stat in enumerate(stats):
                key_idx = idx + 49  # 49 is 1
                stat_lvl = player.levels[stat]
                cost = int((stat_lvl + 1) ** 2)

                if (
                    key[key_idx]
                    and cost <= money.value
                    and money.can_update()
                    and player.can_update(stat)
                ):
                    money.update(money.value - cost)
                    game_stats.money = money.value
                    player.increase_stat_level(stat)

                if player.can_update(stat):
                    upgrade_text = f"{sanitize_text(stat): <10}: {stat_lvl: <4}  Cost: {cost: <6} Press {idx+1} to upgrade"
                else:
                    upgrade_text = (
                        f"{sanitize_text(stat): <10}: {stat_lvl: <4}. (Maximum level)"
                    )

                render_text(screen, upgrade_text, 0, 16, idx + 8)

            render_text(screen, "Shop", 2, 16, 3)
            render_text(screen, f"Money: {game_stats.money}", 1, 16, 5)
            render_text(screen, "Press m to go to main menu", 1, 16, 17)

        display.blit(
            screen,
            pygame.Vector2(
                [
                    (display.get_width() - WIDTH) / 2,
                    (display.get_height() - HEIGHT) / 2,
                ]
            )
            + screen_shake.get_screen_offset(),
        )
        pygame.display.update()
        await asyncio.sleep(0)


asyncio.run(main())
