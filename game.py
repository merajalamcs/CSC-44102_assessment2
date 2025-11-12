
import tkinter as tk
import random
from dataclasses import dataclass

BG = "#111827"
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID = "#1f2937"
TEXT = "#e5e7eb"  # for status bar text


@dataclass
class Point:
    x: int
    y: int


class SnakeGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Snake Game - CSC-44102")
        self.root.resizable(False, False)

        # ---- Status bar ----
        self.top = tk.Frame(root, bg=BG)
        self.top.pack(fill=tk.X)
        self.score = 0
        self.score_var = tk.StringVar(value="Score: 0")
        self.msg_var = tk.StringVar(value="Arrow keys to move")
        tk.Label(self.top, textvariable=self.score_var, fg=TEXT, bg=BG, font=("Segoe UI", 12)).pack(
            side=tk.LEFT, padx=8, pady=6
        )
        tk.Label(self.top, textvariable=self.msg_var, fg=TEXT, bg=BG, font=("Segoe UI", 10)).pack(
            side=tk.RIGHT, padx=8
        )

        # Canvas
        self.cv = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
        self.cv.pack()
        self.draw_grid()

        # Grid dims + initial snake
        self.grid_w = WIDTH // CELL_SIZE
        self.grid_h = HEIGHT // CELL_SIZE
        mid = Point(self.grid_w // 2, self.grid_h // 2)
        self.snake = [Point(mid.x, mid.y), Point(mid.x - 1, mid.y), Point(mid.x - 2, mid.y)]

        # Direction state
        self.dir = Point(1, 0)            # moving right
        self.pending_dir = self.dir

        # Spawn first food
        self.food = self.spawn_food()

        # Alive flag for game-over flow
        self.alive = True

        # Key bindings
        self.root.bind("<Up>",    lambda e: self.set_dir(0, -1))
        self.root.bind("<Down>",  lambda e: self.set_dir(0,  1))
        self.root.bind("<Left>",  lambda e: self.set_dir(-1, 0))
        self.root.bind("<Right>", lambda e: self.set_dir(1,  0))

        # Start loop
        self.loop()

    # ---- Input ----
    def set_dir(self, dx, dy):
        # block 180° turns
        if (dx, dy) == (-self.dir.x, -self.dir.y):
            return
        self.pending_dir = Point(dx, dy)

    # ---- Food helpers ----
    def spawn_food(self) -> Point:
        occupied = {(p.x, p.y) for p in self.snake}
        free = [(x, y) for x in range(self.grid_w) for y in range(self.grid_h) if (x, y) not in occupied]
        x, y = random.choice(free)
        return Point(x, y)

    def draw_food(self):
        # red-500
        self.draw_cell(self.food, "#ef4444")

    # ---- Game over ----
    def game_over(self, reason: str):
        self.alive = False
        self.msg_var.set(f"Game over: {reason} • Press R to restart")
        # Overlay
        self.cv.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#000000", stipple="gray50", outline="")
        self.cv.create_text(WIDTH // 2, HEIGHT // 2 - 10, text="GAME OVER",
                            fill=TEXT, font=("Segoe UI", 24, "bold"))
        self.cv.create_text(WIDTH // 2, HEIGHT // 2 + 20,
                            text=f"Score: {self.score}  •  Press R to restart",
                            fill=TEXT, font=("Segoe UI", 14))

    # ---- Game step (UPDATED with self-collision) ----
    def step(self):
        if not self.alive:
            return

        self.dir = self.pending_dir
        head = self.snake[0]
        new_head = Point(head.x + self.dir.x, head.y + self.dir.y)

        # Wall collision instead of wrapping
        if not (0 <= new_head.x < self.grid_w and 0 <= new_head.y < self.grid_h):
            self.game_over("Hit the wall!")
            return

        # ---- NEW: self-collision check ----
        if any(seg.x == new_head.x and seg.y == new_head.y for seg in self.snake):
            self.game_over("Ran into yourself!")
            return

        # proceed with movement
        self.snake.insert(0, new_head)

        # Eat / grow + scoring
        if new_head.x == self.food.x and new_head.y == self.food.y:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    # ---- Main loop ----
    def loop(self):
        self.cv.delete("all")
        self.draw_grid()
        self.step()
        self.draw_food()
        self.draw_snake()
        self.update_labels()
        self.root.after(150, self.loop)

    # ---- Drawing helpers ----
    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            self.cv.create_line(x, 0, x, HEIGHT, fill=GRID)
        for y in range(0, HEIGHT, CELL_SIZE):
            self.cv.create_line(0, y, WIDTH, y, fill=GRID)

    def draw_cell(self, p: Point, color: str):
        x0, y0 = p.x * CELL_SIZE, p.y * CELL_SIZE
        x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
        self.cv.create_rectangle(x0, y0, x1, y1, fill=color, outline=BG)

    def draw_snake(self):
        for seg in self.snake:
            self.draw_cell(seg, "#10b981")  # emerald-500

   
    def update_labels(self):
        self.score_var.set(f"Score: {self.score}")


def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
