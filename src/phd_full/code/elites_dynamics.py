import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

V = 50
BASE_B = 0.5 * V
BASE_L = 0.75 * V

# parameters
c = 1.0      # cost of being elite (smaller so elites can survive when L small)
beta = 0.8   # effectiveness of elites in raising r

delta = 20.0

# strategies: B (bourgeois norm followers), L (bluffers), E (elites)
# x = (xB,xL,xE)

# We want:
# - elites invest in r, get some sanction revenue from L
# - when L is rare, elites are slightly less profitable than B so they don't dominate
# - but a small positive xE is maintained because when L appears, E does better than B


def payoffs(x):
    xB, xL, xE = x
    r = beta * xE
    r = max(0.0, min(1.0, r))

    # base payoffs
    uB = BASE_B
    uL = BASE_L - r * delta

    # elites: base B - cost + sanction revenue
    # total sanction revenue from L: r * delta * xL
    sanction_revenue = r * delta * xL
    share = sanction_revenue / xE if xE > 1e-12 else 0.0
    uE = BASE_B - c + share

    return np.array([uB, uL, uE])


def replicator_three(x, t):
    x = np.maximum(x, 1e-12)
    x = x / np.sum(x)
    F = payoffs(x)
    f_bar = np.dot(x, F)
    return x * (F - f_bar)

# simulate from generic initial condition
x0 = np.array([0.7, 0.25, 0.05])
T = 200
nT = 4000
t = np.linspace(0, T, nT)
sol = odeint(replicator_three, x0, t)

x_final = sol[-1]

plt.figure(figsize=(6,4))
plt.plot(t, sol[:,0], label='x_B (bourgeois)', color='green')
plt.plot(t, sol[:,1], label='x_L (bluffers)', color='red')
plt.plot(t, sol[:,2], label='x_E (elites)', color='blue')
plt.xlabel('time')
plt.ylabel('frequency')
plt.ylim(0,1)
plt.title('Dynamics: bourgeois, bluffers, elites')
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('three_strategy_elites_mixedESS.png', dpi=300)
plt.close()

x_final
