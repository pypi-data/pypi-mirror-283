import numpy as np
import matplotlib.pyplot as plt
from typhon.plots import center_colorbar


fig, ax = plt.subplots()
sm = ax.pcolormesh(np.random.randn(10, 10) + 0.75, cmap='difference')
cb = fig.colorbar(sm)
center_colorbar(cb)

plt.show()