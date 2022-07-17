class UPGRADEABLE_STATS:
    MAX_SPEED = "max_speed"
    MAX_HEALTH = "max_health"
    SPEED = "speed"
    PRECISION = "precision"
    COOLDOWN = "cooldown"
    DAMAGE = "damage"


UPGRADES = {
    UPGRADEABLE_STATS.MAX_SPEED: {
        "multiplier": 1.1,
        "amount": 0,
        "upper_bound": 18,
        "lower_bound": 0,
    },
    UPGRADEABLE_STATS.MAX_HEALTH: {
        "multiplier": 1.1,
        "affects": "health",
        "amount": 0,
        "upper_bound": 3000,
        "lower_bound": 0,
    },
    UPGRADEABLE_STATS.SPEED: {
        "multiplier": 1,
        "amount": 1,
        "upper_bound": 35,
        "lower_bound": 0,
    },
    UPGRADEABLE_STATS.PRECISION: {
        "multiplier": 1,
        "amount": 0.5,
        "upper_bound": 100,
        "lower_bound": 0,
    },
    UPGRADEABLE_STATS.COOLDOWN: {
        "multiplier": 1,
        "amount": -1,
        "upper_bound": 100,
        "lower_bound": 4,
    },
    UPGRADEABLE_STATS.DAMAGE: {
        "multiplier": 1,
        "amount": 10,
        "upper_bound": 120,
        "lower_bound": 0,
    },
}

DEFAULT_UPGRADE_LVLS = {
    "max_speed": 0,
    "max_health": 0,
    "speed": 0,
    "precision": 0,
    "cooldown": 0,
    "damage": 0,
}
