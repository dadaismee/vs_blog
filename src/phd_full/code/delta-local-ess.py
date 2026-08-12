import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

V = 50

def make_BL_matrix(delta):
    return np.array([
        [0.5 * V,          0.5 * V      ],
        [0.75 * V - delta, 0.5 * V      ]
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
    sol = odeint(replicator_BL, x0, t, args=(A,))
    return sol[-1, 0]  # финальная доля B

if __name__ == "__main__":
    x0 = np.array([0.98, 0.02])

    n_delta = 200
    delta_vals = np.linspace(10, 15, n_delta)
    final_B = np.array([run(delta, x0) for delta in delta_vals])

    threshold = V / 4  # 12.5

    plt.figure(figsize=(6, 4))
    plt.plot(delta_vals, final_B, color="black", linewidth=1.5, label="финальная доля B")

    # области по разные стороны порога
    mask_left = delta_vals <= threshold
    mask_right = delta_vals >= threshold

    # слева от порога — область блефа (L доминирует)
    plt.fill_between(
        delta_vals[mask_left],
        final_B[mask_left],
        10,
        color="red",
        alpha=0.3,
        label="область блефа (L)"
    )

    # справа от порога — область буржуа
    plt.fill_between(
        delta_vals[mask_right],
        final_B[mask_right],
        0,
        color="green",
        alpha=0.3,
        label="область буржуа (B)"
    )

    # вертикальная линия порога
    plt.axvline(threshold, color="gray", linestyle="--")
    plt.text(threshold + 0.3, 0.5, "δ = V/4", rotation=90, va="center", color="gray")

    plt.xlabel("δ (размер санкции)")
    plt.ylabel("финальная доля B")
    plt.ylim(0, 1)
    plt.xlim(10, 15)
    plt.title("Режимы динамики: блеф vs буржуа")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("BL_final_B_vs_delta_filled.png", dpi=300)
    plt.close()
