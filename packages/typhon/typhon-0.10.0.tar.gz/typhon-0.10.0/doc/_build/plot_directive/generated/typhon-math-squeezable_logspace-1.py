import itertools

from typhon.plots import profile_p_log
from typhon.math import squeezable_logspace


fixpoints = [0, 0.7]
squeezefacotrs = [0.5, 1.5]
combinations = itertools.product(fixpoints, squeezefacotrs)

fig, axes = plt.subplots(len(fixpoints), len(squeezefacotrs),
                        sharex=True, sharey=True)
for ax, (fp, s) in zip(axes.flat, combinations):
    p = squeezable_logspace(1000e2, 0.01e2, 20,
                            fixpoint=fp, squeeze=s)
    profile_p_log(p, np.ones(p.size),
                marker='.', linestyle='none', ax=ax)
    ax.set_title('fixpoint={}, squeeze={}'.format(fp, s),
                size='x-small')