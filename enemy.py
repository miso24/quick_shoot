from __future__ import annotations
from typing import TYPE_CHECKING
import pyxel # type: ignore
import random
import math

from game_object import Character
from vector import Vector2f


if TYPE_CHECKING:
    from bullet_manager import BulletManager
    from player import Player


class Enemy(Character):
    def __init__(self, x: float, y: float, life: int, camera: Vector2f, bullet_manager: BulletManager, level: int, player: Player) -> None:
        super().__init__(x, y, life, camera, bullet_manager)
        self.level = level
        self.player = player
        self.angle = 0
        self.speed = 0.5 + (level - 1) * random.random() * 0.20
        self.shot_interval = max(30 - self.level * 2, 10) + random.randint(-5, 5)
        self.shot_count = 0

    def update_velocity(self) -> None:
        self.angle = math.atan2(
            self.position.y - self.player.position.y,
            self.player.position.x - self.position.x
        ) 
        self.velocity = Vector2f(math.cos(self.angle), -math.sin(self.angle)) * self.speed

    def fire(self) -> None:
        self.shot_count += 1
        if self.shot_count % self.shot_interval != 0:
            return
        self.bullet_manger.add_bullet(
            self,
            Vector2f(
                math.cos(self.angle) * (self.level) * 0.75,
                -math.sin(self.angle) * (self.level) * 0.75
            ) 
        )
        self.shot_count = 0

    def update(self) -> None:
        self.update_velocity()
        self.fire()
        self.move()

    def draw(self) -> None:
        u = ((22.5 + self.angle * (180 / math.pi)) // 45) % 8
        pyxel.blt(self.view_x + 2, self.view_y + 2, 0, u * 8, 24, 8, 8, 0)
        pyxel.blt(self.view_x, self.view_y, 0, u * 8, 8, 8, 8, 0)
