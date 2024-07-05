import numpy as np
import matplotlib.pyplot as plt
import typhon
from typhon.plots import (set_yaxis_formatter, HectoPascalFormatter)


p = typhon.math.nlogspace(1000e2, 0.1e2, 50)

fig, ax = plt.subplots()
ax.plot(np.exp(p / p[0]), p)
ax.invert_yaxis()
set_yaxis_formatter(HectoPascalFormatter())

plt.show()