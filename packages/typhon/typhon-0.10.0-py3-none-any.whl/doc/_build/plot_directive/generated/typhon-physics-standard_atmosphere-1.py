import numpy as np
from typhon.plots import (profile_p_log, profile_z)
from typhon.physics import standard_atmosphere
from typhon.math import nlogspace


z = np.linspace(0, 84e3, 100)
fig, ax = plt.subplots()
profile_z(z, standard_atmosphere(z), ax=ax)

p = nlogspace(1000e2, 0.4, 100)
fig, ax = plt.subplots()
profile_p_log(p, standard_atmosphere(p, coordinates='pressure'))

plt.show()