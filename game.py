import tkinter as tk


BG = "#111827"
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID = "#1f2937"


class SnakeGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Snake Game - CSC-44102")
        self.root.resizable(False, False)
        self.cv = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
        self.cv.pack()
        self.draw_grid()
        self.loop()

    def loop(self):
        # nothing yet; just refresh
        self.root.after(200, self.loop)

    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            self.cv.create_line(x, 0, x, HEIGHT, fill=GRID)
        for y in range(0, HEIGHT, CELL_SIZE):
            self.cv.create_line(0, y, WIDTH, y, fill=GRID)

def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()