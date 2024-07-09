"""
Cross-sectional areas of silicon subshells for photon interactions.

Examples
--------

Plot the cross-section areas of each silicon subshell as a function of
photon energy.

.. jupyter-execute::

    import numpy as np
    import matplotlib.pyplot as plt
    import astropy.units as u
    import astropy.visualization
    import fano

    # Define of grid of photon energies to sample
    energy = np.geomspace(1, 10000, num=1001) * u.eV

    # Evaluate the area of each subshell for the given
    # photon energy.
    area_k1 = fano.photons.areas.area_photoionization_k1(energy)
    area_l1 = fano.photons.areas.area_photoionization_l1(energy)
    area_l2 = fano.photons.areas.area_photoionization_l2(energy)
    area_l3 = fano.photons.areas.area_photoionization_l3(energy)
    area_m1 = fano.photons.areas.area_photoionization_m1(energy)
    area_m2 = fano.photons.areas.area_photoionization_m2(energy)
    area_m3 = fano.photons.areas.area_photoionization_m3(energy)
    area = fano.photons.areas.area_photoionization(energy)

    # Plot the areas as a function of photon energy.
    with astropy.visualization.quantity_support():
        fig, ax = plt.subplots()
        ax.loglog(energy, area_k1, label="$K_1$")
        ax.loglog(energy, area_l1, label="$L_1$")
        ax.loglog(energy, area_l2, label="$L_2$")
        ax.loglog(energy, area_l3, label="$L_3$")
        ax.loglog(energy, area_m1, label="$M_1$")
        ax.loglog(energy, area_m2, label="$M_2$")
        ax.loglog(energy, area_m3, label="$M_3$")
        ax.loglog(energy, area, label="total")
        ax.set_xlabel(f"photon energy ({ax.get_xlabel()})")
        ax.set_ylabel(f"cross-sectional aread ({ax.get_ylabel()})")
        ax.legend()
"""

from ._ionization import (
    area_photoionization_k1,
    area_photoionization_l1,
    area_photoionization_l2,
    area_photoionization_l3,
    area_photoionization_m1,
    area_photoionization_m2,
    area_photoionization_m3,
    area_photoionization,
)

__all__ = [
    "area_photoionization_k1",
    "area_photoionization_l1",
    "area_photoionization_l2",
    "area_photoionization_l3",
    "area_photoionization_m1",
    "area_photoionization_m2",
    "area_photoionization_m3",
    "area_photoionization",
]
