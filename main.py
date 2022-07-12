import pygame

from game.bullet import Bullet
from game.constants import Colors
from game.helpers import check_quit_condition
from game.player import Player

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.init()
pygame.display.set_caption("Tank game")

player = Player(screen)
bullets = pygame.sprite.Group()

while True:
    pygame.time.delay(40)

    check_quit_condition()
    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
        if player.shooting_reload == 0:
            bullets.add(Bullet(screen, player))
            player.shooting_reload = player.BulletStats.cooldown
    if key[pygame.K_UP] or key[pygame.K_w]:
        player.update_speed(pygame.Vector2(0, -1))
    if key[pygame.K_LEFT] or key[pygame.K_a]:
        player.update_speed(pygame.Vector2(-1, 0))
    if key[pygame.K_DOWN] or key[pygame.K_s]:
        player.update_speed(pygame.Vector2(0, +1))
    if key[pygame.K_RIGHT] or key[pygame.K_d]:
        player.update_speed(pygame.Vector2(+1, 0))

    screen.fill(Colors.Background)

    for bullet in bullets:
        bullet.update()
        if bullet.lifespan == 0:
            bullets.remove(bullet)

    player.update()

    pygame.display.update()
