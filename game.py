import tkinter as tk
import random
from dataclasses import dataclass

BG = "#111827"
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID = "#1f2937"
TEXT = "#e5e7eb"  # for status bar text

# --- NEW: speed + color constants ---
SPEED_MS = 120
SPEED_UP_EVERY = 5
SPEED_DELTA = -5
SNAKE = "#10b981"
FOOD = "#ef4444"


@dataclass
class Point:
    x: int
    y: int


class SnakeGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Snake Game - CSC-44102 - Assesment 2")
        self.root.resizable(False, False)

        # ---- Status bar (before canvas) ----
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

        # Grid dims
        self.grid_w = WIDTH // CELL_SIZE
        self.grid_h = HEIGHT // CELL_SIZE

        # Direction state (initial placeholders; real init in reset())
        self.dir = Point(1, 0)
        self.pending_dir = self.dir

        # Alive/pause flags
        self.alive = True
        self.paused = False

        # Key bindings
        self.root.bind("<Up>",    lambda e: self.set_dir(0, -1))
        self.root.bind("<Down>",  lambda e: self.set_dir(0,  1))
        self.root.bind("<Left>",  lambda e: self.set_dir(-1, 0))
        self.root.bind("<Right>", lambda e: self.set_dir(1,  0))
        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<r>",     lambda e: self.restart())
        self.root.bind("<R>",     lambda e: self.restart())

        # Initialize all runtime state (snake, food, score, tick, etc.)
        self.reset()

        # Start loop
        self.loop()

    # ---- Input ----
    def set_dir(self, dx, dy):
        # block 180° turns
        if (dx, dy) == (-self.dir.x, -self.dir.y):
            return
        self.pending_dir = Point(dx, dy)

    # ---- Lifecycle helpers ----
    def reset(self):
        mid = Point(self.grid_w // 2, self.grid_h // 2)
        self.snake = [Point(mid.x, mid.y), Point(mid.x - 1, mid.y), Point(mid.x - 2, mid.y)]
        self.dir = Point(1, 0)
        self.pending_dir = self.dir
        self.food = self.spawn_food()
        self.score = 0
        self.alive = True
        self.paused = False

        # speed management state 
        self.tick = SPEED_MS
        self.foods_eaten = 0

        self.msg_var.set("Arrow keys to move • Space: Pause • R: Restart")

    def restart(self):
        if not self.alive:
            self.msg_var.set("Restarted. Arrow keys to move • Space: Pause")
        self.reset()

    def toggle_pause(self):
        if not self.alive:
            return
        self.paused = not self.paused
        self.msg_var.set(
            "Paused. Press Space to resume"
            if self.paused
            else "Arrow keys to move • Space: Pause • R: Restart"
        )

    # ---- Food helpers ----
    def spawn_food(self) -> Point:
        occupied = {(p.x, p.y) for p in self.snake}
        free = [(x, y) for x in range(self.grid_w) for y in range(self.grid_h) if (x, y) not in occupied]
        x, y = random.choice(free)
        return Point(x, y)

    def draw_food(self):
        # use constant color
        self.draw_cell(self.food, FOOD)

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

    # ---- Game step (with speed-up) ----
    def step(self):
        # Early exit if dead or paused
        if not self.alive or self.paused:
            return

        self.dir = self.pending_dir
        head = self.snake[0]
        new_head = Point(head.x + self.dir.x, head.y + self.dir.y)

        # Wall collision instead of wrapping
        if not (0 <= new_head.x < self.grid_w and 0 <= new_head.y < self.grid_h):
            self.game_over("Hit the wall!")
            return

        # Self-collision
        if any(seg.x == new_head.x and seg.y == new_head.y for seg in self.snake):
            self.game_over("Ran into yourself!")
            return

        # proceed with movement
        self.snake.insert(0, new_head)

        # Eat / grow + scoring + speed adjustments
        if new_head.x == self.food.x and new_head.y == self.food.y:
            self.score += 10
            self.foods_eaten += 1
            # --- NEW: speed up every N foods, keep a safe lower bound ~40ms
            if self.foods_eaten % SPEED_UP_EVERY == 0 and self.tick + SPEED_DELTA >= 40:
                self.tick += SPEED_DELTA
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    # ---- Main loop (dynamic tick) ----
    def loop(self):
        self.cv.delete("all")
        self.draw_grid()
        self.step()
        self.draw_food()
        self.draw_snake()
        self.update_labels()
        # use dynamic tick
        self.root.after(self.tick, self.loop)

    # ---- Drawing helpers ----
    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            self.cv.create_line(x, 0, x, HEIGHT, fill=GRID)
        for y in range(0, HEIGHT, CELL_SIZE):
            self.cv.create_line(0, y, WIDTH, y, fill=GRID)

    # --- NEW: rounded look via inner rectangle outline ---
    def draw_cell(self, p: Point, color: str, radius: int = 2):
        x0 = p.x * CELL_SIZE
        y0 = p.y * CELL_SIZE
        x1 = x0 + CELL_SIZE
        y1 = y0 + CELL_SIZE
        self.cv.create_rectangle(x0, y0, x1, y1, fill=color, outline=BG)
        pad = max(0, radius)
        self.cv.create_rectangle(x0 + pad, y0 + pad, x1 - pad, y1 - pad, outline=color)

    def draw_snake(self):
        for i, seg in enumerate(self.snake):
            self.draw_cell(seg, SNAKE, radius=4 if i == 0 else 2)

  
    def update_labels(self):
        self.score_var.set(f"Score: {self.score}")


def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()