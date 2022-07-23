import math
from random import randint

from pygame import Vector2

from .bullet import Bullet


class ScreenShake:
    shaking = 0
    strength = 5

    def stop(self) -> None:
        self.shaking = 0

    def shake(self, bullet: Bullet) -> None:
        self.shaking += int(math.sqrt(bullet.radius * 2))
        self.strength = int(math.sqrt(bullet.radius * 2))

    def get_screen_offset(self) -> Vector2:
        self.shaking = max(0, self.shaking - 1)
        return (
            Vector2([randint(-self.strength, self.strength) for _ in range(2)])
            if self.shaking > 0
            else Vector2([0, 0])
        )
