class UpgradeableStats:
    MAX_SPEED = "max_speed"
    MAX_HEALTH = "max_health"
    SPEED = "speed"
    PRECISION = "precision"
    COOLDOWN = "cooldown"
    DAMAGE = "damage"
    REGEN = "regen"


UPGRADES = {
    UpgradeableStats.MAX_SPEED: {
        "multiplier": 1.1,
        "amount": 0,
        "upper_bound": 18,
        "lower_bound": 0,
    },
    UpgradeableStats.MAX_HEALTH: {
        "multiplier": 1.1,
        "affects": "health",
        "amount": 0,
        "upper_bound": 3000,
        "lower_bound": 0,
    },
    UpgradeableStats.SPEED: {
        "multiplier": 1,
        "amount": 1,
        "upper_bound": 35,
        "lower_bound": 0,
    },
    UpgradeableStats.PRECISION: {
        "multiplier": 1,
        "amount": 0.5,
        "upper_bound": 100,
        "lower_bound": 0,
    },
    UpgradeableStats.COOLDOWN: {
        "multiplier": 1,
        "amount": -1,
        "upper_bound": 100,
        "lower_bound": 4,
    },
    UpgradeableStats.DAMAGE: {
        "multiplier": 1,
        "amount": 10,
        "upper_bound": 120,
        "lower_bound": 0,
    },
    UpgradeableStats.REGEN: {
        "multiplier": 1.1,
        "amount": 0.1,
        "upper_bound": 2,
        "lower_bound": -1,
    },
}

DEFAULT_UPGRADE_LVLS = {
    "max_speed": 0,
    "max_health": 0,
    "speed": 0,
    "precision": 0,
    "cooldown": 0,
    "damage": 0,
    "regen": 0,
}
