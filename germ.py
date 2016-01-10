# germ.py

class Germ:
    def __init__(self, canvas, xy, color):
        self.canvas = canvas
        self.id = self.canvas.create_oval(0, 0, 10, 10, fill=color)
        self.canvas.move(self.id, *xy)
