import numpy as np
import matplotlib.pyplot as plt
from typhon.plots import heatmap


x = np.random.randn(500)
y = x + np.random.randn(x.size)

fig, ax = plt.subplots()
heatmap(x, y, ax=ax)

plt.show()