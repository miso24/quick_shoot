from __future__ import annotations
from typing import Generic, TypeVar
import math


T = TypeVar('T', int, float)


class Vector2(Generic[T]):
    def __init__(self, x: T, y: T) -> None:
        self.x: T = x
        self.y: T = y

    def euclid_dist(self) -> T:
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))

    def __add__(self, other: Vector2[T]) -> Vector2[T]:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2[T]) -> Vector2[T]:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: T) -> Vector2[T]:
        return Vector2(self.x * other, self.y * other)

Vector2i = Vector2[int]
Vector2f = Vector2[float]
