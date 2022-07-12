from random import random

import pygame

from .constants import Colors
from .player import Player


class Bullet(pygame.sprite.Sprite):
    surface: pygame.Surface

    speed: float
    radius: float
    lifespan: int

    center: pygame.Vector2
    direction: pygame.Vector2

    def __init__(self, surface: pygame.Surface, player: Player) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.speed = player.BulletStats.speed
        self.lifespan = player.BulletStats.lifespan
        self.radius = player.BulletStats.radius
        self.center = pygame.Vector2(player.center)
        self.direction = pygame.Vector2()
        self.direction.from_polar(
            (1, player.angle + (random() - 0.5) * player.BulletStats.precision)
        )
        player.update_speed(self.direction, -player.BulletStats.recoil)

    def draw(self) -> None:
        pygame.draw.circle(self.surface, Colors.Bullet, self.center, self.radius)

    def update(self) -> None:
        self.lifespan -= 1
        self.center += self.speed * self.direction
        self.draw()
