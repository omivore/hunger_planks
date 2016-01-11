#! python
# vim.py

from tkinter import *
from tkinter import ttk
import germ

root = Tk()
root.title("The Hunger Planks")
root.resizable(0, 0)

frame = Frame(root, bd=5, relief=SUNKEN)
frame.pack()

canvas = Canvas(frame, width=500, height=200, bd=0, highlightthickness=0)
canvas.pack()

germs = [germ.Germ(canvas, (100, 100), "cyan", 5),
         germ.Germ(canvas, (100, 80), "red", -5),
         germ.Germ(canvas, (100, 120), "green", 1),
         germ.Germ(canvas, (100, 150), "gold", 20)]

root.update()

while True:
    for i in range(len(germs)):
        germs[i] = germs[i]()
        root.update_idletasks()
    root.update()
