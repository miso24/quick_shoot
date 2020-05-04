from __future__ import annotations
from typing import List, TYPE_CHECKING

from bullet import Bullet


if TYPE_CHECKING:
    from game_object import GameObject
    from vector import Vector2f
    from player import Player
    from enemy import Enemy


class BulletManager:
    def __init__(self) -> None:
        self.bullets: List[Bullet] = []

    def add_bullet(self, parent: GameObject, velocity: Vector2f) -> None:
        self.bullets.append(Bullet(
            parent,
            velocity
        ))

    def update(self, player: Player, enemy_list: List[Enemy]) -> None:
        for bullet in self.bullets:
            bullet.update()
            bullet.collision_check([player, *enemy_list])
        self.bullets = [bullet for bullet in self.bullets if bullet.is_enable]

    def clear_bullets(self) -> None:
        self.bullets = []

    def draw(self) -> None:
        for bullet in self.bullets:
            bullet.draw()
