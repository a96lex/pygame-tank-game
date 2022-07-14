from random import randint
from time import time

import pygame

from .bullet import Bullet
from .shooter import Shooter


def check_quit_condition() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def cirlce_collision(c1: Shooter | Bullet, c2: Shooter | Bullet) -> bool:
    distanceV = pygame.Vector2(c1.center - c2.center)
    return distanceV.magnitude() < c1.radius + c2.radius, distanceV


def handle_collision_if_exist(bullet: Bullet, entity: Shooter) -> int:
    collided, direction = cirlce_collision(entity, bullet)
    if collided:
        bullet.kill()
        return entity.take_damage(bullet.damage, direction)
    else:
        return 0


def get_random_position_at_edge(surface: pygame.Surface, padding=100) -> pygame.Vector2:
    width = surface.get_width() - padding
    height = surface.get_height() - padding
    p = randint(0, width + width + height + height)
    center = pygame.Vector2()
    if p < (width + height):
        if p < width:
            center.x = p + padding / 2
            center.y = 0 + padding / 2
        else:
            center.x = width + padding / 2
            center.y = p - width + padding / 2
    else:
        p = p - (width + height)
        if p < width:
            center.x = width - p + padding / 2
            center.y = height + padding / 2
        else:
            center.x = 0 + padding / 2
            center.y = height - (p - width) + padding / 2

    return center


class DelayedBoolean:
    value = False
    refresh = 0.5  # seconds
    last_time = 0

    def __init__(
        self, value: bool = False, refresh: float = 0.5, last_time: float = 0
    ) -> None:
        self.value = value
        self.refresh = refresh
        self.last_time = last_time

    def switch(self) -> None:
        if time() >= self.last_time + self.refresh:
            self.last_time = time()
            self.value = not self.value

    def __bool__(self) -> bool:
        return self.value
