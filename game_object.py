from __future__ import annotations
from typing import TYPE_CHECKING
import pyxel # type: ignore

from vector import Vector2f


if TYPE_CHECKING:
    from bullet_manager import BulletManager


class GameObject:
    def __init__(self, x: float, y: float, camera: Vector2f, size: int = 8) -> None:
        self.position = Vector2f(x, y)
        self.velocity = Vector2f(0.0, 0.0)
        self.camera = camera
        self.size = size

    def move(self) -> None:
        self.position += self.velocity

    def update(self) -> None:
        pass

    @property
    def view_x(self) -> float:
        return self.position.x - self.camera.x + pyxel.width / 2 - self.size / 2

    @property
    def view_y(self) -> float:
        return self.position.y - self.camera.y + pyxel.height / 2 - self.size / 2

    def draw(self) -> None:
        pass

class Character(GameObject):
    def __init__(self, x: float, y: float, life: int, camera: Vector2f, bullet_manger: BulletManager):
        super().__init__(x, y, camera, CHAR_SIZE)
        self.bullet_manger = bullet_manger
        self.life = life

    @property
    def is_alive(self) -> bool:
        return self.life > 0
