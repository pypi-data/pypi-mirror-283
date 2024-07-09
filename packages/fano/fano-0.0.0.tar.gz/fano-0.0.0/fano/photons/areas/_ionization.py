import pathlib
import numpy as np
import numba
import astropy.units as u
import endf

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

_path_epdl = pathlib.Path(__file__).parent / "epdl-silicon.endf"

_mf = 23

_mt_k1 = 534
_mt_l1 = 535
_mt_l2 = 536
_mt_l3 = 537
_mt_m1 = 538
_mt_m2 = 539
_mt_m3 = 540

_mat = endf.Material(_path_epdl)

_xs_k1 = _mat.section_data[_mf, _mt_k1]["sigma"]
_xs_l1 = _mat.section_data[_mf, _mt_l1]["sigma"]
_xs_l2 = _mat.section_data[_mf, _mt_l2]["sigma"]
_xs_l3 = _mat.section_data[_mf, _mt_l3]["sigma"]
_xs_m1 = _mat.section_data[_mf, _mt_m1]["sigma"]
_xs_m2 = _mat.section_data[_mf, _mt_m2]["sigma"]
_xs_m3 = _mat.section_data[_mf, _mt_m3]["sigma"]

_energy_k1 = _xs_k1.x
_energy_l1 = _xs_l1.x
_energy_l2 = _xs_l2.x
_energy_l3 = _xs_l3.x
_energy_m1 = _xs_m1.x
_energy_m2 = _xs_m2.x
_energy_m3 = _xs_m3.x

_area_k1 = _xs_k1.y
_area_l1 = _xs_l1.y
_area_l2 = _xs_l2.y
_area_l3 = _xs_l3.y
_area_m1 = _xs_m1.y
_area_m2 = _xs_m2.y
_area_m3 = _xs_m3.y

_unit_energy = u.eV
_unit_area = u.barn

_energy = [
    [_energy_k1],
    [_energy_l1, _energy_l2, _energy_l3],
    [_energy_m1, _energy_m2, _energy_m3],
]

_area = [
    [_area_k1],
    [_area_l1, _area_l2, _area_l3],
    [_area_m1, _area_m2, _area_m3],
]


def area_photoionization_k1(energy: u.Quantity) -> u.Quantity:
    """
    Calculate the cross-section area of the :math:`K_1` shell for a photon of a
    given energy.

    Parameters
    ----------
    energy
        The energy of the incident photon
    """
    energy = energy.to_value(_unit_energy, equivalencies=u.spectral())
    result = _area_photoionization_k1(energy) << _unit_area
    return result


@numba.njit
def _area_photoionization_k1(energy: np.ndarray) -> np.ndarray:
    return np.interp(energy, _energy_k1, _area_k1)


def area_photoionization_l1(energy: u.Quantity) -> u.Quantity:
    """
    Calculate the photoionization cross-sectional area of the :math:`L_1` subshell.

    Parameters
    ----------
    energy
        The energy of the incident photon
    """
    energy = energy.to_value(_unit_energy, equivalencies=u.spectral())
    result = _area_photoionization_l1(energy) << _unit_area
    return result


@numba.njit
def _area_photoionization_l1(energy: np.ndarray) -> np.ndarray:
    return np.interp(energy, _energy_l1, _area_l1)


def area_photoionization_l2(energy: u.Quantity) -> u.Quantity:
    """
    Calculate the photoionization cross-sectional area of the :math:`L_2` subshell.

    Parameters
    ----------
    energy
        The energy of the incident photon
    """
    energy = energy.to_value(_unit_energy, equivalencies=u.spectral())
    result = _area_photoionization_l2(energy) << _unit_area
    return result


@numba.njit
def _area_photoionization_l2(energy: np.ndarray) -> np.ndarray:
    return np.interp(energy, _energy_l2, _area_l2)


def area_photoionization_l3(energy: u.Quantity) -> u.Quantity:
    """
    Calculate the photoionization cross-sectional area of the :math:`L_3` subshell.

    Parameters
    ----------
    energy
        The energy of the incident photon
    """
    energy = energy.to_value(_unit_energy, equivalencies=u.spectral())
    result = _area_photoionization_l3(energy) << _unit_area
    return result


@numba.njit
def _area_photoionization_l3(energy: np.ndarray) -> np.ndarray:
    return np.interp(energy, _energy_l3, _area_l3)


def area_photoionization_m1(energy: u.Quantity) -> u.Quantity:
    """
    Calculate the photoionization cross-sectional area of the :math:`M_1` subshell.

    Parameters
    ----------
    energy
        The energy of the incident photon
    """
    energy = energy.to_value(_unit_energy, equivalencies=u.spectral())
    result = _area_photoionization_m1(energy) << _unit_area
    return result


@numba.njit
def _area_photoionization_m1(energy: np.ndarray) -> np.ndarray:
    return np.interp(energy, _energy_m1, _area_m1)


def area_photoionization_m2(energy: u.Quantity) -> u.Quantity:
    """
    Calculate the photoionization cross-sectional area of the :math:`M_2` subshell.

    Parameters
    ----------
    energy
        The energy of the incident photon
    """
    energy = energy.to_value(_unit_energy, equivalencies=u.spectral())
    result = _area_photoionization_m2(energy) << _unit_area
    return result


@numba.njit
def _area_photoionization_m2(energy: np.ndarray) -> np.ndarray:
    return np.interp(energy, _energy_m2, _area_m2)


def area_photoionization_m3(energy: u.Quantity) -> u.Quantity:
    """
    Calculate the photoionization cross-sectional area of the :math:`M_3` subshell.

    Parameters
    ----------
    energy
        The energy of the incident photon
    """
    energy = energy.to_value(_unit_energy, equivalencies=u.spectral())
    result = _area_photoionization_m3(energy) << _unit_area
    return result


@numba.njit
def _area_photoionization_m3(energy: np.ndarray) -> np.ndarray:
    return np.interp(energy, _energy_m3, _area_m3)


def area_photoionization(energy: u.Quantity) -> u.Quantity:
    """
    Calculate the total photoionization cross-sectional area of silicon.

    Parameters
    ----------
    energy
        The energy of the incident photon
    """
    energy = energy.to_value(_unit_energy, equivalencies=u.spectral())
    result = _area_photoionization(energy) << _unit_area
    return result


@numba.njit
def _area_photoionization(energy: np.ndarray) -> np.ndarray:
    a_k1 = _area_photoionization_k1(energy)
    a_l1 = _area_photoionization_l1(energy)
    a_l2 = _area_photoionization_l2(energy)
    a_l3 = _area_photoionization_l3(energy)
    a_m1 = _area_photoionization_m1(energy)
    a_m2 = _area_photoionization_m2(energy)
    a_m3 = _area_photoionization_m3(energy)
    return a_k1 + a_l1 + a_l2 + a_l3 + a_m1 + a_m2 + a_m3
