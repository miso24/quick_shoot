from __future__ import annotations
from typing import List, TYPE_CHECKING
import pyxel # type: ignore
import random
import math

from enemy import Enemy


if TYPE_CHECKING:
    from player import Player
    from vector import Vector2f
    from bullet_manager import BulletManager


class Wave:
    def __init__(self, camera: Vector2f, player: Player, bullet_manager: BulletManager) -> None:
        self.level = 1
        self.camera = camera
        self.player = player
        self.bullet_manager = bullet_manager
        self.enemies: List[Enemy] = []

    def start_wave(self) -> None:
        self.enemies: List[Enemy] = []
        for _ in range(5 + (self.level - 1) * 2):
            dist = random.randint(pyxel.width / 2, pyxel.width / 2 + self.level * 10)
            angle = random.randint(0, 360) / (180 / math.pi)
            self.enemies.append(Enemy(
                self.player.position.x + math.cos(angle) * dist,
                self.player.position.y + math.sin(angle) * dist,
                1 + self.level * 5,
                self.camera,
                self.bullet_manager,
                self.level,
                self.player
            ))

    @property
    def enemy_eliminated(self) -> bool:
        return not self.enemies

    def update(self) -> None:
        for enemy in self.enemies:
            enemy.update()
        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive]

    def draw(self) -> None:
        for enemy in self.enemies:
            enemy.draw()
