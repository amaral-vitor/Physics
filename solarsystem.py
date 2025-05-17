# -*- coding: utf-8 -*-
"""
Created on Fri May 16 22:23:08 2025

@author: vamar
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constantes
G = 4 * np.pi ** 2  # constante gravitacional em unidades AU^3 / (ano^2 * Msol)

# Parâmetros dos corpos celestes
class CorpoCeleste:
    def __init__(self, nome, massa, pos, vel, cor, rastro=False):
        self.nome = nome
        self.massa = massa
        self.pos = np.array(pos, dtype='float64')
        self.vel = np.array(vel, dtype='float64')
        self.cor = cor
        self.rastro = rastro
        self.traj = [self.pos.copy()]

# Sol e alguns planetas (simplificados)
corpos = [
    CorpoCeleste("Sol", 1.0, [0, 0], [0, 0], 'yellow'),
    CorpoCeleste("Terra", 3e-6, [1, 0], [0, 2 * np.pi], 'blue', rastro=True),
    CorpoCeleste("Marte", 3.2e-7, [1.52, 0], [0, 2 * np.pi / np.sqrt(1.52)], 'red', rastro=True),
    CorpoCeleste("Vênus", 2.4e-6, [0.72, 0], [0, 2 * np.pi / np.sqrt(0.72)], 'orange', rastro=True),
    CorpoCeleste("Mercúrio", 1.7e-7, [0.39, 0], [0, 2 * np.pi / np.sqrt(0.39)], 'gray', rastro=True),
]

# Parâmetros da simulação
dt = 0.002  # passo de tempo (anos)
n_passos = 3000

# Inicialização da figura
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor("black")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_title("Sistema Solar (simulação gravitacional)", color='white')
ax.tick_params(colors='white')

# Gráficos dos planetas
pontos = []
trilhas = []

for corpo in corpos:
    ponto, = ax.plot([], [], 'o', color=corpo.cor, label=corpo.nome)
    pontos.append(ponto)
    if corpo.rastro:
        trilha, = ax.plot([], [], '-', color=corpo.cor, linewidth=0.5, alpha=0.6)
        trilhas.append(trilha)
    else:
        trilhas.append(None)

ax.legend(loc="upper right", facecolor='black', labelcolor='white')

# Atualização da posição
def update(frame):
    for i, corpo in enumerate(corpos):
        if corpo.nome == "Sol":
            continue  # Sol fixo no centro (massa infinita, simplificação)

        # Força gravitacional do Sol
        dx = corpos[0].pos - corpo.pos
        dist = np.linalg.norm(dx)
        forca = G * corpos[0].massa * corpo.massa / dist**3 * dx

        # Atualizar velocidade e posição (Euler)
        corpo.vel += forca / corpo.massa * dt
        corpo.pos += corpo.vel * dt

        corpo.traj.append(corpo.pos.copy())
        if len(corpo.traj) > 500:
            corpo.traj.pop(0)

    # Atualizar gráfico
    for i, corpo in enumerate(corpos):
        pontos[i].set_data(*corpo.pos)
        if corpo.rastro and trilhas[i]:
            traj = np.array(corpo.traj)
            trilhas[i].set_data(traj[:, 0], traj[:, 1])
    return pontos + [t for t in trilhas if t]

# Animação
ani = FuncAnimation(fig, update, frames=n_passos, interval=10, blit=True)
plt.show()