from random import random
from typing import Tuple

import pygame


from .player import Player
from .constants import SpriteWidth


class Bullet(pygame.sprite.Sprite):
    surface: pygame.Surface

    speed: float
    radius: float
    lifespan: int
    color: Tuple[int, int, int]

    center: pygame.Vector2
    direction: pygame.Vector2

    from_player: bool
    random_movement: bool

    # Bullets can also spawn bullets (particles)
    class BulletStats:
        speed = 2
        radius = 4
        lifespan = 40
        precision = 0
        recoil = 2
        cooldown = 0
        color = None
        random_movement = True

    def __init__(self, shooter: Player) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.surface = shooter.surface

        self.color = shooter.BulletStats.color or shooter.color
        self.speed = shooter.BulletStats.speed
        self.lifespan = shooter.BulletStats.lifespan
        self.radius = shooter.BulletStats.radius

        self.center = pygame.Vector2(shooter.center)
        self.direction = pygame.Vector2()
        self.random_movement = shooter.BulletStats.random_movement

        if hasattr(shooter, "angle"):
            angle = shooter.angle
        else:
            angle = random() * 360

        self.direction.from_polar(
            (1, angle + (random() - 0.5) * shooter.BulletStats.precision)
        )

        if hasattr(shooter, "update_speed"):
            shooter.update_speed(self.direction, -shooter.BulletStats.recoil)

    def draw(self) -> None:
        pygame.draw.circle(
            self.surface, self.color, self.center, self.radius, SpriteWidth
        )

    def update(self) -> None:
        self.lifespan -= 1
        self.center += self.speed * self.direction
        if self.random_movement:
            self.center.x += random() * self.speed
            self.center.y += random() * self.speed
        self.draw()
