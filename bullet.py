from __future__ import annotations
from typing import List, TYPE_CHECKING
import pyxel # type: ignore

from game_object import GameObject, Character
from enemy import Enemy


if TYPE_CHECKING:
    from vector import Vector2f 


class Bullet(GameObject):
    def __init__(self, parent: Character, velocity: Vector2f) -> None:
        super().__init__(parent.position.x, parent.position.y, parent.camera)
        self.parent = parent
        self.velocity = velocity
        self.is_enable = True

    @property
    def is_frame_out(self) -> bool:
        if -self.size < self.view_x < pyxel.width and -self.size < self.view_y < pyxel.height:
            return False
        return True

    def collision_check(self, targets: List[Character]) -> None:
        for target in targets:
            diff = self.position - target.position
            dist = diff.euclid_dist()
            if dist >= self.size / 2:
                continue
            if isinstance(target, Enemy) and isinstance(self.parent, Enemy) or id(self.parent) == id(target):
                continue
            target.life -= 1
            self.is_enable = False

    def update(self) -> None:
        if self.is_frame_out:
            self.is_enable = False
        else:
            self.move()

    def draw(self) -> None:
        if isinstance(self.parent, Enemy):
            pyxel.blt(self.view_x, self.view_y, 0, 8, 16, 8, 8, 0)
        else:
            pyxel.blt(self.view_x, self.view_y, 0, 0, 16, 8, 8, 0)
