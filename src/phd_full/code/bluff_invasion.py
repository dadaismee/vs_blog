import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

V = 50  # Стандарт Maynard Smith
C = 100

def replicator(X, t, A):
    x = np.maximum(X, 1e-10)
    x = x / np.sum(x)
    F = np.dot(x, A)
    fbar = np.dot(x, F)
    dx = x * (F - fbar)
    return dx

# БАЗОВАЯ матрица Maynard Smith H D B
A3 = np.array([
    [0.5*(V-C), V, 0.75*V - 0.25*C],
    [0, 0.5*V, 0.25*V],
    [0.25*(V-C), 0.75*V, 0.5*V]
])

print("3-strategy (Maynard Smith):\\n", np.round(A3,1))

# РАСШИРЕННАЯ с L (эксплуатирует B)
A4 = np.array([
    [0.5*(V-C), V, 0.75*V - 0.25*C, V],  # H
    [0, 0.5*V, 0.25*V, 0],                # D
    [0.25*(V-C), 0.75*V, 0.5*V, 0.25*V],  # B
    [0, 0.75*V, 0.75*V, 0.5*(V-C)]            # L: L vs D=38.5, L vs B=37.5 (эксплоит!)
])

print("\\n4-strategy with Bluff L:\\n", np.round(A4,1))

t = np.linspace(0, 50, 500)

# Эксперимент 1: вторжение L в B
x0_invade = [0.001, 0.001, 0.996, 0.002]
sol_invade = odeint(replicator, x0_invade, t, args=(A4,))
final_B_invade = sol_invade[-1,2]

# Эксперимент 2: равномерный
x0_equal = [0.25]*4
sol_equal = odeint(replicator, x0_equal, t, args=(A4,))
final_B_equal = sol_equal[-1,2]

print(f"Вторжение L в B: final x_B = {final_B_invade:.4f}")
print(f"Равномерный: final x_B = {final_B_equal:.4f}")

# График вторжения
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.plot(t, sol_invade[:,0], label='H')
plt.plot(t, sol_invade[:,1], label='D')
plt.plot(t, sol_invade[:,2], 'r-', lw=3, label='B')
plt.plot(t, sol_invade[:,3], label='L')
plt.ylabel('Frequency')
plt.title('L Invasion in B (x_L=0.002)')
plt.legend()
plt.grid()

plt.subplot(1,2,2)
plt.plot(t, sol_equal[:,0], label='H')
plt.plot(t, sol_equal[:,1], label='D')
plt.plot(t, sol_equal[:,2], 'r-', lw=3, label='B')
plt.plot(t, sol_equal[:,3], label='L')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.title('Equal Start (0.25 each)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig('maynard_smith_bluff.png', dpi=300)
plt.close()

# CSV
data_invade = np.column_stack((t, sol_invade))
np.savetxt('bluff_invasion.csv', data_invade, delimiter=',', header='t,xH,xD,xB,xL')
