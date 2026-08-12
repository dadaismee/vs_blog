import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

V = 50

def make_BL_matrix(delta, r):
    # усреднённая санкция: E∈{0,1}, r = E[E] => эффективный штраф r*delta
    delta_eff = r * delta
    return np.array([
        [0.5 * V,            0.5 * V        ],  # B row
        [0.75 * V - delta_eff, 0.5 * V      ]   # L row
    ])

def replicator_BL(x, t, A):
    x = np.maximum(x, 1e-12)
    x = x / np.sum(x)
    F = A @ x
    f_bar = np.dot(x, F)
    return x * (F - f_bar)

def run(delta, r, x0, T=80, nT=4000):
    A = make_BL_matrix(delta, r)
    t = np.linspace(0, T, nT)
    sol = odeint(replicator_BL, x0, t, args=(A,))
    return sol[-1]  # конечное состояние (x_B, x_L)

if __name__ == "__main__":
    # редкий мутант L в популяции B
    x0 = np.array([0.5, 0.5])

    n_delta, n_r = 50, 50
    delta_vals = np.linspace(0, V, n_delta)  # по оси x
    r_vals     = np.linspace(0, 1,  n_r)      # по оси y

    # X[i,j] = финальная доля B при (delta_j, r_i)
    X = np.zeros((n_r, n_delta))

    for i, r in enumerate(r_vals):
        for j, delta in enumerate(delta_vals):
            x_final = run(delta, r, x0)
            X[i, j] = x_final[0]  # x_B

    plt.figure(figsize=(6, 4))
    im = plt.imshow(
        X,
        origin="lower",
        aspect="auto",
        extent=[delta_vals[0], delta_vals[-1], r_vals[0], r_vals[-1]],
        vmin=0, vmax=1,
        cmap="viridis"
    )
    cbar = plt.colorbar(im, label="Вероятность агента следовать правилу")
    plt.xlabel("δ (размер санкции)")
    plt.ylabel("r (надёжность санкции)")
    plt.title("Вероятность агента следовать правилу")
    plt.tight_layout()
    plt.savefig("BL_heatmap_delta_r.png", dpi=300)
    plt.close()
