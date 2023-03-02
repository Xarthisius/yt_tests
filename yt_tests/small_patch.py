from itertools import product
import os
import pytest
from yt.utilities.answer_testing.answer_tests import (
    field_values,
    grid_hierarchy,
    grid_values,
    parentage_relationships,
    pixelized_projection_values,
)


class SmallPatchTest:
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


class SPHSmallPatchTest:
    @pytest.mark.answer_test
    @pytest.mark.parametrize(
        "dobj_name",
        [None, ("sphere", ("max", (0.1, "unitary")))],
        ids=("entire_domain", "small_sphere"),
    )
    @pytest.mark.parametrize("axis", [0, 1, 2], ids=["x", "y", "z"])
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
    def test_field_values(self, ds, dobj_name, weight_field, field):
        """Test common combination of field values (answer test)."""
        is_particle_field = field[0] in ds.particle_types
        return field_values(ds, field, obj_type=dobj_name, particle_type=is_particle_field)

    def test_basic_attrs(self, ds, ds_str_repr, nparts):
        assert str(ds) == ds_str_repr
        dd = ds.all_data()
        assert dd["all", "particle_position"].shape == (nparts, 3)
        tot = sum(
            dd[ptype, "particle_position"].shape[0] for ptype in ds.particle_types_raw
        )
        assert tot == nparts


def parameterize_sph_patch_tests(ds_list, fields_list, weights=None):
    params = []
    for ds, fields in zip(ds_list, fields_list):
        if weights:
            fields = product(fields, weights)
        params += [(_[0], *_[1]) for _ in product([ds], fields)]
    ids = [
        (os.path.splitext(os.path.basename(dsname))[0], "_".join(f), "_".join(w))
        if w
        else (
            os.path.splitext(os.path.basename(dsname))[0],
            "_".join(f),
            "no_weight",
        )
        for dsname, f, w in params
    ]
    ids = ["-".join(_) for _ in ids]
    return params, ids
