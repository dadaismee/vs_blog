# Colab link — https://colab.research.google.com/drive/1IqXGnv_ZulVffliy3gf7RQgL1ADblWPx?usp=sharing
# ------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict, Counter

random.seed(43)

# --- Agent Definitions ---

class Agent:
    def __init__(self, alpha=0.1, q=None):
        self.alpha = alpha
        self.q = q if q is not None else defaultdict(lambda: {'Hawk': 1.0, 'Dove': 1.0})

    def perceive(self, true_role, translucency):
        if random.random() < translucency:
            return 'intruder' if true_role == 'owner' else 'owner'
        return true_role

    def choose_action(self, cue):
        ct = self.cognitive_type()
        if ct == 'Detection' and isinstance(cue, str):
            pass
        elif ct == 'Robust' and isinstance(cue, tuple) and len(cue) == 2:
            pass
        elif ct == 'Decoupled' and isinstance(cue, tuple) and cue[0] == 'context':
            pass

        if cue not in self.q:
            self.q[cue] = {'Hawk': 1.0, 'Dove': 1.0}
        probs = self.get_action_probs(cue)
        return np.random.choice(['Hawk', 'Dove'], p=[probs['Hawk'], probs['Dove']])

    def get_action_probs(self, cue):
        q_vals = self.q[cue]
        total = q_vals['Hawk'] + q_vals['Dove']
        return {a: q_vals[a] / total for a in ['Hawk', 'Dove']}

    def learn(self, cue, action, reward):
        self.q[cue][action] += self.alpha * (reward - self.q[cue][action])

    def cognitive_type(self):
        cues_used = set(self.q.keys())
        if any(isinstance(c, tuple) and c[0] == 'context' for c in cues_used):
            return 'Decoupled'
        elif any(isinstance(c, tuple) and len(c) == 2 for c in cues_used):
            return 'Robust'
        return 'Detection'

# --- Payoffs ---

def get_payoff(role1, a1, role2, a2):
    if role1 == 'owner' and a1 == 'Hawk' and role2 == 'intruder' and a2 == 'Dove': return 1.5, 1.5
    if role1 == 'intruder' and a1 == 'Dove' and role2 == 'owner' and a2 == 'Hawk': return 1.5, 1.5
    if a1 == 'Hawk' and a2 == 'Dove': return 2, 1
    if a1 == 'Dove' and a2 == 'Hawk': return 1, 2
    if a1 == 'Hawk' and a2 == 'Hawk': return 0, 0
    if a1 == 'Dove' and a2 == 'Dove': return 1, 1

# --- Simulation ---

N = 100
G = 100
pop = [Agent() for _ in range(N)]

salient_use = []
translucency_log = []
coord_success_log = []
cog_type_log = []

for gen in range(G):
    rewards = np.zeros(N)
    successful_coordination = 0
    s_use = 0

    if gen == 0:
        base_translucency = 0.5
    else:
        base_translucency = 0.5 + gen * 0.001 - coord_success_log[-1]

    pop_behavior = {'owner': [], 'intruder': []}

    for i in range(N):
        j = random.choice([x for x in range(N) if x != i])
        role_i, role_j = ('owner', 'intruder') if random.random() < 0.5 else ('intruder', 'owner')

        cue_i = pop[i].perceive(role_i, base_translucency)
        cue_j = pop[j].perceive(role_j, base_translucency)

        def encode_cue(agent, role, cue, freq):
            total = sum(freq.values())
            if total > 10:
                dominant, count = freq.most_common(1)[0]
                ratio = count / total
                if agent.cognitive_type() == 'Detection' and ratio > 0.6:
                    return (cue, dominant), True
                elif agent.cognitive_type() == 'Robust' and ratio > 0.75:
                    return ('context', cue, dominant), True
            return cue, False

        freq_i = Counter(pop_behavior[role_i])
        freq_j = Counter(pop_behavior[role_j])

        cue_i, si = encode_cue(pop[i], role_i, cue_i, freq_i)
        cue_j, sj = encode_cue(pop[j], role_j, cue_j, freq_j)

        s_use += int(si) + int(sj)

        a_i = pop[i].choose_action(cue_i)
        a_j = pop[j].choose_action(cue_j)

        r_i, r_j = get_payoff(role_i, a_i, role_j, a_j)
        pop[i].learn(cue_i, a_i, r_i)
        pop[j].learn(cue_j, a_j, r_j)

        pop_behavior[role_i].append(a_i)
        pop_behavior[role_j].append(a_j)

        rewards[i] += r_i
        rewards[j] += r_j

        if (role_i == 'owner' and a_i == 'Hawk' and role_j == 'intruder' and a_j == 'Dove') or \
           (role_j == 'owner' and a_j == 'Hawk' and role_i == 'intruder' and a_i == 'Dove'):
            successful_coordination += 1

    salient_use.append(s_use / N)
    translucency_log.append(base_translucency)
    coord_success_log.append(successful_coordination / N)

    type_counts = Counter([a.cognitive_type() for a in pop])
    cog_type_log.append(type_counts)

    if gen == 0:
        continue

    fitness = rewards / rewards.sum()
    new_pop = [pop[np.random.choice(range(N), p=fitness)] for _ in range(N)]
    pop = [Agent(alpha=a.alpha, q=a.q.copy()) for a in new_pop]

# --- Visualization ---

generations = range(G)

plt.figure(figsize=(12, 8))

# Cue usage and dynamics
plt.subplot(2, 2, 1)
plt.plot(generations, salient_use, label='Structured Cue Use', color='orange')
plt.plot(generations, coord_success_log, label='Coordination Success', color='green')
plt.plot(generations, translucency_log, label='Translucency', color='blue')
plt.title('Cue Use, Coordination, and Translucency')
plt.xlabel('Generation')
plt.legend()

# Agent Type Composition
plt.subplot(2, 2, 2)
detection = [log.get('Detection', 0) for log in cog_type_log]
robust = [log.get('Robust', 0) for log in cog_type_log]
decoupled = [log.get('Decoupled', 0) for log in cog_type_log]
plt.stackplot(generations, detection, robust, decoupled,
              labels=['Detection', 'Robust', 'Decoupled'],
              colors=['#bbbbff', '#88dd88', '#ffaa88'])
plt.title("Cognitive Type Composition")
plt.xlabel("Generation")
plt.legend(loc='upper right')
plt.grid(True)

# Cue Type Transition with Translucency and Coord overlay
plt.subplot(2, 1, 2)
total_agents = [sum(log.values()) for log in cog_type_log]
ontic_prop = [log.get('Detection', 0) / t for log, t in zip(cog_type_log, total_agents)]
salient_prop = [log.get('Robust', 0) / t for log, t in zip(cog_type_log, total_agents)]
context_prop = [log.get('Decoupled', 0) / t for log, t in zip(cog_type_log, total_agents)]
plt.stackplot(generations, ontic_prop, salient_prop, context_prop,
              labels=['Ontic (Flat)', 'Salient (Role+Action)', 'context (Integrated)'],
              colors=['#aaaaff', '#aaffaa', '#ffccaa'])
plt.plot(generations, translucency_log, label='Translucency', color='blue', linestyle='--')
plt.plot(generations, coord_success_log, label='Coord. Success', color='green', linestyle='--')
plt.title('Cue Type Transition & Selection Pressures')
plt.xlabel('Generation')
plt.ylabel('Proportion / Pressure')
plt.legend(loc='upper left')
plt.grid(True)

plt.tight_layout()
plt.show()
