import numpy as np
import matplotlib.pyplot as plt

from typhon.plots import colored_bars


N = 50
x = np.arange(N)
y = np.sin(np.linspace(0, 3 * np.pi, N)) + 0.5 * np.random.randn(N)

# Basic series with bars colored according to y-value.
fig, ax = plt.subplots()
colored_bars(x, y, cmap='seismic')

# Add a colorbar to the figure.
fig, ax = plt.subplots()
sm, bars = colored_bars(x, y, cmap='seismic')
cb = fig.colorbar(sm, ax=ax)

# Pass different values for coloring (here, x-values).
fig, ax = plt.subplots()
colored_bars(x, y, c=x)

plt.show()