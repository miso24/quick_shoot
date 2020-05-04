import random
import pyxel


class FieldRender:
    FIELD_WIDTH = 480
    FIELD_HEIGHT = 480
    
    def __init__(self, camera):
        self.field_data = []
        self.camera = camera
        for _ in range(FieldRender.FIELD_HEIGHT // 16):
            line = []
            for __ in range(FieldRender.FIELD_WIDTH // 16):
                r = random.randint(0, 100)
                r = max(r - 50, 0)
                line.append(r // 10)
            self.field_data.append(line)

    def draw(self) -> None:
        for y in range(-1, pyxel.height // 16 + 2):
            for x in range(-1, pyxel.width // 16 + 2):
                tx = int(x * 16 + self.camera.x - pyxel.width // 2) // 16
                ty = int(y * 16 + self.camera.y - pyxel.height // 2) // 16
                if tx < 0 or tx >= FieldRender.FIELD_WIDTH // 16 or ty < 0 or ty >= FieldRender.FIELD_HEIGHT // 16:
                    continue
                u = self.field_data[ty][tx] % 4
                v = self.field_data[ty][tx] // 4
                dx = (self.camera.x // 16 - self.camera.x / 16) * 16 + x * 16
                dy = (self.camera.y // 16 - self.camera.y / 16) * 16 + y * 16
                pyxel.blt(dx, dy, 1, u * 16, v * 16, 16, 16)
