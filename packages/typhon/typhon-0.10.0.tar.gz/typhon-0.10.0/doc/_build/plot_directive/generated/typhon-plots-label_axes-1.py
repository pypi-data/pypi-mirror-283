import matplotlib.pyplot as plt
from typhon.plots import label_axes, styles


plt.style.use(styles('typhon'))

# Automatic labeling of axes.
fig, axes = plt.subplots(ncols=2, nrows=2)
label_axes()

# Manually specify the axes to label.
fig, axes = plt.subplots(ncols=2, nrows=2)
label_axes(axes[:, 0])  # label each row.

# Pass explicit labels (and additional arguments).
fig, axes = plt.subplots(ncols=2, nrows=2)
label_axes(labels=map(str, range(axes.size)), weight='bold')