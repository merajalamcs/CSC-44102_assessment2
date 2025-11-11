import tkinter as tk
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
        self.cv = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
        self.cv.pack()
        self.draw_grid()
                
        self.grid_w = WIDTH // CELL_SIZE
        self.grid_h = HEIGHT // CELL_SIZE
        mid = Point(self.grid_w // 2, self.grid_h // 2)
        self.snake = [Point(mid.x, mid.y), Point(mid.x - 1, mid.y), Point(mid.x - 2, mid.y)]

        self.loop()
        self.draw_snake()

    def loop(self):
        # nothing yet; just refresh
        self.root.after(200, self.loop)

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