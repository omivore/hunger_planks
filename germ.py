# germ.py
# comment the stuffs pls 
class Germ:
    def __init__(self, canvas, xy, color, delta): #initialize the contructors
        self.canvas = canvas
        self.id = self.canvas.create_oval(0, 0, 10, 10, fill=color)
        self.canvas.move(self.id, *xy)
        if delta > 0:
            self.delta = delta
            self.start = self.right
        else:
            self.delta = -delta
            self.start = self.left

    def __call__(self):
        return self.start

    def right(self):
        xy = self.canvas.coords(self.id)
        if xy[1] >= 20:
            return self.left
        self.canvas.move(self.id, self.delta, 0)
        return self.right

    def left(self):
        xy = self.canvas.coords(self.id)
        if xy[0] <= 0:
            return self.right
        self.canvas.move(self.id, -self.delta, 0)
        return self.left
