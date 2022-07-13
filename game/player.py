from typing import List

import pygame

from .constants import Colors, SpriteWidth


class Player(pygame.sprite.Sprite):
    surface: pygame.Surface = None

    cannon_coords: List[pygame.Vector2]
    center: pygame.Vector2
    radius = 40

    acceleration = 3
    speed = pygame.Vector2(0, 0)
    max_speed = 10
    angle = 0

    cannon_rect = [
        [10, 20],
        [10, -20],
        [60, -20],
        [60, 20],
    ]

    shooting_reload = 0

    class BulletStats:
        speed = 20
        radius = 10
        lifespan = 100
        precision = 10
        recoil = 5
        cooldown = 20
        color = Colors.PlayerBullet
        random_movement = False

    def __init__(self, surface: pygame.Surface) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.center = pygame.Vector2(surface.get_width() / 2, surface.get_height() / 2)

    def update_speed(self, dir: pygame.Vector2, magnitude=None) -> None:
        if not magnitude:
            magnitude = self.acceleration

        self.speed = pygame.Vector2(
            [
                max(-self.max_speed, min(self.max_speed, a + b))
                for a, b in zip(self.speed, dir * magnitude)
            ]
        )

    def move_cannon(self) -> None:
        self.center += self.speed
        self.speed *= 0.9

    def rotate_cannon(self) -> None:
        vMouse = pygame.Vector2(pygame.mouse.get_pos())
        vCenter = pygame.Vector2(self.center)
        self.angle = pygame.Vector2().angle_to(vMouse - vCenter)

        rotated_point = [pygame.Vector2(p).rotate(self.angle) for p in self.cannon_rect]

        self.cannon_coords = [(vCenter + p) for p in rotated_point]

    def draw(self) -> None:
        pygame.draw.polygon(self.surface, Colors.Background, self.cannon_coords)
        pygame.draw.polygon(
            self.surface, Colors.Player, self.cannon_coords, SpriteWidth
        )
        pygame.draw.circle(self.surface, Colors.Player, self.center, self.radius)
        pygame.draw.circle(
            self.surface, Colors.Background, self.center, self.radius - SpriteWidth
        )

    def update(self) -> None:
        self.shooting_reload = max(0, self.shooting_reload - 1)
        self.move_cannon()
        self.rotate_cannon()
        self.draw()
