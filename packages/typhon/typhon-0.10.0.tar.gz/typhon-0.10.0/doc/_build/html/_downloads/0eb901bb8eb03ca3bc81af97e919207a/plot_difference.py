# -*- coding: utf-8 -*-

"""Plot to demonstrate the difference colormap.
"""

import numpy as np
import matplotlib.pyplot as plt

from typhon.plots import (figsize, cmap2rgba)


x = np.linspace(0, 2 * np.pi, 500)
y = np.linspace(0, -1, 500)[:, np.newaxis]
z = np.sin(x**2) * np.exp(y)

fig, ax = plt.subplots(figsize=figsize(10))
ax.set_prop_cycle(color=cmap2rgba('qualitative1', 7))
sm = ax.pcolormesh(x, y, z, cmap='difference', rasterized=True)
fig.colorbar(sm)

fig.tight_layout()
plt.show()
