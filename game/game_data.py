import json
import os


DEFAULT_STATS = {"money": 0, "high_score": 0, "highest_level": 0}


class GameStats:
    _stats_path = "data/stats.json"
    _loaded = False
    money = 0
    high_score = 0
    highest_level = 0

    def load_stats(self) -> None:
        if os.path.exists(self._stats_path):
            with open(self._stats_path, "r") as f:
                try:
                    stats = json.load(f)
                except:
                    stats = DEFAULT_STATS
        else:
            stats = DEFAULT_STATS

        for stat, value in stats.items():
            if hasattr(self, stat):
                setattr(self, stat, value)

        self._loaded = True

    def __setattr__(self, stat, value) -> None:
        super(GameStats, self).__setattr__(stat, value)

        if self._loaded:
            stats = {k: v for k, v in self.__dict__.items() if k[0] != "_"}

            with open(self._stats_path, "w") as f:
                json.dump(stats, f, indent=2)


class Scenes:
    LEVEL = "level"
    SHOP = "shop"
    MENU = "menu"


class GameConfig:
    friendly_fire = False
    bouncy_bullets = False
    scene = Scenes.MENU
