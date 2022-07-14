from random import random
from typing import Tuple

import pygame

from .player import Player
from .shooter import Shooter


from .constants import Colors, SpriteWidth


class Bullet(pygame.sprite.Sprite):
    # Bullets can also spawn bullets (particles)
    class BulletStats:
        speed = 2
        radius = 1.5
        lifespan = 40
        precision = 0
        recoil = 2
        cooldown = 0
        color = None
        random_movement = True
        damage = 0

    def __init__(self, shooter: Shooter, bouncy: bool = False) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.surface = shooter.surface
        self.bouncy = bouncy

        self.color = shooter.BulletStats.color or shooter.color
        self.speed = shooter.BulletStats.speed
        self.lifespan = shooter.BulletStats.lifespan
        self.radius = shooter.BulletStats.radius
        self.damage = shooter.BulletStats.damage

        self.center = pygame.Vector2(shooter.center)
        self.direction = pygame.Vector2()
        self.random_movement = shooter.BulletStats.random_movement

        self.from_player = isinstance(shooter, Player)

        if hasattr(shooter, "angle"):
            angle = shooter.angle
        else:
            angle = random() * 360

        self.direction.from_polar(
            (1, angle + (random() - 0.5) * shooter.BulletStats.precision)
        )
        self.direction.normalize_ip()

        self.center += self.direction * (shooter.radius + shooter.BulletStats.radius)

        if hasattr(shooter, "update_speed"):
            shooter.update_speed(self.direction, -shooter.BulletStats.recoil)

    def draw(self) -> None:
        pygame.draw.circle(
            self.surface, self.color, self.center, self.radius, SpriteWidth
        )

    def bounce(self) -> None:
        if (
            self.center.x + self.speed > self.surface.get_width() - self.radius
            or self.center.x + self.speed < 0 + self.radius
        ):
            self.direction.x *= -1
        if (
            self.center.y + self.speed > self.surface.get_height() - self.radius
            or self.center.y + self.speed < 0 + self.radius
        ):
            self.direction.y *= -1

    def update(self) -> None:
        self.lifespan -= 1
        if self.bouncy:
            self.bounce()
        self.center += self.speed * self.direction
        if self.random_movement:
            self.center.x += random() * self.speed
            self.center.y += random() * self.speed
        self.draw()


class Explosion(Bullet):
    color = Colors.UI

    def __init__(self, shooter: Shooter) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.radius = shooter.radius
        self.surface = shooter.surface
        self.center = shooter.center
        self.lifespan = 10

    def update(self) -> None:
        self.lifespan -= 1
        self.radius *= 1.05

        if self.lifespan == 0:
            self.kill()

        self.radius += 1
        self.draw()
