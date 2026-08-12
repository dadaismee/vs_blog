import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os

ASSETS_DIR = '../assets'
os.makedirs(ASSETS_DIR, exist_ok=True)

V = 50
C = 100

def make_matrix(delta_eff):
    # delta_eff = r * delta
    return np.array([
        [-25,   50,    12.5,              50],
        [  0,   25,    12.5,               0],
        [-12.5, 37.5,  25,              12.5],
        [  0,   37.5,  37.5 - delta_eff, 25]
    ], dtype=float)

def replicator(x, t, A):
    x = np.maximum(x, 1e-12)
    x = x/np.sum(x)
    F = A @ x
    f_bar = np.dot(x, F)
    return x*(F - f_bar)

T = 200
nT = 8000
t = np.linspace(0, T, nT)

n_delta = 60
n_r = 60

delta_vals = np.linspace(0, 40, n_delta)   # ось x
r_vals     = np.linspace(0, 1,  n_r)       # ось y

X_H = np.zeros((n_r, n_delta))
X_D = np.zeros((n_r, n_delta))
X_B = np.zeros((n_r, n_delta))
X_L = np.zeros((n_r, n_delta))

# фиксированное начальное состояние, например почти все B, немного L
x0 = np.array([0.0, 0.0, 0.98, 0.02])

for i, r in enumerate(r_vals):
    for j, delta in enumerate(delta_vals):
        delta_eff = r * delta
        A = make_matrix(delta_eff)
        sol = odeint(replicator, x0, t, args=(A,))
        xf = sol[-1]
        X_H[i, j], X_D[i, j], X_B[i, j], X_L[i, j] = xf

np.savez(os.path.join(ASSETS_DIR, 'HDBL_heat_data_delta_r.npz'),
         delta_vals=delta_vals, r_vals=r_vals,
         X_H=X_H, X_D=X_D, X_B=X_B, X_L=X_L)

fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)
axes = axes.ravel()

data = [X_H, X_D, X_B, X_L]
labels = ['H', 'D', 'B', 'L']

for ax, Z, lab in zip(axes, data, labels):
    im = ax.imshow(
        Z,
        origin='lower',
        aspect='auto',
        extent=[delta_vals[0], delta_vals[-1], r_vals[0], r_vals[-1]],
        vmin=0, vmax=1,
        cmap='viridis'
    )
    ax.set_title(f'Финальная доля {lab}')
    ax.grid(False)

fig.colorbar(im, ax=axes.tolist(), label='Доля в популяции')
fig.text(0.5, 0.04, 'δ (размер санкции)', ha='center')
fig.text(0.04, 0.5, 'r (надёжность санкции)', va='center', rotation='vertical')

heat4_path = os.path.join(ASSETS_DIR, 'HDBL_heatmaps_4panel.png')
plt.savefig(heat4_path, dpi=300)
plt.close()

print('saved', heat4_path)
