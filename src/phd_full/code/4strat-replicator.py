import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os

ASSETS_DIR = '../assets'
os.makedirs(ASSETS_DIR, exist_ok=True)

V = 50
C = 100


def make_matrix(delta):
    return np.array([
        [-25,   50,    12.5,        50],
        [  0,   25,    12.5,         0],
        [-12.5, 37.5,  25,        12.5],
        [  0,   37.5,  37.5 - delta, 25]
    ], dtype=float)


def replicator(x, t, A):
    x = np.maximum(x, 1e-12)
    x = x/np.sum(x)
    F = A @ x
    f_bar = np.dot(x, F)
    return x*(F - f_bar)


T = 80
nT = 4000
t = np.linspace(0, T, nT)

# new initial condition: H=0, D=0, B=0.98, L=0.02
x0 = np.array([0.0, 0.0, 0.98, 0.02])

cases = [
    (0.0, 'delta0'),
    (12.5, 'delta12.5'),
    (12.75, 'delta12.75'),
    (12.76, 'delta12.76'),
]

summaries = []

fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)
axes = axes.ravel()

for ax, (delta, tag) in zip(axes, cases):
    A = make_matrix(delta)
    sol = odeint(replicator, x0, t, args=(A,))
    final = sol[-1]
    summaries.append((delta, final))

    ax.plot(t, sol[:,0], label='H', color='black')
    ax.plot(t, sol[:,1], label='D', color='blue')
    ax.plot(t, sol[:,2], label='B', color='green')
    ax.plot(t, sol[:,3], label='L', color='red')
    ax.set_title(f'delta = {delta}')
    ax.grid(alpha=0.3)

axes[0].legend(loc='upper right')
fig.text(0.5, 0.04, 'time', ha='center')
fig.text(0.04, 0.5, 'frequency', va='center', rotation='vertical')
plt.tight_layout(rect=[0.06, 0.06, 1, 1])

fname = os.path.join(ASSETS_DIR, '4-strat-replicator.png')
plt.savefig(fname, dpi=200)
plt.close()

print('Final frequencies for x0=(0,0,0.98,0.02):')
for delta, final in summaries:
    print('delta', delta, '->', final)
