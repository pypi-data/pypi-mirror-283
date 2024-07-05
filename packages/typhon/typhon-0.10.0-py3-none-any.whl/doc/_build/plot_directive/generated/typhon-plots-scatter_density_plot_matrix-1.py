import numpy as np
import matplotlib.pyplot as plt
from typhon.plots import scatter_density_plot_matrix

x = 5*np.random.randn(5000)
y = x + 10*np.random.randn(x.size)
z = y**2 + x**2 + 20*np.random.randn(x.size)

scatter_density_plot_matrix(
    x=x, y=y, z=z,
    hexbin_kw={"mincnt": 1, "cmap": "viridis", "gridsize": 20},
    units=dict(x="romans", y="knights", z="rabbits"))

plt.show()