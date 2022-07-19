import math
from random import randint
from typing import List

from .bullet import Bullet


class ScreenShake:
    shaking = 0
    strength = 5

    def stop(self) -> None:
        self.shaking = 0

    def shake(self, bullet: Bullet) -> None:
        self.shaking += int(math.sqrt(bullet.radius * 2))
        self.strength = int(math.sqrt(bullet.radius * 2))

    def get_screen_offset(self) -> List[int]:
        self.shaking = max(0, self.shaking - 1)
        return (
            [randint(-self.strength, self.strength) for _ in range(2)]
            if self.shaking > 0
            else [0, 0]
        )
