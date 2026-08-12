import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

V = 50
C = 100

# 4 стратегии: H, D, B, L
# delta и r влияют только на L vs B

def make_HDBL_matrix(delta, r):
    delta_eff = r * delta
    A = np.zeros((4, 4))
    # индексы: 0=H, 1=D, 2=B, 3=L

    # стандартная H,D,B-часть (одна из версий Hawk-Dove-Bourgeois)
    A[0,0] = 0.5 * (V - C)   # H vs H
    A[0,1] = V               # H vs D
    A[0,2] = 0.75*V - 0.25*C # H vs B

    A[1,0] = 0               # D vs H
    A[1,1] = 0.5 * V         # D vs D
    A[1,2] = 0.25 * V        # D vs B

    A[2,0] = 0.25*(V - C)    # B vs H
    A[2,1] = 0.75 * V        # B vs D
    A[2,2] = 0.5 * V         # B vs B

    # взаимодействия с L (упрощённо)
    A[0,3] = V               # H vs L
    A[3,0] = 0               # L vs H

    A[1,3] = 0               # D vs L
    A[3,1] = 0.75 * V        # L vs D

    A[2,3] = 0.5 * V         # B vs L
    A[3,2] = 0.75 * V - delta_eff  # L vs B, штраф через r*delta

    A[3,3] = 0.5 * (V - C)   # L vs L (аналог H vs H, опционально)

    return A

def replicator_full(x, t, A):
    x = np.maximum(x, 1e-12)
    x = x / np.sum(x)
    F = A @ x
    f_bar = np.dot(x, F)
    return x * (F - f_bar)

def run_full(delta, r, x0, T=200, nT=4000):
    A = make_HDBL_matrix(delta, r)
    t = np.linspace(0, T, nT)
    sol = odeint(replicator_full, x0, t, args=(A,))
    return sol[-1]  # финальное состояние (x_H, x_D, x_B, x_L)

if __name__ == "__main__":
    # начальное состояние: почти все B, немного L, чуть-чуть H,D
    x0 = np.array([0.01, 0.01, 0.96, 0.02])

    n_delta, n_r = 40, 40
    delta_vals = np.linspace(0, 50, n_delta)
    r_vals     = np.linspace(0, 1,  n_r)

    XB = np.zeros((n_r, n_delta))  # финальная доля B
    XL = np.zeros((n_r, n_delta))  # финальная доля L

    for i, r in enumerate(r_vals):
        for j, delta in enumerate(delta_vals):
            x_final = run_full(delta, r, x0)
            XB[i, j] = x_final[2]
            XL[i, j] = x_final[3]

    # heatmap для B
    plt.figure(figsize=(6, 5))
    imB = plt.imshow(
        XB,
        origin="lower",
        aspect="auto",
        extent=[delta_vals[0], delta_vals[-1], r_vals[0], r_vals[-1]],
        vmin=0, vmax=1, cmap="viridis"
    )
    cbarB = plt.colorbar(imB, label="Final frequency of B")
    plt.xlabel("δ (sanction size)")
    plt.ylabel("r (sanction reliability)")
    plt.title("Final frequency of B in H,D,B,L game")
    plt.tight_layout()
    plt.savefig("HDBL_heatmap_B_delta_r.png", dpi=300)
    plt.close()

    # heatmap для L
    plt.figure(figsize=(6, 5))
    imL = plt.imshow(
        XL,
        origin="lower",
        aspect="auto",
        extent=[delta_vals[0], delta_vals[-1], r_vals[0], r_vals[-1]],
        vmin=0, vmax=1, cmap="magma"
    )
    cbarL = plt.colorbar(imL, label="Final frequency of L")
    plt.xlabel("δ (sanction size)")
    plt.ylabel("r (sanction reliability)")
    plt.title("Final frequency of L in H,D,B,L game")
    plt.tight_layout()
    plt.savefig("HDBL_heatmap_L_delta_r.png", dpi=300)
    plt.close()
