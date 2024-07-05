import numpy as np
import matplotlib.pyplot as plt
from typhon import physics

T = np.linspace(245, 285)
fig, ax = plt.subplots()
ax.semilogy(T, physics.e_eq_mixed_mk(T), lw=3, c='k', label='Mixed')
ax.semilogy(T, physics.e_eq_ice_mk(T), ls='dashed', label='Ice')
ax.semilogy(T, physics.e_eq_water_mk(T), ls='dashed', label='Water')
ax.set_ylabel('Vapor pressure [Pa]')
ax.set_xlabel('Temperature [K]')
ax.legend()

plt.show()