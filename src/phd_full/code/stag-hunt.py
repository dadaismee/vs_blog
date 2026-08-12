import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

ASSETS_DIR = "../assets"

# 1) верхний график: Delta u(p) = 2 - 3p
p_vals = np.linspace(0, 1, 400)
Delta_vals = 2 - 3*p_vals
# Delta_vals = 1 - 2*p_vals

plt.figure(figsize=(5, 3))
plt.plot(p_vals, Delta_vals, 'k-', linewidth=2)
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.xlabel('вероятность, что оппонент сыграет S')
plt.ylabel('Δu(p)')
plt.title('Размер выигрыша при отклонении')
plt.tight_layout()
plt.savefig('sh-line.png', dpi=300)
plt.close()

# 2) нижний: 2 панели по (delta, r) для двух p

def delta_u(p):
    return 2 - 3*p
    # return 1 - 2*p

ps = [0.65, 0.5]
labels = ["p = 0.65", "p = 0.5"]

n_delta = 200
n_r = 200

delta_vals = np.linspace(0, 2.0, n_delta)
r_vals     = np.linspace(0, 1.0, n_r)

fig, axes = plt.subplots(1, 2, figsize=(8, 3.5), sharex=True, sharey=True)
axes = axes.ravel()

cmap = ListedColormap([
    [0.7, 0.9, 0.7],  # институт устойчив
    [1.0, 1.0, 1.0],  # порог
    [1.0, 0.75, 0.8], # коллапс
])

for ax, p, lab in zip(axes, ps, labels):
    Du = delta_u(p)
    Z = np.zeros((n_r, n_delta))
    for i, r in enumerate(r_vals):
        for j, delta in enumerate(delta_vals):
            eff = r * delta
            if Du <= 0:
                Z[i, j] = -1
            else:
                if eff < Du - 1e-6:
                    Z[i, j] = 1   # коллапс
                elif eff > Du + 1e-6:
                    Z[i, j] = -1  # институт
                else:
                    Z[i, j] = 0   # порог

    ax.imshow(
        Z,
        origin='lower',
        aspect='auto',
        extent=[delta_vals[0], delta_vals[-1], r_vals[0], r_vals[-1]],
        cmap=cmap,
        vmin=-1, vmax=1
    )

    if Du > 0:
        delta_line = np.linspace(1e-3, 2.0, 500)
        r_line = Du / delta_line
        r_line = np.clip(r_line, 0, 1)
        ax.plot(delta_line, r_line, color='k', linestyle='--', linewidth=1)

    ax.set_title(lab, fontsize=10)

fig.text(0.5, 0.03, 'δ (размер санкции)', ha='center')
fig.text(0.03, 0.5, 'r (надёжность санкции)', va='center', rotation='vertical')

legend_elements = [
    Patch(facecolor=[0.7, 0.9, 0.7], label='Институт устойчив (rδ ≥ Δu(p))'),
    Patch(facecolor=[1.0, 1.0, 1.0], edgecolor='black', label='Порог rδ = Δu(p)'),
    Patch(facecolor=[1.0, 0.75, 0.8], label='Коллапс (rδ < Δu(p))'),
]
fig.legend(
    handles=legend_elements,
    loc='upper center',
    bbox_to_anchor=(0.5, 0.98),
    ncol=3,
    fontsize=8
)

plt.tight_layout(rect=(0.06, 0.06, 0.94, 0.9))
plt.savefig('stag_hunt.png', dpi=300)
plt.close()

'created stag_hunt_delta_u_of_p_final.png and stag_hunt_delta_r_2panels_soft_final.png'
