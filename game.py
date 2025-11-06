import tkinter as tk

BG = "#111827"
WIDTH, HEIGHT = 600, 400

class SnakeGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Snake Game - CSC-44102")
        self.root.resizable(False, False)

        self.cv = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
        self.cv.pack()

        self.loop()

    def loop(self):
        # nothing yet; just refresh
        self.root.after(200, self.loop)

def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
