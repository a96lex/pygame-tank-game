import json
import os

from .shooter import Shooter
from .constants import Colors

UPGRADES = {
    "max_speed": {"multiplier": 1.1, "amount": 0, "upper_bound": 18, "lower_bound": 0},
    "max_health": {
        "multiplier": 1.1,
        "amount": 0,
        "upper_bound": 3000,
        "lower_bound": 0,
    },
    "speed": {"multiplier": 1, "amount": 1, "upper_bound": 35, "lower_bound": 0},
    "precision": {"multiplier": 1, "amount": 0.5, "upper_bound": 100, "lower_bound": 0},
    "cooldown": {"multiplier": 1, "amount": -1, "upper_bound": 100, "lower_bound": 4},
    "damage": {"multiplier": 1, "amount": 10, "upper_bound": 120, "lower_bound": 0},
}

DEFAULT_UPGRADE_LVLS = {
    "max_speed": 0,
    "max_health": 0,
    "speed": 0,
    "precision": 0,
    "cooldown": 0,
    "damage": 0,
}


def clamp(value: float, upper_bound: float, lower_bound: float) -> float:
    return max(lower_bound, min(upper_bound, value))


class Player(Shooter):
    radius = 30
    acceleration = 3
    max_speed = 10
    angle = 0
    cannon_rect = [
        [10, 18],
        [10, -18],
        [49, -18],
        [49, 18],
    ]
    shooting_reload = 0
    max_health = 1000
    health = max_health
    cooldown = 20

    class BulletStats:
        speed = 20
        radius = 10
        lifespan = 100
        precision = 93
        recoil = 5
        color = Colors.PlayerBullet
        random_movement = False
        damage = 40

    def upgrade_stat(self, stat=str) -> None:
        amount = UPGRADES[stat]["amount"]
        multiplier = UPGRADES[stat]["multiplier"]
        upper_bound = UPGRADES[stat]["upper_bound"]
        lower_bound = UPGRADES[stat]["lower_bound"]

        el = None
        if hasattr(self, stat):
            el = self

        if hasattr(self.BulletStats, stat):
            el = self.BulletStats

        if el:
            setattr(
                el, stat, clamp(getattr(el, stat) + amount, upper_bound, lower_bound)
            )
            setattr(
                el,
                stat,
                clamp(getattr(el, stat) * multiplier, upper_bound, lower_bound),
            )

    def load_stats(self) -> None:
        path = "data/upgrades.dat"

        if os.path.exists(path):
            with open(path, "r") as f:
                upgrade_data = json.load(f)
        else:
            upgrade_data = DEFAULT_UPGRADE_LVLS

        for k, v in upgrade_data.items():
            for _ in range(v):
                self.upgrade_stat(k)
