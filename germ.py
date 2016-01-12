# germ.py

class Germ:
    def __init__(self, canvas, xy, color, velocity):
        # 'Adopts' the canvas, and then creates itself on the canvas with the color given.
        # Then moves itself to the given xy coordinate.
        self.canvas = canvas
        self.id = self.canvas.create_oval(0, 0, 10, 10, fill=color)
        self.canvas.move(self.id, *xy)
        
        # Determines the starting speed and direction. velocity contains two 'speeds', and the signs
        # is the direction, left or right, or down or up, corresponding to negative or positive.
        self.velocity = list(velocity)

    def move(self):
        xy = self.canvas.coords(self.id)
        if xy[1] <= 0 or xy[3] >= 499: self.velocity[1] *= -1
        if xy[2] >= 499 or xy[0] <= 0: self.velocity[0] *= -1
        self.canvas.move(self.id, *self.velocity)
