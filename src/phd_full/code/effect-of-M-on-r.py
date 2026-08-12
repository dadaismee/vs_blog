import numpy as np
import matplotlib.pyplot as plt

V = 50

# эмпирический r из M игр с блефом: r = (1/M) Σ E_i
def r_empirical(M, p, rng):
    E = rng.binomial(1, p, size=M)
    return E.mean()

if __name__ == "__main__":
    rng = np.random.default_rng(42)

    Ms = [20, 50, 100]
    p  = 0.5  # вероятность санкции в одной игре

    delta_min, delta_max = 0.1, V
    r_min, r_max = 0.0, 1.0

    # сетка для закраски областей
    delta_vals = np.linspace(delta_min, delta_max, 400)
    r_vals_grid = np.linspace(r_min, r_max, 400)
    Delta, R = np.meshgrid(delta_vals, r_vals_grid)

    # слева от гиперболы r * delta < V/4 (нехватка санкций)
    left_region = (R * Delta < V / 4.0).astype(float)

    plt.figure(figsize=(7, 5))

    # сначала жёлтый фон (справа от гиперболы)
    plt.contourf(Delta, R, np.ones_like(left_region),
                 levels=[-0.1, 0.5, 1.1],
                 colors=["#ffff80"], alpha=0.4)   # жёлтый

    # затем поверх слева фиолетовый
    plt.contourf(Delta, R, left_region,
                 levels=[-0.1, 0.5, 1.1],
                 colors=["#e0b0ff"], alpha=0.6)   # фиолетовый

    # гипербола r * delta = V/4
    r_line = np.linspace(0.01, 1.0, 400)
    delta_line = (V / 4.0) / r_line
    plt.plot(delta_line, r_line, 'k--', linewidth=1.5, label="r·δ = V/4")

    # точки пересечения для разных M
    for M in Ms:
        r_M = r_empirical(M, p, rng)
        if r_M > 0:
            delta_M = V / (4.0 * r_M)
            if delta_min <= delta_M <= delta_max:
                plt.scatter([delta_M], [r_M], color='black', zorder=5)
                plt.text(delta_M, r_M,
                         f" M={M}\nδ≈{delta_M:.1f}, r≈{r_M:.2f}",
                         fontsize=8, ha='left', va='bottom')

    plt.xlim(delta_min, delta_max)
    plt.ylim(r_min, r_max)
    plt.xlabel("δ (размер санкции)")
    plt.ylabel("r (надёжность санкции)")
    plt.title("Пространство (δ, r): слева блеф (фиолет.), справа буржуа (жёлт.)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("delta_r_all_M.png", dpi=300)
    plt.close()

# import numpy as np
# import matplotlib.pyplot as plt
#
# V = 50
#
# # эмпирический r из M игр с блефом: r = (1/M) Σ E_i
# def r_empirical(M, p, rng):
#     E = rng.binomial(1, p, size=M)
#     return E.mean()
#
# if __name__ == "__main__":
#     rng = np.random.default_rng(42)
#
#     Ms = [20, 50, 100, 1000, 100000]
#     p  = 0.5  # вероятность санкции в одной игре
#     delta_vals = np.linspace(0, V, 200)
#
#     # считаем r(M) для разных M
#     r_vals = [r_empirical(M, p, rng) for M in Ms]
#
#     plt.figure(figsize=(6, 4))
#
#     # фон: область выше порога r*delta = V/4 (институт устойчив)
#     Delta, R = np.meshgrid(delta_vals, np.linspace(0, 1, 200))
#     stable = (R * Delta >= V / 4).astype(float)
#     plt.contourf(Delta, R, stable, levels=[-0.1, 0.5, 1.1],
#                  colors=["#f0f0f0", "#d0ffd0"], alpha=0.5)
#
#     # пунктирная линия порога r*delta = V/4
#     r_line = np.linspace(0.01, 1, 200)
#     delta_line = (V / 4) / r_line
#     plt.plot(delta_line, r_line, 'k--', linewidth=1.2, label="r·δ = V/4")
#
#     # уровни r(M) как горизонтальные линии
#     for M, r in zip(Ms, r_vals):
#         plt.axhline(r, linestyle='-', linewidth=1.2, label=f"M={M}, r≈{r:.2f}")
#
#     plt.xlim(0, V)
#     plt.ylim(0, 1)
#     plt.xlabel("δ (размер санкции)")
#     plt.ylabel("r (надёжность санкции)")
#     plt.title("Пространство параметров (δ, r) при разных M")
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig("delta_r_M_levels.png", dpi=300)
#     plt.close()

# import numpy as np
# from scipy.integrate import odeint
# import matplotlib.pyplot as plt
#
# V = 50
#
# def make_BL_matrix(delta, r):
#     delta_eff = r * delta
#     return np.array([
#         [0.5 * V,              0.5 * V      ],   # B row
#         [0.75 * V - delta_eff, 0.5 * V      ]    # L row
#     ])
#
# def replicator_BL(x, t, A):
#     x = np.maximum(x, 1e-12)
#     x = x / np.sum(x)
#     F = A @ x
#     f_bar = np.dot(x, F)
#     return x * (F - f_bar)
#
# def run(delta, r, x0, T=80, nT=4000):
#     A = make_BL_matrix(delta, r)
#     t = np.linspace(0, T, nT)
#     sol = odeint(replicator_BL, x0, t, args=(A,))
#     return sol[-1]  # (x_B, x_L)
#
# # эмпирический r из M игр с блефом
# def r_empirical(M, p, rng):
#     # E_i ~ Bernoulli(p): факт применения санкции в i-й игре
#     E = rng.binomial(1, p, size=M)
#     return E.mean()
#
# if __name__ == "__main__":
#     rng = np.random.default_rng(42)
#
#     x0 = np.array([0.5, 0.5])  # старт: пополам B и L
#     Ms = [1, 10, 100, 1000]
#     p  = 0.5  # вероятность санкции в одной игре (для генерации E_i)
#
#     n_delta = 60
#     delta_vals = np.linspace(0, V, n_delta)
#
#     X = np.zeros((len(Ms), n_delta))  # финальная доля B
#
#     for i, M in enumerate(Ms):
#         # считаем r как эмпирическую среднюю по M играм
#         r = r_empirical(M, p, rng)
#         print(f"M={M}, r≈{r:.3f}")
#         for j, delta in enumerate(delta_vals):
#             x_final = run(delta, r, x0)
#             X[i, j] = x_final[0]
#
#     # аналитический порог при данном r: r*delta = V/4  ⇒  delta_c = V/(4r)
#     # (это уже интерпретация, не меняющая твое определение r)
#     # можно вывести в консоль или нарисовать вертикальными линиями
#
#     plt.figure(figsize=(7, 4))
#     for i, M in enumerate(Ms):
#         # для красоты пересчитаем r тем же способом (или сохраняй r в массив)
#         r = r_empirical(M, p, rng)
#         plt.plot(delta_vals, X[i], label=f"M={M}, r≈{r:.2f}")
#     plt.xlabel("δ (размер санкции)")
#     plt.ylabel("Финальная доля Буржуа")
#     plt.title("Эффект эмпирического r = (1/M) Σ E_i для разных M")
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig("BL_empirical_r_M.png", dpi=300)
#     plt.close()
