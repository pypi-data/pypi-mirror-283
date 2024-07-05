import matplotlib.pyplot as plt
import numpy as np
from typhon.plots import supcolorbar


fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
for ax in axes.flat:
    sm = ax.pcolormesh(np.random.random((10,10)), vmin=0, vmax=1)

supcolorbar(sm, label='Test label')