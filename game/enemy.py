from typing import List
from random import randint
import pygame


from .player import Player
from .shooter import Shooter
from .constants import Colors


class Enemy(Shooter):
    surface: pygame.Surface = None

    cannon_coords: List[pygame.Vector2]
    center: pygame.Vector2
    radius = 20

    acceleration = 1
    speed = pygame.Vector2(0, 0)
    max_speed = 5
    angle = 0

    cannon_rect = [
        [5, 15],
        [5, -15],
        [40, -15],
        [40, 15],
    ]

    shooting_reload = 0

    class BulletStats:
        speed = 20
        radius = 6
        lifespan = 100
        precision = 30
        recoil = 5
        cooldown = 20
        color = Colors.EnemyBullet
        random_movement = False

    def __init__(self, player: Player) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.surface = player.surface
        self.target = player
        width = self.surface.get_width()
        height = self.surface.get_height()
        p = randint(0, width + width + height + height)
        center = pygame.Vector2()
        if p < (width + height):
            if p < width:
                center.x = p
                center.y = 0
            else:
                center.x = width
                center.y = p - width
        else:
            p = p - (width + height)
            if p < width:
                center.x = width - p
                center.y = height
            else:
                center.x = 0
                center.y = height - (p - width)
        self.center = center

    def rotate(self) -> None:
        vMouse = pygame.Vector2(self.target.center)
        vCenter = pygame.Vector2(self.center)
        self.angle = pygame.Vector2().angle_to(vMouse - vCenter)

        rotated_point = [pygame.Vector2(p).rotate(self.angle) for p in self.cannon_rect]

        self.cannon_coords = [(vCenter + p) for p in rotated_point]

    def update(self) -> None:
        self.shooting_reload = max(0, self.shooting_reload - 1)
        self.update_speed()
        self.move()
        self.rotate()
        self.draw()


class Sniper(Enemy):
    radius = 15
    acceleration = 0.5
    max_speed = 2
    cannon_rect = [
        [5, 10],
        [5, -10],
        [40, -8],
        [40, 8],
    ]
    cooldown = 30

    class BulletStats:
        speed = 30
        radius = 3
        lifespan = 100
        precision = 5
        recoil = 3
        color = Colors.EnemyBullet
        random_movement = False
        damage = 80


class Shotgun(Enemy):
    radius = 20
    acceleration = 2
    max_speed = 3
    cannon_rect = [
        [5, 15],
        [5, -15],
        [30, -20],
        [30, 20],
    ]
    cooldown = 4

    class BulletStats:
        speed = 20
        radius = 7
        lifespan = 100
        precision = 30
        recoil = 2
        color = Colors.EnemyBullet
        random_movement = False
        damage = 30


class ShotgunBoss(Enemy):
    radius = 30
    acceleration = 2
    max_speed = 4
    cannon_rect = [
        [5, 20],
        [5, -20],
        [40, -25],
        [40, 25],
    ]
    cooldown = 10
    max_health = 400
    health = max_health

    class BulletStats:
        speed = 20
        radius = 15
        lifespan = 100
        precision = 18
        recoil = 6
        color = Colors.EnemyBullet
        random_movement = False
        damage = 100


class Bomber(Enemy):
    radius = 22
    acceleration = 3
    max_speed = 2
    cannon_rect = [
        [5, 20],
        [5, -20],
        [30, -20],
        [30, 20],
    ]
    cooldown = 30
    max_health = 150
    health = max_health

    class BulletStats:
        speed = 15
        radius = 20
        lifespan = 100
        precision = 10
        recoil = 80
        color = Colors.EnemyBullet
        random_movement = False
        damage = 200
