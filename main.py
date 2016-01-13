#! python
# vim.py

from tkinter import *
import time
from germ import Germ

root = Tk()
root.title("The Hunger Planks")

canvas = Canvas(root, width=500, height=500)
canvas.bind("<Button-1>", lambda event: germs.append(Germ.from_random(canvas)))
canvas.pack(fill=BOTH, expand=YES)

germs = [Germ.from_random(canvas) for germ_count in range(3)]

root.update()
try:
    while True:
        for i in range(len(germs)):
            germs[i].move()
            root.update_idletasks()
        root.update()
        time.sleep(0.01)    # This is to make sure the germs don't move too fast to see.

# When the window closes, the loop will run one last time and throw a TclError. Do nothing.
except TclError:
    pass
