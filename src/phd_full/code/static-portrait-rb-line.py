import numpy as np
import matplotlib.pyplot as plt

def delta_u(alpha):
    return -25 + 50*alpha

n_delta = 200
n_r = 200

delta_vals = np.linspace(0, 40, n_delta)
r_vals     = np.linspace(0, 1,  n_r)

alpha = 0.51
Du = delta_u(alpha)

Z = np.zeros((n_r, n_delta))

for i, r in enumerate(r_vals):
    for j, delta in enumerate(delta_vals):
        eff = r * delta
        if Du <= 0:
            Z[i, j] = -1
        else:
            if eff < Du:
                Z[i, j] = 1
            else:
                Z[i, j] = -1

cmap = plt.cm.get_cmap('bwr', 2)  # только синий/красный

plt.figure(figsize=(6, 4))
plt.imshow(
    Z,
    origin='lower',
    aspect='auto',
    extent=[delta_vals[0], delta_vals[-1], r_vals[0], r_vals[-1]],
    cmap=cmap,
    vmin=-1, vmax=1
)

# аналитическая пороговая линия r = Du / delta
if Du > 0:
    delta_line = np.linspace(1e-3, 40, 500)
    r_line = Du / delta_line
    r_line = np.clip(r_line, 0, 1)
    plt.plot(delta_line, r_line, 'k--', linewidth=2, label='rδ = Δu(α)')
    plt.legend(loc='upper right')

plt.xlabel('δ (размер санкции)')
plt.ylabel('r (надёжность санкции)')
plt.title(f'Режимы при α = {alpha:.2f}')
plt.tight_layout()
plt.savefig(f'property_delta_r_alpha_{alpha:.2f}_with_line.png', dpi=300)
plt.close()
