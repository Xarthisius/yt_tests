"""Basic test for ART frontend."""
import pytest
from yt.frontends.art.api import ARTDataset
from yt.testing import (
    ParticleSelectionComparison,
    assert_almost_equal,
    assert_equal,
    units_override_check,
)
from yt.units.yt_array import YTQuantity
from yt.utilities.answer_testing.answer_tests import (
    field_values,
    pixelized_projection_values,
)
from yt.utilities.answer_testing.framework import data_dir_load
from yt.utilities.answer_testing.testing_utilities import can_run_ds

_fields = (
    ("gas", "density"),
    ("gas", "temperature"),
    ("all", "particle_mass"),
    ("all", "particle_position_x"),
    ("all", "particle_velocity_y"),
)

_particle_types = (
    "specie0",
    "specie1",
    "specie2",
    "specie3",
    "specie4",
    "all",
    "nbody",
    "darkmatter",
    "stars",
)

d9p = "D9p_500/10MpcBox_HartGal_csf_a0.500.d"
dmonly = "DMonly/PMcrs0.0100.DAT"


def test_d9p(ds):
    """Assert that d9p loads as ARTDataset."""
    assert isinstance(ds, ARTDataset)


@pytest.mark.answer_test
@pytest.mark.parametrize("field", _fields)
@pytest.mark.parametrize("dobj_name", [None, ("sphere", ("max", (0.1, "unitary")))])
def test_field_values(ds, field, dobj_name):
    """Test common combination of field values (answer test)."""
    is_particle_field = field[0] in _particle_types
    return field_values(ds, field, obj_type=dobj_name, particle_type=is_particle_field)


@pytest.mark.answer_test
@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize(
    "field", [field for field in _fields if field[0] not in _particle_types]
)
@pytest.mark.parametrize("dobj_name", [None, ("sphere", ("max", (0.1, "unitary")))])
@pytest.mark.parametrize("weight_field", [None, ("gas", "density")])
def test_pixelized_projection(ds, axis, field, dobj_name, weight_field):
    """Test common combination of projection values (answer test)."""
    return pixelized_projection_values(
        ds, axis, field, weight_field=weight_field, dobj_type=dobj_name
    )


def test_d9p_global_values(ds):
    """Test some global values for the default ART dataset."""
    ad = ds.all_data()
    AnaNStars = 6255
    assert_equal(ad[("stars", "particle_type")].size, AnaNStars)
    assert_equal(ad[("specie4", "particle_type")].size, AnaNStars)

    # The *real* answer is 2833405, but yt misses one particle since it lives
    # on a domain boundary. See issue 814. When that is fixed, this test
    # will need to be updated
    AnaNDM = 2833404
    assert_equal(ad[("darkmatter", "particle_type")].size, AnaNDM)
    assert_equal(
        (
            ad[("specie0", "particle_type")].size
            + ad[("specie1", "particle_type")].size
            + ad[("specie2", "particle_type")].size
            + ad[("specie3", "particle_type")].size
        ),
        AnaNDM,
    )

    for spnum in range(5):
        npart_read = ad[f"specie{spnum}", "particle_type"].size
        npart_header = ds.particle_type_counts[f"specie{spnum}"]
        if spnum == 3:
            # see issue 814
            npart_read += 1
        assert_equal(npart_read, npart_header)

    AnaBoxSize = YTQuantity(7.1442196564, "Mpc")
    AnaVolume = YTQuantity(364.640074656, "Mpc**3")
    Volume = 1
    for i in ds.domain_width.in_units("Mpc"):
        assert_almost_equal(i, AnaBoxSize)
        Volume *= i
    assert_almost_equal(Volume, AnaVolume)

    AnaNCells = 4087490
    assert_equal(len(ad[("index", "cell_volume")]), AnaNCells)

    AnaTotDMMass = YTQuantity(1.01191786808255e14, "Msun")
    assert_almost_equal(
        ad[("darkmatter", "particle_mass")].sum().in_units("Msun"), AnaTotDMMass
    )

    AnaTotStarMass = YTQuantity(1776701.3990607238, "Msun")
    assert_almost_equal(
        ad[("stars", "particle_mass")].sum().in_units("Msun"), AnaTotStarMass
    )

    AnaTotStarMassInitial = YTQuantity(2423468.2801332865, "Msun")
    assert_almost_equal(
        ad[("stars", "particle_mass_initial")].sum().in_units("Msun"),
        AnaTotStarMassInitial,
    )

    AnaTotGasMass = YTQuantity(1.7826982029216785e13, "Msun")
    assert_almost_equal(ad[("gas", "cell_mass")].sum().in_units("Msun"), AnaTotGasMass)

    AnaTotTemp = YTQuantity(150219844793.3907, "K")  # just leaves
    assert_almost_equal(ad[("gas", "temperature")].sum().in_units("K"), AnaTotTemp)


def test_units_override():
    """Test if units can be overridden."""
    units_override_check("D9p_500/10MpcBox_HartGal_csf_a0.500.d")


@pytest.mark.skipif(not can_run_ds(dmonly), reason=f"Dataset {dmonly} not found.")
def test_particle_selection():
    """Test common particle selection schemes."""
    ds = data_dir_load(dmonly)
    psc = ParticleSelectionComparison(ds)
    psc.run_defaults()
