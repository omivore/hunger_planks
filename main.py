#! python
# vim.py

from tkinter import *
from tkinter import ttk
import germ

root = Tk()
root.title("The Hunger Planks")

canvas = Canvas(root)
canvas.pack()

germs = [germ.Germ(canvas, (0, 0), "cyan")]

root.mainloop()
