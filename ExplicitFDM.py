import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L = 2
k = 0.0001
nx = 101

# grid spacing coordinates
dx = L / (nx - 1)
x = np.linspace(0, L, nx)
t_end = float(input("Enter the end time of the simulation (in seconds): "))
nt = int(t_end / (0.5 * dx**2 / k)) # number of iterations
dt = t_end / nt # timestep
alpha = k * dt / dx**2 # stabilityfactor so that the graph does not diverge

# Initial and boundary conditions
T = np.ones(nx) * 300 # Temperature of the rod at the initial time
T[0] = 400 # Temperature of the rod at one end
T[-1] = 300 # Temperature of the rod at the boundary

#plot creation
fig, ax = plt.subplots()
ax.set_xlabel('Position (m)') # X axis label
ax.set_ylabel('Temperature (K)') # Y axis label
ax.set_ylim([290, 450]) # Limits of the Y axis
ax.set_xlim([0, L]) # Limits of the X axis

line, = ax.plot([], [], lw=2, color = 'k') #Line to be animated

# Initialize the text object for displaying the current time
frame_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

#initilise function for animation
def init():
    line.set_data([], [])
    frame_text.set_text('')
    return (line, frame_text)

def animate(i):
    # Updating the temperature distribution using the explicit scheme
    T[1:-1] += alpha * (T[2:] - 2*T[1:-1] + T[:-2])

    # Updating the line object with the new temperature distribution
    line.set_data(x, T)

    frame_text.set_text('Time = {} s'.format(i*dt))
    return (line, frame_text)

anim = FuncAnimation(fig, animate, init_func=init, frames=nt, interval=50, blit=True)
plt.show()