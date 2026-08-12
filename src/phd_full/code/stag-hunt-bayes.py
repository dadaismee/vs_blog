import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

# Параметры игры «охота на оленя»
def delta_u(p):  # структурная премия за отклонение Δu(p) = 2 - 3p
    return 1 - 2*p

p = 0.25  # уровень координации (вероятность, что оппонент играет S)
Du = delta_u(p)  # Δu(p)
alpha = 0.5  # субъективная доля от объективного r: r̃ = α r

# Сетка по δ и r
n_delta = 200
n_r = 200
delta_vals = np.linspace(0, 2.0, n_delta)
r_vals = np.linspace(0, 1.0, n_r)

# Карта областей по объективному условию rδ ≥ Δu(p)
Z = np.zeros((n_r, n_delta))
for i, r in enumerate(r_vals):
    for j, delta in enumerate(delta_vals):
        eff = r * delta
        if Du <= 0:
            Z[i, j] = -1  # конвенция: премии за отклонение нет даже без санкций
        else:
            if eff < Du - 1e-6:
                Z[i, j] = 1  # объективный коллапс (rδ < Δu)
            elif eff > Du + 1e-6:
                Z[i, j] = -1  # объективно устойчивый институт
            else:
                Z[i, j] = 0  # объективный порог

cmap = ListedColormap([
    [0.7, 0.9, 0.7],  # институт устойчив (rδ ≥ Δu)
    [1.0, 1.0, 1.0],  # порог
    [1.0, 0.75, 0.8],  # коллапс (rδ < Δu)
])

fig, ax = plt.subplots(figsize=(6, 5))
im = ax.imshow(
    Z,
    origin='lower',
    aspect='auto',
    extent=[delta_vals[0], delta_vals[-1], r_vals[0], r_vals[-1]],
    cmap=cmap,
    vmin=-1,
    vmax=1
)

# Объективный порог: rδ = Δu(p)
if Du > 0:
    delta_line = np.linspace(1e-3, 2.0, 500)
    r_line_obj = Du / delta_line
    r_line_obj = np.clip(r_line_obj, 0, 1)
    line_obj = ax.plot(delta_line, r_line_obj, color='k', linestyle='--', linewidth=2, label='Объективный порог rδ = Δu(p)')[0]

    # Субъективный порог: r̃δ = Δu(p), при r̃ = α r ⇒ r = Δu(p)/(α δ)
    r_line_subj = Du / (alpha * delta_line)
    r_line_subj = np.clip(r_line_subj, 0, 1)
    line_subj = ax.plot(delta_line, r_line_subj, color='blue', linestyle=':', linewidth=2, label='Субъективный порог r̃δ = Δu(p)')[0]

    # Заштриховка области между черной и синей линиями (субъективная устойчивость)
    ax.fill_between(delta_line, r_line_subj, r_line_obj, where=(r_line_subj < r_line_obj), color='yellow', alpha=0.4, label='Субъективная устойчивость')

ax.set_xlabel('δ (размер санкции)', fontsize=12)
ax.set_ylabel('r (объективная надёжность санкции)', fontsize=12)
ax.set_title(f'Ястреб-Голубь при p = {p:.2f}, r̃ = α r, α = {alpha}', fontsize=14)

# Легенда для областей
legend_patches = [
    Patch(facecolor=[0.7, 0.9, 0.7], label='Объективно устойчив (rδ ≥ Δu(p))'),
    Patch(facecolor=[1.0, 0.75, 0.8], label='Объективный коллапс (rδ < Δu(p))'),
]
leg1 = ax.legend(handles=legend_patches, loc='lower left', fontsize=10)

# Легенда для линий и заштриховки
handles2 = [Patch(facecolor='yellow', alpha=0.4, label='Субъективная устойчивость'), line_obj, line_subj]
leg2 = ax.legend(handles=handles2, loc='upper right', fontsize=10)

ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('protoinstitute.png', dpi=300, bbox_inches='tight')
plt.close()
