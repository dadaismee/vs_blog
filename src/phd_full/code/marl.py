import numpy as np
import random
import matplotlib.pyplot as plt

V = 50
BASE_B = 0.5 * V
BASE_L = 0.75 * V

alpha = 0.1
gamma = 0.95
epsilon = 0.1

n_episodes = 50000

def run_experiment(delta, reward_sanction_punish=0.0, track=False):
    Q_beh = np.zeros(2)
    Q_san = np.zeros((2,2))
    history_beh_action = []
    history_sanction_L = []
    for ep in range(n_episodes):
        # choose behaviour action
        if random.random() < epsilon:
            a_beh = random.randint(0,1)
        else:
            a_beh = int(np.argmax(Q_beh))
        # sanctioner's state
        s_san = a_beh
        # choose sanction action
        if random.random() < epsilon:
            a_san = random.randint(0,1)
        else:
            a_san = int(np.argmax(Q_san[s_san]))
        # payoffs
        if a_beh == 0:  # B
            r_beh = BASE_B
            r_san = 0.0
        else:          # L
            r_beh = BASE_L
            if a_san == 1:
                r_beh -= delta
                r_san = reward_sanction_punish
            else:
                r_san = 0.0
        # Q update behaviour
        best_next_beh = np.max(Q_beh)
        td_target_beh = r_beh + gamma * best_next_beh
        td_error_beh = td_target_beh - Q_beh[a_beh]
        Q_beh[a_beh] += alpha * td_error_beh
        # Q update sanctioner
        best_next_san = np.max(Q_san[s_san])
        td_target_san = r_san + gamma * best_next_san
        td_error_san = td_target_san - Q_san[s_san, a_san]
        Q_san[s_san, a_san] += alpha * td_error_san

        if track:
            history_beh_action.append(a_beh)
            if a_beh == 1:
                history_sanction_L.append(a_san)
            else:
                history_sanction_L.append(None)

    # final greedy policies
    a_beh_star = int(np.argmax(Q_beh))
    # estimate r: Pr(E=1 | L) under greedy policy
    count_L = 0
    count_E1 = 0
    for _ in range(10000):
        a_beh = a_beh_star
        if a_beh == 1:
            count_L += 1
            s_san = 1
            a_san = int(np.argmax(Q_san[s_san]))
            if a_san == 1:
                count_E1 += 1
    r_est = count_E1 / count_L if count_L > 0 else 0.0

    if track:
        return Q_beh, Q_san, a_beh_star, r_est, history_beh_action, history_sanction_L
    else:
        return Q_beh, Q_san, a_beh_star, r_est

# пример: delta = 20, санкционер получает delta за наказание
Qb, Qs, a_star, r_est, h_beh, h_sanL = run_experiment(
    20.0,
    reward_sanction_punish=20.0,
    track=True
)

# скользящие средние
window = 500
beh_B_freq = []
sanction_rate_L = []
for i in range(0, len(h_beh), window):
    chunk_beh = h_beh[i:i+window]
    if not chunk_beh:
        break
    beh_B_freq.append(1 - np.mean(chunk_beh))  # 0=B,1=L
    chunk_san = h_sanL[i:i+window]
    L_events = [a for a in chunk_san if a is not None]
    if len(L_events) == 0:
        sanction_rate_L.append(0.0)
    else:
        sanction_rate_L.append(np.mean(L_events))

episodes_axis = np.arange(len(beh_B_freq)) * window

plt.figure(figsize=(7, 4))
plt.plot(episodes_axis, beh_B_freq, label="freq(B) moving avg", color="green")
plt.plot(episodes_axis, sanction_rate_L, label="Pr(punish | L) moving avg", color="red")
plt.xlabel("episode")
plt.ylabel("moving average")
plt.ylim(0, 1)
plt.title("Learning dynamics (δ = 20, sanctioner rewarded)")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("MARL_learning_dynamics_delta20.png", dpi=300)
plt.close()
