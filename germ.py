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
        self.velocity = [None, None] # Initialize first so they work in the if and else's
        if velocity[0] > 0:
            self.velocity[0] = velocity[0] 
            self.start = self.right
        else:
            self.velocity[0] = -velocity[0]
            self.start = self.left

        if velocity[1] > 0:
            self.velocity[1] = velocity[1]
            self.start = self.up
        else:
            self.velocity[1] = -velocity[1]
            self.start = self.down

    def __call__(self):
        return self.start

    def up(self):
        xy = self.canvas.coords(self.id)
        if xy[1] <= 0:
            return self.down
        self.canvas.move(self.id, 0, -self.velocity[1])
        return self.up

    def down(self):
        xy = self.canvas.coords(self.id)
        if xy[3] >= 499:
            return self.up
        self.canvas.move(self.id, 0, self.velocity[1])
        return self.down

    def right(self):
        xy = self.canvas.coords(self.id)
        if xy[2] >= 499:
            return self.left
        self.canvas.move(self.id, self.velocity[0], 0)
        return self.right

    def left(self):
        xy = self.canvas.coords(self.id)
        if xy[0] <= 0:
            return self.right
        self.canvas.move(self.id, -self.velocity[0], 0)
        return self.left
