import numpy as np

from yt.units import dimensions
from yt.testing import (
    assert_allclose_units,
    assert_equal,
    disable_dataset_cache,
    units_override_check,
)
from yt.frontends.athena_pp.api import AthenaPPDataset
from yt_tests.small_patch import SmallPatchTest


class TestAthenaPPSmallPatch(SmallPatchTest):
    pass


def test_AM06_override(AM06_uo):
    ds = AM06_uo
    assert_equal(float(ds.magnetic_unit.in_units("gauss")), 9.01735778342523e-08)


def test_AthenaDataset(AM06):
    assert isinstance(AM06, AthenaPPDataset)


def test_magnetic_units(AM06_code):
    ds = AM06_code
    assert ds.magnetic_unit.units.dimensions == dimensions.magnetic_field_cgs
    assert (ds.magnetic_unit**2).units.dimensions == dimensions.pressure


@disable_dataset_cache
def test_mag_factor(AM06_uo, AM06_uo_lorentz):
    ds1 = AM06_uo
    ds2 = AM06_uo_lorentz

    assert ds1.magnetic_unit == np.sqrt(
        4.0 * np.pi * ds1.mass_unit / (ds1.time_unit**2 * ds1.length_unit)
    )
    sp1 = ds1.sphere("c", (100.0, "kpc"))
    pB1a = (
        sp1["athena_pp", "Bcc1"] ** 2
        + sp1["athena_pp", "Bcc2"] ** 2
        + sp1["athena_pp", "Bcc3"] ** 2
    ) / (8.0 * np.pi)
    pB1b = (
        sp1["gas", "magnetic_field_x"] ** 2
        + sp1["gas", "magnetic_field_y"] ** 2
        + sp1["gas", "magnetic_field_z"] ** 2
    ) / (8.0 * np.pi)
    pB1a.convert_to_units("dyn/cm**2")
    pB1b.convert_to_units("dyn/cm**2")
    assert_allclose_units(pB1a, pB1b)
    assert_allclose_units(pB1a, sp1["magnetic_pressure"])

    assert ds2.magnetic_unit == np.sqrt(
        ds2.mass_unit / (ds2.time_unit**2 * ds2.length_unit)
    )
    sp2 = ds2.sphere("c", (100.0, "kpc"))
    pB2a = (
        sp2["athena_pp", "Bcc1"] ** 2
        + sp2["athena_pp", "Bcc2"] ** 2
        + sp2["athena_pp", "Bcc3"] ** 2
    ) / 2.0
    pB2b = (
        sp2["gas", "magnetic_field_x"] ** 2
        + sp2["gas", "magnetic_field_y"] ** 2
        + sp2["gas", "magnetic_field_z"] ** 2
    ) / 2.0
    pB2a.convert_to_units("dyn/cm**2")
    pB2b.convert_to_units("dyn/cm**2")
    assert_allclose_units(pB2a, pB2b)
    assert_allclose_units(pB2a, sp2["magnetic_pressure"])
    assert_allclose_units(pB1a, pB2a)


def test_units_override(AM06):
    units_override_check("AM06/AM06.out1.00400.athdf")
