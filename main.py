#! python
# vim.py

from tkinter import *
import time, random
from germ import Germ
from plank import Plank

root = Tk()
root.title("The Hunger Planks")

canvas = Canvas(root, width=500, height=500)
canvas.bind("<Button-1>", lambda event: germs.append(Germ.from_random(canvas)))
canvas.pack(fill=BOTH, expand=YES)

root.update()

germs = [Germ.from_random(canvas) for germ_count in range(3)]
planks = [Plank(canvas, (5, 10), 0, canvas.winfo_width() - 10, "blue", 0),
          Plank(canvas, (5, canvas.winfo_height() - 10), 0, canvas.winfo_width() - 10, "green", 0),
          Plank(canvas, (5, 10), 90, canvas.winfo_height() - 10, "red", 0),
          Plank(canvas, (canvas.winfo_width() - 10, 10), 90, canvas.winfo_width() - 10, "yellow", 0)]
try:
    while True:
        for i in range(len(germs)):
            germs[i].move(random.choice([-1, 1]), random.choice([-1, 1]))
            if germs[i].dead: germs.remove(germs[i])
            root.update_idletasks()

        for i in range(len(planks)):
            planks[i].move()
            if planks[i].dead: planks.remove(planks[i])
            root.update_idletasks()

        root.update()
        time.sleep(.2)    # This is to make sure the germs don't move too fast to see.

# When the window closes, the loop will run one last time and throw a TclError. Do nothing.
except TclError:
    pass
