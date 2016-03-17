import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# define the figure hierarchy (figure holds axes)
figure = plt.figure()
axes = figure.add_subplot('111',aspect='equal')
axes.set_xlim(-2,7)
axes.set_ylim(-2,7)

# add a patch to the axis
ball = plt.Circle((0,0), radius=2)
axes.add_patch(ball)

def animate(i):
    # shift the ball's position
    ball.center = (i/10.,i/15.)
    return ball,

# afterwards, switch to zoomable GUI mode

ani = animation.FuncAnimation(figure, 
                              animate, 
                              np.arange(1, 50), 
                              interval=25)

plt.show()
