import pytest

from yt.utilities.answer_testing.answer_tests import (
    field_values,
    pixelized_projection_values,
)


@pytest.mark.answer_test
@pytest.mark.parametrize(
    "dobj_name",
    [None, ("sphere", ("max", (0.1, "unitary")))],
    ids=("entire_domain", "small_sphere"),
)
@pytest.mark.parametrize("axis", [0, 1, 2], ids=["x", "y", "z"])
def test_pixelized_projection(ds, axis, field, dobj_name, weight_field):
    """Test common combination of projection values (answer test)."""
    return pixelized_projection_values(
        ds, axis, field, weight_field=weight_field, dobj_type=dobj_name
    )


@pytest.mark.answer_test
@pytest.mark.parametrize(
    "dobj_name",
    [None, ("sphere", ("max", (0.1, "unitary")))],
    ids=("entire_domain", "small_sphere"),
)
def test_field_values(ds, dobj_name, weight_field, field):
    """Test common combination of field values (answer test)."""
    if weight_field:
        pytest.skip("Duplicate test")
    is_particle_field = field[0] in ds.particle_types
    return field_values(ds, field, obj_type=dobj_name, particle_type=is_particle_field)


def test_basic_attrs(ds, ds_str_repr, nparts):
    assert str(ds) == ds_str_repr
    dd = ds.all_data()
    assert dd["all", "particle_position"].shape == (nparts, 3)
    tot = sum(
        dd[ptype, "particle_position"].shape[0] for ptype in ds.particle_types_raw
    )
    assert tot == nparts
