#! python
# vim.py

speed_limit = 20

from tkinter import *
import germ
import random, time, itertools

root = Tk()
root.title("The Hunger Planks")
root.resizable(0, 0)

canvas = Canvas(root, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()

germs = [germ.Germ(canvas, (100, 100), "cyan", 3)]

def spawnGerm(event):
    germ_colors = ["red", "blue", "green", "magenta", "purple", "yellow", "azure", "cyan", "snow", "lavenderblush", "salmon"]
    germ_speeds = list(itertools.chain(range(-speed_limit - 1, 0), range(1, speed_limit + 1)))

    germs.append(germ.Germ(canvas, (random.randint(0,500), random.randint(0,500)), random.choice(germ_colors), random.choice(germ_speeds)))

canvas.bind("<Button-1>",spawnGerm)

root.update()

try:
    while True:
        for i in range(len(germs)):
            germs[i] = germs[i]()
            root.update_idletasks()
        root.update()
        time.sleep(0.01)
except TclError:
    pass
