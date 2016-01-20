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
canvas.bind("<Button-3>", lambda event: planks.append(Plank.from_random(canvas)))
canvas.pack(fill=BOTH, expand=YES)

root.update()

def get_state():
    return germs + planks

germs = [Germ.from_random(get_state, canvas) for germ_count in range(30)]
planks = [Border(canvas, (5, 10), 0, canvas.winfo_width() - 10, "blue"),
          Border(canvas, (5, canvas.winfo_height() - 10), 0, canvas.winfo_width() - 10, "green"),
          Border(canvas, (5, 10), 90, canvas.winfo_height() - 10, "red"),
          Border(canvas, (canvas.winfo_width() - 10, 10), 90, canvas.winfo_width() - 10, "yellow")]

try:
    spawned = 0
    while True:
<<<<<<< HEAD
        for i in range(len(germs)):
            germs[i].move(1, 1)#random.choice([-1, 1]), random.choice([-1, 1]))
=======
        for germ in germs:
            germ.move(random.choice([-1, 1]), random.choice([-1, 1]))
            if germ.dead: germs.remove(germ)
>>>>>>> origin/master
            root.update_idletasks()

        for plank in planks:
            plank.move()
            if plank.dead: planks.remove(plank)
            root.update_idletasks()

        if spawned > 5:
            if random.choice([0, 1]): planks.append(Plank.from_random(canvas))
            spawned = 0
        else: spawned += 1

        root.update()
<<<<<<< HEAD
        time.sleep(.03)    # This is to make sure the germs don't move too fast to see.
=======
        time.sleep(.2)    # This is to make sure the germs don't move too fast to see.
>>>>>>> origin/master

# When the window closes, the loop will run one last time and throw a TclError. Do nothing.
except TclError:
    pass
