import json
import os


from .shooter import Shooter
from .constants import Colors
from .upgrade_constants import DEFAULT_UPGRADE_LVLS, UPGRADEABLE_STATS, UPGRADES


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

    upgrades_path = "data/upgrades.json"
    levels = {}

    class BulletStats:
        speed = 20
        radius = 10
        lifespan = 100
        precision = 93
        recoil = 5
        color = Colors.PlayerBullet
        random_movement = False
        damage = 40

    def upgrade_stat(self, stat: str) -> None:
        amount = UPGRADES[stat]["amount"]
        multiplier = UPGRADES[stat]["multiplier"]
        upper_bound = UPGRADES[stat]["upper_bound"]
        lower_bound = UPGRADES[stat]["lower_bound"]
        affected_stat = UPGRADES[stat].get("affects")

        obj = None
        if hasattr(self, stat):
            obj = self

        if hasattr(self.BulletStats, stat):
            obj = self.BulletStats

        if obj:
            setattr(
                obj, stat, clamp(getattr(obj, stat) + amount, upper_bound, lower_bound)
            )
            setattr(
                obj,
                stat,
                clamp(getattr(obj, stat) * multiplier, upper_bound, lower_bound),
            )

        if affected_stat:
            setattr(
                obj,
                affected_stat,
                clamp(getattr(obj, stat) + amount, upper_bound, lower_bound),
            )

    def load_stats(self) -> None:
        if os.path.exists(self.upgrades_path):
            with open(self.upgrades_path, "r") as f:
                self.levels = json.load(f)
        else:
            self.levels = DEFAULT_UPGRADE_LVLS

        for k, v in self.levels.items():
            for _ in range(v):
                self.upgrade_stat(k)

    def increase_stat_level(self, stat: str) -> None:
        self.levels[stat] += 1
        self.upgrade_stat(stat)
        with open(self.upgrades_path, "w") as f:
            json.dump(self.levels, f, indent=2)

    def can_update(self, stat) -> bool:
        if hasattr(self, stat):
            obj = self

        if hasattr(self.BulletStats, stat):
            obj = self.BulletStats

        value = getattr(obj, stat)

        upper_bound = UPGRADES[stat]["upper_bound"]
        lower_bound = UPGRADES[stat]["lower_bound"]

        return not (value == upper_bound or value == lower_bound)
