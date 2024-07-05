import numpy as np
import matplotlib.pyplot as plt
import typhon.plots

p = typhon.math.nlogspace(1000e2, 0.1e2, 50)
x = np.exp(p / p[0])

fig, ax = plt.subplots()
typhon.plots.profile_p_log(p, x, ax=ax)

plt.show()