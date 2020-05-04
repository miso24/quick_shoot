from __future__ import annotations
from typing import ClassVar, TYPE_CHECKING
import pyxel # type: ignore
import math

from constants import 8
from vector import Vector2f


if TYPE_CHECKING:
    from bullet_manager import BulletManager


class Player(Character):
    SHOT_INTERVAL: ClassVar[int] = 3
    SHOT_SPEED: ClassVar[float] = 5.0
    LIFE_MAX: ClassVar[int] = 20

    def __init__(self, x: float, y: float, camera: Vector2f, bullet_manager: BulletManager) -> None:
        super().__init__(x, y, Player.LIFE_MAX, camera, bullet_manager)
        self.angle = 0.0
        self.shot_count = 0
        self.speed = 1.0
        self.shot_level = 1

    def update_angle(self) -> None:
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        rad_angle = math.atan2(
            my - pyxel.height / 2,
            pyxel.width / 2 - mx
        )
        self.angle = rad_angle * (180 / math.pi) + 180

    def update_velocity(self) -> None:
        velocity = Vector2f(0.0, 0.0)
        if pyxel.btn(pyxel.KEY_A):
            velocity.x -= self.speed
        if pyxel.btn(pyxel.KEY_D):
            velocity.x += self.speed
        if pyxel.btn(pyxel.KEY_W):
            velocity.y -= self.speed
        if pyxel.btn(pyxel.KEY_S):
            velocity.y += self.speed

        if velocity.x and velocity.y:
            velocity *= 1 / math.sqrt(2)
        self.velocity = velocity

    def fire(self) -> None:
        if not pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
            self.shot_count = 0
            return

        if self.shot_count % Player.SHOT_INTERVAL == 0:
            for i in range(self.shot_level):
                diff = i * 10 if i % 2 == 0 else i * -10
                angle = self.angle + diff
                self.bullet_manger.add_bullet(
                    self,
                    Vector2f(
                        math.cos(angle / (180 / math.pi)) * Player.SHOT_SPEED,
                        -math.sin(angle / (180 / math.pi)) * Player.SHOT_SPEED
                    )
                )
            self.shot_count = 0
        self.shot_count += 1

    def update(self):
        self.update_angle()
        self.update_velocity()
        self.fire()
        self.move()

    def draw(self) -> None:
        u = ((22.5 + self.angle) // 45) % 8
        pyxel.blt(self.view_x + 2, self.view_y + 2, 0, u * 8, 24, 8, 8, 0)
        pyxel.blt(self.view_x, self.view_y, 0, u * 8, 0, 8, 8, 0)
