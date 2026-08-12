import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os

V = 50
ASSETS_DIR = "../assets"

# строим матрицу
def make_BL_matrix(delta):
    return np.array([
        [0.5 * V,          0.5 * V      ],  # B row
        [0.75 * V - delta, 0.5 * V      ]   # L row
    ])

# репликатор
def replicator_BL(x, t, A):
    # делаем начальную долю близкой к 0
    x = np.maximum(x, 1e-12)
    # нормализуем, чтобы сумма долей была 1
    x = x / np.sum(x)
    # умножаем матрицу на вектор долей → payoff чистой стратегии
    F = A @ x
    # считаем средний paoff для каждой стратегии
    f_bar = np.dot(x, F)
    return x * (F - f_bar)

def run(delta, x0, T=80, nT=4000):
    # строим матрицу с конкретной дельтой
    A = make_BL_matrix(delta)
    # linspace создает ряд чисел — похоже на seq в bash
    t = np.linspace(0, T, nT)
    solution = odeint(replicator_BL, x0, t, args=(A,))
    return t, solution

if __name__ == "__main__":
    os.makedirs(ASSETS_DIR, exist_ok=True)
    # можно вернуть сюда (0.98, 0.02), если нужно именно "редкий мутант"
    x0 = np.array([0.98, 0.02])  # (B,L)

    cases = [
        (0.0,   os.path.join(ASSETS_DIR, "BL_delta-zero.png"),   "δ = 0 (< V/4)"),
        (12.5,  os.path.join(ASSETS_DIR, "BL_delta-equal.png"),  "δ = 12.5 (= V/4)"),
        (12.51, os.path.join(ASSETS_DIR, "BL_delta-min.png"),   "δ = 12.51 (> V/4)"),
        (12.58, os.path.join(ASSETS_DIR, "BL_delta-high-full.png"),   "δ = 12.58 (>> V/4)"),
        (37.5, os.path.join(ASSETS_DIR, "BL_delta-high.png"),   "δ = 37.5 (>> V/4)")
    ]

    summary_rows = []

    # считаем и печатаем финальные состояния
    # разбиение кортежа на переменные — типа destructuring в JS
    for delta, fname, title in cases:
        t, solution = run(delta, x0)
        xB_final, xL_final = solution[-1]
        summary_rows.append({
            "delta": delta,
            "xB_final": xB_final,
            "xL_final": xL_final
        })
        print(f"delta = {delta:.2f}, final (B,L) = ({xB_final:.4f}, {xL_final:.4f})")

    # строим и сохраняем графики
    for delta, fname, title in cases:
        t, solution = run(delta, x0)
        # «срезаем» все строки из каждой колонки и сохраняем в переменные
        xB, xL = solution[:, 0], solution[:, 1]

        plt.figure(figsize=(5, 3))
        plt.plot(t, xB, color="green", label="B (Буржуа)")
        plt.plot(t, xL, color="red", linestyle="--", label="L (Блефующий)")
        plt.xlabel("Время")
        plt.ylabel("Доля в популяции")
        plt.ylim(0, 1)
        plt.title(title)
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(fname, dpi=300)
        plt.close()
