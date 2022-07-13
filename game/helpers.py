from random import randint

import pygame

from .bullet import Bullet
from .shooter import Shooter


def check_quit_condition() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break


def cirlce_collision(c1: Shooter | Bullet, c2: Shooter | Bullet) -> bool:
    distanceV = pygame.Vector2(c1.center - c2.center)
    return distanceV.magnitude() < c1.radius + c2.radius, distanceV


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
