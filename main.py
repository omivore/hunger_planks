#! python
# vim.py

from tkinter import *
import time, random
from germ import Germ
from plank import Plank, Border

root = Tk()
root.title("The Hunger Planks")

canvas = Canvas(root, width=500, height=500)
canvas.bind("<Button-1>", lambda event: germs.append(Germ.from_random(get_state, canvas)))
canvas.pack(fill=BOTH, expand=YES)

root.update()

def get_state():
    return germs + planks

germs = [Germ.from_random(get_state, canvas) for germ_count in range(3)]
planks = [Border(canvas, (5, 10), 0, canvas.winfo_width() - 10, "blue"),
          Border(canvas, (5, canvas.winfo_height() - 10), 0, canvas.winfo_width() - 10, "green"),
          Border(canvas, (5, 10), 90, canvas.winfo_height() - 10, "red"),
          Border(canvas, (canvas.winfo_width() - 10, 10), 90, canvas.winfo_width() - 10, "yellow")]
print([plank.body for plank in planks])
try:
    while True:
        for germ in germs:
            germ.move(random.choice([-1, 1]), random.choice([-1, 1]))
            if germ.dead: germs.remove(germ)
            root.update_idletasks()

        for plank in planks:
            plank.move()
            if plank.dead: planks.remove(plank)
            root.update_idletasks()

        root.update()
        time.sleep(.2)    # This is to make sure the germs don't move too fast to see.

# When the window closes, the loop will run one last time and throw a TclError. Do nothing.
except TclError:
    pass
