import pyxel # type: ignore
import time

from vector import Vector2f
from player import Player
from wave import Wave
from field_render import FieldRender
from bullet_manager import BulletManager


class Game:
    def __init__(self) -> None:
        pyxel.init(128, 128, fps=60)
        pyxel.image(0).load(0, 0, "./sprite.png")
        pyxel.image(1).load(0, 0, "./tile.png")
        px, py = FieldRender.FIELD_WIDTH / 2, FieldRender.FIELD_HEIGHT / 2
        self.state = "idle"
        self.timer = time.time()
        self.camera = Vector2f(px, py)
        self.bullet_manager = BulletManager()
        self.field_render = FieldRender(self.camera)
        self.player = Player(px, py, self.camera, self.bullet_manager)
        self.wave = Wave(self.camera, self.player, self.bullet_manager)

    def reset_timer(self) -> None:
        self.timer = time.time()

    @property
    def current_time(self) -> float:
        return time.time() - self.timer

    def run(self) -> None:
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        if self.state == "idle":
            if self.current_time >= 3:
                self.reset_timer()
                self.wave.start_wave()
                self.state = "wave"
        elif self.state == "wave":
            # update enemies
            self.wave.update()
            # check
            if self.player.life <= 0:
                self.state = "game_over"
            if self.current_time >= 30 and not self.wave.enemy_eliminated:
                self.state = "game_over"
            elif self.wave.enemy_eliminated and self.current_time < 30:
                self.reset_timer()
                self.bullet_manager.clear_bullets()
                self.player.shot_level = 1 + self.wave.level // 2
                self.player.speed += 0.2
                self.player.life = self.player.LIFE_MAX
                self.state = "result"
        elif self.state == "result":
            if self.current_time >= 2:
                self.reset_timer()
                self.wave.level += 1
                self.state = "idle"

        if self.state != "game_over":
            # update player and bullets
            self.player.update()
            self.bullet_manager.update(self.player, self.wave.enemies)
            # update camera position
            self.camera.x = self.player.position.x
            self.camera.y = self.player.position.y
        else:
            if pyxel.btn(pyxel.KEY_R):
                self.reset_timer()
                self.player.life = self.player.LIFE_MAX
                self.wave.level = 1
                self.state = "idle"

    def draw_time(self) -> None:
        t = int(30 - self.current_time)
        col = 8 if t <= 10 else 7
        pyxel.text(pyxel.width // 2 - 4 + 1, 2, f"{t:02}", 1)
        pyxel.text(pyxel.width // 2 - 4, 1, f"{t:02}", col)

    def draw_status(self) -> None:
        # life text
        pyxel.text(2, 2, "HP: ", 1)
        pyxel.text(1, 1, "HP: ", 7)
        # life bar
        pyxel.rect(15, 3, 20, 4, 1)
        pyxel.rect(14, 2, 20, 4, 11)
        pyxel.rect(14, 2, (1 - self.player.life / self.player.LIFE_MAX) * 20, 4, 8)
        # enemy num
        pyxel.text(2, 8, f"Enemy: {len(self.wave.enemies)}", 1)
        pyxel.text(1, 7, f"Enemy: {len(self.wave.enemies)}", 7)

    def draw(self) -> None:
        pyxel.cls(15)

        self.field_render.draw()
        self.player.draw()
        self.bullet_manager.draw()

        if self.state == "idle":
            if self.current_time < 2.0:
                pyxel.text(pyxel.width // 2 - 12, 32, f"Wave {self.wave.level}", 7)
            else:
                pyxel.text(pyxel.width // 2 - 12, 32, f"Start!", 8)
        elif self.state == "wave":
            self.wave.draw()
            self.draw_time()
            self.draw_status()
        elif self.state == "result":
            pyxel.text(pyxel.width // 2 - 12, 32, f"Wave {self.wave.level}", 7)
            pyxel.text(pyxel.width // 2 - 12, 40, f"Clear!", 7)
        elif self.state == "game_over":
            pyxel.text(pyxel.width // 2 - 16, 32, f"Game Over", 8)
            pyxel.text(pyxel.width // 2 - 24, 40, f"Score: Wave {self.wave.level}", 7)
            pyxel.text(pyxel.width // 2 - 24, 48, "PUSH R RESTART", 7)

        pyxel.circ(pyxel.mouse_x, pyxel.mouse_y, 1, 8)
        pyxel.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
