import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

V = 50
C = 100

A3 = np.array([
    [0.5*(V-C), V, 0.75*V - 0.25*C],
    [0, 0.5*V, 0.25*V],
    [0.25*(V-C), 0.75*V, 0.5*V]
])

print('Payoff matrix 3-strat:\n', np.round(A3,1))


def replicator(x, t, A):
    x = np.maximum(x, 1e-10)
    x = x/np.sum(x)
    F = x @ A
    fbar = np.dot(x, F)
    return x * (F - fbar)

# time
t = np.linspace(0, 80, 4000)

# 1) near pure B
x0_B = [0.01, 0.01, 0.98]
sol_B = odeint(replicator, x0_B, t, args=(A3,))

# 2) equal start
x0_eq = [1/3, 1/3, 1/3]
sol_eq = odeint(replicator, x0_eq, t, args=(A3,))

print('Final near B:', np.round(sol_B[-1],3))
print('Final equal  :', np.round(sol_eq[-1],3))

# save CSV
np.savetxt('ms_3str_nearB.csv', np.column_stack((t, sol_B)), delimiter=',', header='t,xH,xD,xB')
np.savetxt('ms_3str_equal.csv', np.column_stack((t, sol_eq)), delimiter=',', header='t,xH,xD,xB')

# plot
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(t, sol_B[:,0], label='H')
plt.plot(t, sol_B[:,1], label='D')
plt.plot(t, sol_B[:,2], label='B', linewidth=2)
plt.title('Near pure B')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(1,2,2)
plt.plot(t, sol_eq[:,0], label='H')
plt.plot(t, sol_eq[:,1], label='D')
plt.plot(t, sol_eq[:,2], label='B', linewidth=2)
plt.title('Equal start (1/3 each)')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('ms_3str_experiment.png', dpi=300)
plt.close()
