from typing import List

import pygame

from .constants import Colors, SpriteWidth


class Shooter(pygame.sprite.Sprite):
    surface: pygame.Surface = None

    cannon_coords: List[pygame.Vector2]
    center: pygame.Vector2(0, 0)
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
    cooldown = 20

    max_health = 100
    health = max_health

    def __init__(self, surface: pygame.Surface) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.center = pygame.Vector2(surface.get_width() / 2, surface.get_height() / 2)

    def update_speed(
        self, direction: pygame.Vector2 = None, magnitude: float = None
    ) -> None:
        if not magnitude:
            magnitude = self.acceleration

        if not direction and hasattr(self, "target"):
            direction = pygame.Vector2(self.target.center - self.center).normalize()

        self.speed = pygame.Vector2(
            [
                max(-self.max_speed, min(self.max_speed, a + b))
                for a, b in zip(self.speed, direction * magnitude)
            ]
        )

    def move(self) -> None:
        self.center += self.speed
        self.speed *= 0.9

    def rotate(self) -> None:
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

        if self.health < self.max_health:
            # Health bar outline
            pygame.draw.polygon(
                self.surface,
                Colors.Player,
                [
                    [self.center.x - 54, self.center.y + 4 + self.radius + 30],
                    [self.center.x - 54, self.center.y - 4 + self.radius + 30],
                    [self.center.x + 54, self.center.y - 4 + self.radius + 30],
                    [self.center.x + 54, self.center.y + 4 + self.radius + 30],
                ],
                2,
            )

            # Actual health bar
            pygame.draw.polygon(
                self.surface,
                Colors.HealthBar,
                [
                    [self.center.x - 50, self.center.y + 1 + self.radius + 30],
                    [self.center.x - 50, self.center.y - 1 + self.radius + 30],
                    [
                        self.center.x - 50 + 100 * (self.health / self.max_health),
                        self.center.y - 1 + self.radius + 30,
                    ],
                    [
                        self.center.x - 50 + 100 * (self.health / self.max_health),
                        self.center.y + 1 + self.radius + 30,
                    ],
                ],
            )

    def shoot(self) -> None:
        self.shooting_reload = self.cooldown

    def take_damage(self, dmg: float, direction: pygame.Vector2) -> None:
        self.health -= dmg
        self.update_speed(direction, dmg / 1000)
        if self.health <= 0:
            self.kill()
            return self.radius
        return int(self.radius / 10)

    def update(self) -> None:
        self.shooting_reload = max(0, self.shooting_reload - 1)
        self.move()
        self.rotate()
        self.draw()
