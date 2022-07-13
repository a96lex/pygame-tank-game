from math import sqrt
from random import random
import pygame

from game.enemy import Bomber, Shotgun, ShotgunBoss, Sniper
from game.player import Player


class Level:
    def __init__(self, snipers=0, bombers=0, shotguns=0, shotgun_bosses=0) -> None:
        self.snipers = snipers
        self.bombers = bombers
        self.shotguns = shotguns
        self.shotgun_bosses = shotgun_bosses


# One enemy of each for the first few rounds
levels = [
    Level(1, 0, 0, 0),
    Level(0, 1, 0, 0),
    Level(0, 0, 1, 0),
    Level(0, 0, 0, 1),
]


def generate_level(lvl_no: int) -> Level:
    if lvl_no < len(levels):
        return levels[lvl_no]

    snipers = int(sqrt(lvl_no) * random())
    shotguns = int(sqrt(0.5 * lvl_no) * random())
    bombers = int(sqrt(0.25 * lvl_no) * random())
    shotgun_bosses = int(sqrt(0.1 * lvl_no) * random())

    return Level(snipers, shotguns, bombers, shotgun_bosses)


def load_level(lvl_no: int, player: Player) -> pygame.sprite.Group:
    enemies = pygame.sprite.Group()
    level = generate_level(lvl_no)
    for _ in range(level.shotguns):
        enemies.add(Shotgun(player))
    for _ in range(level.snipers):
        enemies.add(Sniper(player))
    for _ in range(level.bombers):
        enemies.add(Bomber(player))
    for _ in range(level.shotgun_bosses):
        enemies.add(ShotgunBoss(player))
    return enemies
