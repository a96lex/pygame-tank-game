from .shooter import Shooter
from .constants import Colors


class Player(Shooter):
    radius = 40
    acceleration = 3
    max_speed = 10
    angle = 0
    cannon_rect = [
        [10, 20],
        [10, -20],
        [60, -20],
        [60, 20],
    ]
    shooting_reload = 0
    max_health = 1000
    health = max_health

    class BulletStats:
        speed = 20
        radius = 10
        lifespan = 100
        precision = 10
        recoil = 5
        cooldown = 20
        color = Colors.PlayerBullet
        random_movement = False
        damage = 40

    def update(self) -> None:
        self.shooting_reload = max(0, self.shooting_reload - 1)
        self.move()
        self.rotate()
        self.draw()
