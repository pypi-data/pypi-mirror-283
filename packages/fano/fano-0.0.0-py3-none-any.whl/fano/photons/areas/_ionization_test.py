from typing import Callable
import pytest
import numpy as np
import astropy.units as u
import fano

_energy = [
    2000 * u.eV,
    np.linspace(5, 2000, num=11) * u.eV,
    np.linspace(1, 1000, num=12) * u.nm,
]


@pytest.mark.parametrize(
    argnames="func",
    argvalues=[
        fano.photons.areas.area_photoionization_k1,
        fano.photons.areas.area_photoionization_l1,
        fano.photons.areas.area_photoionization_l2,
        fano.photons.areas.area_photoionization_l3,
        fano.photons.areas.area_photoionization_m1,
        fano.photons.areas.area_photoionization_m2,
        fano.photons.areas.area_photoionization_m3,
        fano.photons.areas.area_photoionization,
    ],
)
@pytest.mark.parametrize("energy", _energy)
def test_area_photoionization(func: Callable, energy: u.Quantity):
    result = func(energy)
    assert np.all(result >= 0)
    assert result.unit.is_equivalent(u.barn)
