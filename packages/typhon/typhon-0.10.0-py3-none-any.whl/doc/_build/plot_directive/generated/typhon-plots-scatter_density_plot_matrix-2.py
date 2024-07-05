import numpy as np
import matplotlib.pyplot as plt
from typhon.plots import scatter_density_plot_matrix

M = np.zeros(shape=(10000,),
             dtype="f,f,f,f")
M["f0"] = np.random.randn(M.size)
M["f1"] = np.random.randn(M.size) + M["f0"]
M["f2"] = 2*np.random.randn(M.size) + M["f0"]*M["f1"]
M["f3"] = M["f0"] + M["f1"] + M["f2"] + 0.5*np.random.randn(M.size)

scatter_density_plot_matrix(M,
    hexbin_kw={"mincnt": 1, "cmap": "viridis", "gridsize": 20})

plt.show()