import numpy as np

from yt.testing import (
    assert_allclose_units,
    assert_equal,
    disable_dataset_cache,
)
from yt.frontends.athena.api import AthenaDataset
from yt_tests.small_patch import SmallPatchTest


class TestAthenaSmallPatch(SmallPatchTest):
    pass


def test_blast_override(blast_uo):
    # verify that overriding units causes derived unit values to be updated.
    # see issue #1259
    ds = blast_uo
    assert_equal(float(ds.magnetic_unit.in_units("gauss")), 5.47867467969813e-07)


@disable_dataset_cache
def test_nprocs(sloshing_uo, sloshing_uo_np8):
    ds1 = sloshing_uo
    ds2 = sloshing_uo_np8
    sp1 = ds1.sphere("c", (100.0, "kpc"))
    prj1 = ds1.proj(("gas", "density"), 0)
    sp2 = ds2.sphere("c", (100.0, "kpc"))
    prj2 = ds2.proj(("gas", "density"), 0)

    assert_equal(
        sp1.quantities.extrema(("gas", "pressure")),
        sp2.quantities.extrema(("gas", "pressure")),
    )
    assert_allclose_units(
        sp1.quantities.total_quantity(("gas", "pressure")),
        sp2.quantities.total_quantity(("gas", "pressure")),
    )
    for ax in "xyz":
        assert_equal(
            sp1.quantities.extrema(("gas", f"velocity_{ax}")),
            sp2.quantities.extrema(("gas", f"velocity_{ax}")),
        )
    assert_allclose_units(
        sp1.quantities.bulk_velocity(), sp2.quantities.bulk_velocity()
    )
    assert_equal(prj1[("gas", "density")], prj2[("gas", "density")])


def test_AthenaDataset(cloud):
    assert isinstance(cloud, AthenaDataset)


@disable_dataset_cache
def test_mag_factor(sloshing_uo, sloshing_uo_lorentz):
    ds1 = sloshing_uo
    ds2 = sloshing_uo_lorentz

    assert ds1.magnetic_unit == np.sqrt(
        4.0 * np.pi * ds1.mass_unit / (ds1.time_unit**2 * ds1.length_unit)
    )
    sp1 = ds1.sphere("c", (100.0, "kpc"))
    pB1a = (
        sp1["athena", "cell_centered_B_x"] ** 2
        + sp1["athena", "cell_centered_B_y"] ** 2
        + sp1["athena", "cell_centered_B_z"] ** 2
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
        sp2["athena", "cell_centered_B_x"] ** 2
        + sp2["athena", "cell_centered_B_y"] ** 2
        + sp2["athena", "cell_centered_B_z"] ** 2
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
