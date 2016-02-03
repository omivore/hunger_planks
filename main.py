#! python
# vim.py

# Program flags.
sample_size = 50       # The number of initial germs in each generation.
use_memorized = False   # Whether to pull brains from file, if such a file exists.
save_last = (True, 5)   # Whether to save the brains, and how many generations to go through before a save.

from tkinter import *
import time, random
import pickle
from germ import Germ
from plank import Plank, Border
from brain import Brain

root = Tk()
root.title("The Hunger Planks")

canvas = Canvas(root, width=500, height=500)
canvas.bind("<Button-1>", lambda event: state.germs.append(Germ.from_random(state)))
canvas.bind("<Button-3>", lambda event: state.planks.append(Plank.from_random(state)))
canvas.pack(fill=BOTH, expand=YES)

root.update()

class State():
    def __init__(self, canvas):
        self.canvas = canvas
        self.spawn()
        self.current_gen = 0

    def spawn(self, brains: (Brain for _ in range(sample_size))=(None for _ in range(sample_size))):
        if use_memorized:
            past_brains = import_brains()
            if past_brains:
                brains = (brain for brain in past_brains)
        self.germs = [Germ.from_random(self, brains.__next__()) for _ in range(sample_size)]
        self.planks = [Border(self, (5, 10), 0, self.canvas.winfo_width() - 10, "blue"),
                       Border(self, (5, self.canvas.winfo_height() - 10), 0, self.canvas.winfo_width() - 10, "green"),
                       Border(self, (5, 10), 90, self.canvas.winfo_height() - 10, "red"),
                       Border(self, (self.canvas.winfo_width() - 10, 10), 90, self.canvas.winfo_width() - 10, "yellow")]
        self.killers = []#Killer.from_random(get_state, set_state, canvas) for killer_count in range(4)]
        self.death_log = []

    def kill(self, citizen):
        # Remove object from canvas records.
        self.canvas.delete(citizen.body)

        # Remove object from state records.
        if citizen in self.germs:
            self.germs.remove(citizen)
            self.death_log.append(citizen)

            if not self.germs:
                # No germs; pause, cross-mutate best, reset and repopulate.
                self.advance_gen()
        elif citizen in self.planks:
            self.planks.remove(citizen)
        elif citizen in self.killers:
            self.killers.remove(citizen)

    def advance_gen(self):
        # Clear the screen.
        self.canvas.delete(ALL)
        root.update()
        self.current_gen += 1

        best_brains = [germ.brain for germ in self.death_log[:30]]
        new_brains = (Brain.cross_mutate(best_brains) for _ in range(sample_size))

        if save_last[0]:
            if self.current_gen % save_last[1] == 0:
                self.export_brains(best_brains)

        self.spawn(new_brains)

    def export_brains(self, brains: [Brain for _ in range(30)]):
        with open("brains.pickle", "wb") as file:
            pickle.dump(brains, file)

    def import_brains(self):
        try:
            with open("brains.pickle", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None


state = State(canvas)
root.update()
try:
    spawned = 0
    while True:
        for germ in state.germs:
            germ.execute()
            root.update_idletasks()

        for plank in state.planks:
            plank.move()
            root.update_idletasks()

        """
        for killer in state.killers:
            killer.move(random.choice([-1,1]), random.choice([-1,1]))
            killer.checkForGerm()
            if killer.dead: killer.remove(killer)
        """

        if spawned > 5:
            if random.choice([0, 1]): state.planks.append(Plank.from_random(state))
            spawned = 0
        else: spawned += 1

        root.update()

# When the window closes, the loop will run one last time and throw a TclError. Do nothing.
except TclError:
    pass
