import numpy as np
import matplotlib.pyplot as plt

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

# Plotting temperature at fixed fractions of the end time and at the end time
fig, ax = plt.subplots()
ax.set_xlabel('Position (m)')
ax.set_ylabel('Temperature (K)')
ax.set_ylim([T0-20,Tb+50])
ax.set_xlim([0,L])
ax.set_title('Temperature Distribution at Different Time Intervals')
colors = ['g', 'b', 'c', 'm', 'y']
times = [int(nt/100), int(nt/20), int(nt/10), int(nt/5), nt-1]
for i, t in enumerate(times):
    x = np.linspace(0, L, nx)
    y = T[:,t]
    ax.plot(x, y, colors[i], label='Time = {} s'.format(t*dt))
ax.legend()

plt.show()
