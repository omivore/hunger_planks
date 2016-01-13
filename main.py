#! python
# vim.py

from tkinter import *
import time
from germ import Germ

root = Tk()
root.title("The Hunger Planks")
root.resizable(0, 0)

canvas = Canvas(root, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
canvas.bind("<Button-1>", lambda event: germs.append(Germ.from_random(canvas, (500, 500))))

germs = [Germ.from_random(canvas, (500, 500)) for germ_count in range(3)]

root.update()
try:
    while True:
        for i in range(len(germs)):
            germs[i].move()
            root.update_idletasks()
        root.update()
        time.sleep(0.01)
except TclError:
    pass
