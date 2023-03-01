import pytest
from yt.utilities.answer_testing.answer_tests import (
    field_values,
    grid_hierarchy,
    grid_values,
    parentage_relationships,
    pixelized_projection_values,
)


class TestSmallPatch:
    @pytest.mark.answer_test
    def test_hierarchy(self, ds):
        """Test basic grid attributes."""
        return grid_hierarchy(ds)

    @pytest.mark.answer_test
    def test_grids_relations(self, ds):
        """Test grid parent <-> child relations."""
        return parentage_relationships(ds)

    @pytest.mark.answer_test
    def test_grid_value(self, ds, field):
        """Test grid values for a given field."""
        return grid_values(ds, field)

    @pytest.mark.answer_test
    @pytest.mark.parametrize(
        "dobj_name",
        [None, ("sphere", ("max", (0.1, "unitary")))],
        ids=("entire_domain", "small_sphere"),
    )
    @pytest.mark.parametrize("axis", [0, 1, 2], ids=["x", "y", "z"])
    @pytest.mark.parametrize(
        "weight_field",
        [None, ("gas", "density")],
        ids=["no_weight", "weighted_by_density"],
    )
    def test_pixelized_projection(self, ds, axis, field, dobj_name, weight_field):
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
    def test_field_values(self, ds, field, dobj_name):
        """Test common combination of field values (answer test)."""
        return field_values(ds, field, obj_type=dobj_name, particle_type=False)
