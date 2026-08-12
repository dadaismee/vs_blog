import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# параметры игры
V = 50
C = 100

def make_matrix(delta, r):
    # эффективная санкция r*delta
    delta_eff = r * delta
    # порядок стратегий: H, D, B, L
    return np.array([
        [-25,   50,    12.5,            50],
        [  0,   25,    12.5,             0],
        [-12.5, 37.5,  25,            12.5],
        [  0,   37.5,  37.5 - delta_eff, 25]
    ], dtype=float)

def replicator(x, t, A):
    x = np.maximum(x, 1e-12)
    x = x / np.sum(x)
    F = A @ x
    f_bar = np.dot(x, F)
    return x * (F - f_bar)

if __name__ == "__main__":
    # время интегрирования
    T = 120
    nT = 3000
    t = np.linspace(0, T, nT)

    # сетка по δ и r
    n_delta = 80
    n_r     = 80

    delta_vals = np.linspace(0, 40, n_delta)   # ось x: размер санкции δ
    r_vals     = np.linspace(0, 1,  n_r)       # ось y: надёжность r

    # img[i,j,:] = RGB-цвет финальной популяции при (delta_j, r_i)
    img = np.zeros((n_r, n_delta, 3))

    # базовые цвета стратегий:
    # H (ястреб)   - красный     (1, 0, 0)
    # B (буржуа)   - жёлтый      (1, 1, 0)
    # L (блеф)     - фиолетовый  (1, 0, 1)
    # D (голубь)   - синий       (0, 0, 1)
    color_H = np.array([1.0, 0.0, 0.0])
    color_B = np.array([1.0, 1.0, 0.0])
    color_L = np.array([1.0, 0.0, 1.0])
    color_D = np.array([0.0, 0.0, 1.0])

    # фиксированное начальное состояние: почти все B, немного L
    x0 = np.array([0.0, 0.0, 0.98, 0.02])

    for i, r in enumerate(r_vals):
        for j, delta in enumerate(delta_vals):
            A = make_matrix(delta, r)
            sol = odeint(replicator, x0, t, args=(A,))
            H, D, B, L = sol[-1]

            # линейная смесь базовых цветов по долям стратегий
            color = (
                H * color_H +
                B * color_B +
                L * color_L +
                D * color_D
            )

            # нормируем, чтобы максимум не превышал 1
            m = color.max()
            if m > 1:
                color = color / m

            img[i, j, :] = color

    plt.figure(figsize=(7, 4))
    plt.imshow(
        img,
        origin="lower",
        aspect="auto",
        extent=[delta_vals[0], delta_vals[-1], r_vals[0], r_vals[-1]]
    )
    plt.xlabel("δ (размер санкции)")
    plt.ylabel("r (надёжность санкции)")
    plt.title("Фазовая карта: H=красн., B=жёлт., L=фиол., D=син.")
    plt.tight_layout()
    plt.savefig("HDBL_phase_delta_r.png", dpi=300)
    plt.close()
