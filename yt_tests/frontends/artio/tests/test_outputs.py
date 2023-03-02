"""Basic test for ART frontend."""
import pytest

from yt.frontends.artio.api import ARTIODataset
from yt.testing import assert_allclose_units, assert_equal, units_override_check
from yt.utilities.answer_testing.framework import create_obj
from yt_tests.small_patch import SPHSmallPatchTest


class TestARTIOSmallPatch(SPHSmallPatchTest):
    pass


def test_loading(ds):
    """Assert that sizmbhloz loads as ARTIODataset."""
    assert isinstance(ds, ARTIODataset)
    assert_equal(ds.particle_type_counts, {"N-BODY": 100000, "STAR": 110650})


@pytest.mark.parametrize(
    "dobj_name",
    [None, ("sphere", ("max", (0.1, "unitary")))],
    ids=("entire_domain", "small_sphere"),
)
def test_masks(ds, dobj_name):
    """Test some global values for the default ARTIO dataset."""
    dobj = create_obj(ds, dobj_name)
    s1 = dobj[("index", "ones")].sum()
    s2 = sum(mask.sum() for block, mask in dobj.blocks)
    assert_equal(s1, s2)


def test_units_override():
    """Test if units can be overridden."""
    units_override_check("D9p_500/10MpcBox_HartGal_csf_a0.500.d")


def test_particle_derived_field(ds):
    """Test to make sure we get back data in the correct units during field detection."""
    def star_age_alias(field, data):
        """Test field."""
        return data["STAR", "age"].in_units("Myr")

    ds.add_field(
        ("STAR", "new_field"),
        function=star_age_alias,
        units="Myr",
        sampling_type="particle",
    )
    ad = ds.all_data()
    assert_allclose_units(ad["STAR", "age"].in_units("Myr"), ad["STAR", "new_field"])
