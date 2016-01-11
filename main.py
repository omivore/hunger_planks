#! python
# vim.py

from Tkinter import *
import germ
import random
import time

root = Tk()
root.title("The Hunger Planks")
root.resizable(0, 0)

frame = Frame(root, bd=5)
frame.pack()

canvas = Canvas(frame, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()

germs = [germ.Germ(canvas, (100, 100), "cyan", 5),
         germ.Germ(canvas, (100, 80), "red", -5),
         germ.Germ(canvas, (100, 120), "green", 1),
         germ.Germ(canvas, (100, 150), "gold", 20)]

def spawnGerm(event):
	germs.append(germ.Germ(canvas, (random.randint(0,400), random.randint(0,400)), random.choice(["red","blue" ,"green" ,"magenta" ,"purple" ,"yellow", "azure" ,"cyan" , "snow", "lavenderblush" ,"salmon" ]), random.randint(-32, 32)))

canvas.bind("<Button-1>",spawnGerm)

root.update()

while True:
    for i in range(len(germs)):
        germs[i] = germs[i]()
        root.update_idletasks()
    root.update()
    time.sleep(0.01)
