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
