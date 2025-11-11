import tkinter as tk
import random
from dataclasses import dataclass

BG = "#111827"
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID = "#1f2937"


@dataclass
class Point:
    x: int
    y: int


class SnakeGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Snake Game - CSC-44102")
        self.root.resizable(False, False)

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

        # --- NEW: spawn first food ---
        self.food = self.spawn_food()

        # Key bindings (use real angle brackets)
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

    # ---- Food helpers (NEW) ----
    def spawn_food(self) -> Point:
        occupied = {(p.x, p.y) for p in self.snake}
        free = [(x, y) for x in range(self.grid_w) for y in range(self.grid_h) if (x, y) not in occupied]
        x, y = random.choice(free)
        return Point(x, y)

    def draw_food(self):
        # red-500
        self.draw_cell(self.food, "#ef4444")

    # ---- Game step ----
    def step(self):
        self.dir = self.pending_dir
        head = self.snake[0]
        new_head = Point(head.x + self.dir.x, head.y + self.dir.y)

        # temporary wrap; you can replace with wall collision later
        new_head.x %= self.grid_w
        new_head.y %= self.grid_h

        self.snake.insert(0, new_head)

        # --- NEW: eat / grow logic ---
        if new_head.x == self.food.x and new_head.y == self.food.y:
            # keep grown (no pop) and respawn food
            self.food = self.spawn_food()
        else:
            # normal move: remove tail
            self.snake.pop()

    # ---- Main loop ----
    def loop(self):
        self.cv.delete("all")
        self.draw_grid()
        self.step()
        # --- NEW: draw food each frame ---
        self.draw_food()
        self.draw_snake()
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


def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()