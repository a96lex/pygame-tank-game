from random import randint

import pygame

from .helpers import get_random_position_at_edge
from .player import Player
from .shooter import Shooter
from .constants import Colors


class Enemy(Shooter):
    idle_state: int

    def __init__(self, player: Player, idle_state: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.shooting_reload += idle_state + randint(0, 10)
        self.surface = player.surface
        self.target = player
        self.idle_state = idle_state
        self.center = get_random_position_at_edge(self.surface)

    def is_active(self) -> bool:
        return self.idle_state == 0

    def rotate(self) -> None:
        vMouse = pygame.Vector2(self.target.center)
        vCenter = pygame.Vector2(self.center)
        self.angle = pygame.Vector2().angle_to(vMouse - vCenter)

        rotated_point = [pygame.Vector2(p).rotate(self.angle) for p in self.cannon_rect]

        self.cannon_coords = [(vCenter + p) for p in rotated_point]


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
        radius = 4
        lifespan = 100
        precision = 98
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
        speed = 14
        radius = 7
        lifespan = 100
        precision = 91
        recoil = 3
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
    max_health = 200
    health = max_health

    class BulletStats:
        speed = 20
        radius = 15
        lifespan = 100
        precision = 95
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
        precision = 97
        recoil = 80
        color = Colors.EnemyBullet
        random_movement = False
        damage = 200
