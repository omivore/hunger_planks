#! python
# vim.py

from tkinter import *
import germ
import random
import time

root = Tk()
root.title("The Hunger Planks")
root.resizable(0, 0)

canvas = Canvas(root, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()

germs = [germ.Germ(canvas, (100, 100), "cyan", 3)]

def spawnGerm(event):
    germ_colors = ["red","blue" ,"green" ,"magenta" ,"purple" ,"yellow", "azure" ,"cyan" , "snow", "lavenderblush" ,"salmon" ]
    germs.append(germ.Germ(canvas, (random.randint(0,500), random.randint(0,500)), random.choice(germ_colors), random.randint(-32, 32)))

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
