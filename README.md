# hunger_planks
A clone of otoro.net/planks, with a couple tweaks to implement survival of the fittest.

Small 'germs' wander around based on randomly initialized perceptron networks that act as brains when connected to their movement. Planks randomly spawn and drift slowly in one direction and, when they touch a germ, kill the germ and itself. The germs, like in the original otoro.net version, are given raycasted sight in eight directions and the ability to perceive whether it is seeing a plank or another germ. These are fed into the perceptron, which in turn affects how they move. Germs move by pivoting left or right around an external point.

## Screenshots
A shot of the germs and planks.
<br/><img width=513 height=535 src="https://user-images.githubusercontent.com/5184643/30544768-92a9834c-9c55-11e7-8d05-ea4d4588cd19.png">

## Results
Perhaps this was out of my reach - perhaps the whole concept is systemically flawed. Or perhaps there was an issue with preserving and/or passing down the surviving 'genes'. But the germs did not evolve as I had hoped - in fact, they seemed to tend to chase the planks after a couple generations.

Coming back to this program a year or two later, I see that while a good project, hunger_planks was badly implemented. Choosing to express movement and simulation directly through the tkinter canvas was a mistake, and should this project be revisited, would need to be redone entirely.
