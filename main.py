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
    return germs, planks, killers

def set_state(new_germs, new_planks, new_killers, newly_dead=None):
    germs = new_germs
    planks = new_planks
    killers = new_killers
    if newly_dead:
        death.append(newly_dead)

germs = [Germ.from_random(get_state, set_state, canvas) for germ_count in range(30)]
planks = [Border(get_state, set_state, canvas, (5, 10), 0, canvas.winfo_width() - 10, "blue"),
          Border(get_state, set_state, canvas, (5, canvas.winfo_height() - 10), 0, canvas.winfo_width() - 10, "green"),
          Border(get_state, set_state, canvas, (5, 10), 90, canvas.winfo_height() - 10, "red"),
          Border(get_state, set_state, canvas, (canvas.winfo_width() - 10, 10), 90, canvas.winfo_width() - 10, "yellow")]
killers = []#Killer.from_random(get_state, set_state, canvas) for killer_count in range(4)]

root.update()
death = []
try:
    spawned = 0
    while True:
        for germ in germs:
            germ.execute()
            root.update_idletasks()

        for plank in planks:
            plank.move()
            root.update_idletasks()

        """
        for killer in killers:
            killer.move(random.choice([-1,1]), random.choice([-1,1]))
            killer.checkForGerm()
            if killer.dead: killer.remove(killer)
        """

        if spawned > 5:
            if random.choice([0, 1]): planks.append(Plank.from_random(get_state, set_state, canvas))
            spawned = 0
        else: spawned += 1

        root.update()

# When the window closes, the loop will run one last time and throw a TclError. Do nothing.
except TclError:
    pass
