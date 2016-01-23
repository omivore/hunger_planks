from tkinter import *
from germ import Germ

def Killer(Germ):
	def __init__(self, state, canvas: "tkinter.canvas", xy: (int, int), bearing: float):

		super().__init__(state, canvas, xy, bearing, "red")
        self.body = self.canvas.create_oval(0, 0, 11, 11, fill=color, tags="cereal-killer")
        self.spoon = self.canvas.create_oval(0,0,14,14,fill=color)
        self.dead = False;

    def killGerm(self):
        overlap = find_overlapping(self.knife)
            for thing in overlap:
                if thing.gettags() is germ:
                    thing.die()


	def checkForGerm(self):
        self.spoon = self.canvas.create_oval(0,0,14,14,fill="white")
        killGerm()
        self.canvas.delete(self.spoon)

    def die(self):
        self.dead = True;