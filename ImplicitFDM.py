import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

T0 = 300.0
Tb = 400.0
al = 1.0e-4
dx = 0.02
L = 2.0

#userinputs
t_end = float(input("Enter the end time of the simulation (in seconds): "))
dt = float(input("Enter the time step of the simulation (in seconds): "))

# time step calculation
nt = int(t_end/dt)

# spatial grid calculation
nx = int(L/dx) + 1

T = np.zeros((nx,nt)) # Set temperature matrix
T[:,0] = T0

# boundary conditions
T[0,:] = Tb
T[-1,:] = T[-2,:]

#Implicit scheme matrix
r = al*dt/(dx*dx)
A = np.zeros((nx,nx))
A[0,0] = 1.0
A[-1,-1] = 1.0
for i in range(1,nx-1):
    A[i,i] = 1.0 + 2.0*r
    A[i,i-1] = -r
    A[i,i+1] = -r
B = np.linalg.inv(A)

# temperature at each time step
for n in range(1,nt):
    T[:,n] = np.dot(B,T[:,n-1])

# Plot creation that is updating by time 
fig, ax = plt.subplots()
ax.set_xlabel('Position (m)')
ax.set_ylabel('Temperature (K)')
ax.set_ylim([T0-20,Tb+50])
ax.set_xlim([0,L])
line, = ax.plot([], [], lw=2)
frame_texts = ax.text(0.05, 0.9, '', transform=ax.transAxes)

def init():
    line.set_data([], [])
    frame_texts.set_text('')
    return (line, frame_texts)

def animate(i):
    if i == nt - 1:
        anim.event_source.stop()
    x = np.linspace(0, L, nx)
    y = T[:,i]
    line.set_data(x, y)
    frame_texts.set_text('Time = {} s'.format(i*dt))
    return (line, frame_texts)

anim = FuncAnimation(fig, animate, init_func=init, frames=nt, interval=50, blit=True)

plt.show()
