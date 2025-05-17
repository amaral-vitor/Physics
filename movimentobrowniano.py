# -*- coding: utf-8 -*-
"""
Created on Fri May 16 22:09:37 2025

@author: vamar
"""

# !pip install matplotlib numpy

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Número de passos e tamanho do passo
n_passos = 200
delta = 0.1  # Tamanho do passo

# Gera posições acumuladas aleatórias para x e y
x = np.cumsum(np.random.randn(n_passos) * delta)
y = np.cumsum(np.random.randn(n_passos) * delta)

# Cria a figura
fig, ax = plt.subplots()
linha, = ax.plot([], [], lw=2)
particula, = ax.plot([], [], 'ro')  # ponto vermelho

# Define os limites do gráfico
ax.set_xlim(np.min(x) - 1, np.max(x) + 1)
ax.set_ylim(np.min(y) - 1, np.max(y) + 1)
ax.set_title("Movimento Browniano")

# Inicialização da linha e partícula
def init():
    linha.set_data([], [])
    particula.set_data([], [])
    return linha, particula

# Função de animação
def animate(i):
    linha.set_data(x[:i], y[:i])
    particula.set_data(x[i-1], y[i-1])
    return linha, particula

# Cria a animação
ani = animation.FuncAnimation(fig, animate, frames=n_passos, init_func=init,
                              interval=50, blit=True, repeat=False)

plt.show()
