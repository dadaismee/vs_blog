import numpy as np
import matplotlib.pyplot as plt

# Параметры игры для второго игрока
# E[u(D)] = 25*alpha
# E[u(H)] = -25 + 75*alpha
# Delta u(alpha) = -25 + 50*alpha

def delta_u(alpha):
    return -25 + 50*alpha

# Сетка по delta и r
n_delta = 200
n_r = 200

delta_vals = np.linspace(0, 40, n_delta)   # размер санкции
r_vals     = np.linspace(0, 1,  n_r)       # надёжность

# Выбери значение alpha, которое хочешь проиллюстрировать
alpha = 0.75  # например, мягкое поведение "первых" 75% времени

Du = delta_u(alpha)

Z = np.zeros((n_r, n_delta))

for i, r in enumerate(r_vals):
    for j, delta in enumerate(delta_vals):
        eff = r * delta  # ожидаемая санкция
        if Du <= 0:
            # премии за отклонение нет вообще: правило поддерживается структурой игры
            Z[i, j] = -1
        else:
            if eff + 1e-6 < Du:
                Z[i, j] = 1   # санкции не покрываютDelta u: отклонение выгодно
            elif eff > Du + 1e-6:
                Z[i, j] = -1  # санкции достаточны: следовать правилу выгоднее
            else:
                Z[i, j] = 0   # пограничный случай r*delta = Delta u

cmap = plt.cm.get_cmap('bwr', 3)  # синий–белый–красный

plt.figure(figsize=(6, 4))
plt.imshow(
    Z,
    origin='lower',
    aspect='auto',
    extent=[delta_vals[0], delta_vals[-1], r_vals[0], r_vals[-1]],
    cmap=cmap,
    vmin=-1, vmax=1
)
cbar = plt.colorbar(ticks=[-1, 0, 1])
cbar.ax.set_yticklabels([
    'Институт устойчив\n(правило выгодно)',
    'Порог rδ = Δu(α)',
    'Коллапс\n(отклонение выгодно)'
])

plt.xlabel('δ (размер санкции)')
plt.ylabel('r (надёжность санкции)')
plt.title(f'Режимы при α = {alpha:.2f} (вероятность мягкого поведения первого)')
plt.tight_layout()
plt.savefig(f'property_delta_r_alpha_{alpha:.2f}.png', dpi=300)
plt.close()
