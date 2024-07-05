import numpy as np
import matplotlib.pyplot as plt
import typhon.plots

z = np.linspace(0, 80e3, 50)
x = np.sin(z / 5e3)

fig, ax = plt.subplots()
typhon.plots.profile_z(z, x, ax=ax)

plt.show()