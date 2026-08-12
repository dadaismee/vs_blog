import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os

V = 50
ASSETS_DIR = "../assets"

def make_BL_matrix(delta):
    return np.array([
        [0.5 * V,          0.5 * V],
        [0.75 * V - delta, 0.5 * V]
    ])

def replicator_BL(x, t, A):
    x = np.maximum(x, 1e-12)
    x = x / np.sum(x)
    F = A @ x
    f_bar = np.dot(x, F)
    return x * (F - f_bar)

def run(delta, x0, T=80, nT=4000):
    A = make_BL_matrix(delta)
    t = np.linspace(0, T, nT)
    solution = odeint(replicator_BL, x0, t, args=(A,))
    return t, solution

if __name__ == "__main__":
    os.makedirs(ASSETS_DIR, exist_ok=True)
    x0 = np.array([0.98, 0.02])  # (B,L)

    cases = [
        (0.0,   os.path.join(ASSETS_DIR, "BL_delta-zero.png"),   "δ = 0 (< V/4)"),
        (12.5,  os.path.join(ASSETS_DIR, "BL_delta-equal.png"),  "δ = 12.5 (= V/4)"),
        (12.51, os.path.join(ASSETS_DIR, "BL_delta-min.png"),   "δ = 12.51 (> V/4)"),
        (12.58, os.path.join(ASSETS_DIR, "BL_delta-high-full.png"), "δ = 12.58 (> V/4)"),
        (37.5,  os.path.join(ASSETS_DIR, "BL_delta-high.png"),   "δ = 37.5 (>> V/4)")
    ]

    summary_rows = []

    results = []
    for delta, fname, title in cases:
        t, solution = run(delta, x0)
        xB_final, xL_final = solution[-1]
        summary_rows.append({
            "delta": delta,
            "xB_final": xB_final,
            "xL_final": xL_final
        })
        print(f"delta = {delta:.2f}, final (B,L) = ({xB_final:.4f}, {xL_final:.4f})")
        results.append((t, solution, fname, title))

    # 2. Одно окно с 4 графиками (берём первые 4 cases)
    fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharex=True, sharey=True)

    for i, (t, solution, fname, title) in enumerate(results[:4]):
        row = i // 2
        col = i % 2
        ax = axes[row, col]

        xB, xL = solution[:, 0], solution[:, 1]

        ax.plot(t, xB, color="green", label="B (Буржуа)")
        ax.plot(t, xL, color="red", linestyle="--", label="L (Блефующий)")
        ax.set_ylim(0, 1)
        ax.set_title(title, fontsize=10)
        ax.grid(alpha=0.3)
        if row == 1:
            ax.set_xlabel("Время")
        if col == 0:
            ax.set_ylabel("Доля в популяции")

    # общая лёгкая подпись легенды (один раз для всех)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)  # место для легенды
    # plt.show()
    plt.savefig(os.path.join(ASSETS_DIR, "BL_combined_4-0.98.png"), dpi=300)
    plt.close()
