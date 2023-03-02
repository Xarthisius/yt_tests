"""
Chimera frontend tests

"""

import pytest
import numpy as np

from yt.testing import (
    assert_almost_equal,
    assert_array_equal,
    assert_equal,
)


@pytest.mark.answer_test
def test_fields(ds, field):
    if field == ("chimera", "shock"):
        pytest.skip(f"Skip unsupported field '{field}'")
    if field not in ds.field_list:
        pytest.skip(f"Field {field=} not available in {ds=}")
    dd = ds.all_data()
    return [dd[field].min(), dd[field].max(), np.mean(dd[field]), dd[field].size]


def test_2D(Two_D):
    ds = Two_D
    assert_equal(str(ds), "chimera_00001_grid_1_01.h5")
    assert_equal(str(ds.geometry), "spherical")  # Geometry
    assert_almost_equal(
        ds.domain_right_edge,
        ds.arr([1.0116509e10 + 100, 3.14159265e00, 6.28318531e00], "code_length"),
    )  # domain edge
    assert_array_equal(
        ds.domain_left_edge, ds.arr([0.0, 0.0, 0.0], "code_length")
    )  # domain edge
    assert_array_equal(ds.domain_dimensions, np.array([722, 240, 1]))  # Dimensions
    assert_array_equal(ds.field_list, pytest.chimera_fields)


def test_3D(Three_D):
    ds = Three_D
    assert_equal(str(ds), "chimera_002715000_grid_1_01.h5")
    assert_equal(str(ds.geometry), "spherical")  # Geometry
    assert_almost_equal(
        ds.domain_right_edge,
        ds.arr(
            [1.06500257e09 - 1.03818333, 3.14159265e00, 6.2831853e00], "code_length"
        ),
    )  # Domain edge
    assert_array_equal(ds.domain_left_edge, [0.0, 0.0, 0.0])  # Domain edge
    assert_array_equal(ds.domain_dimensions, [542, 60, 135])  # Dimensions
    _fields = pytest.chimera_fields.copy()
    _fields.pop(_fields.index(("chimera", "fe56")))
    assert_array_equal(ds.field_list, _fields)


def test_multimesh(Three_D):  # Tests that the multimesh system for 3D data has been created correctly
    ds = Three_D
    assert_equal(len(ds.index.meshes), 45)
    for i in range(44):
        assert_almost_equal(
            ds.index.meshes[i + 1].connectivity_coords
            - ds.index.meshes[i].connectivity_coords,
            np.tile([0.0, 0.0, 0.13962634015954636], (132004, 1)),
        )  # Tests that each mesh is an identically shaped wedge, incrememnted in Phi.
        assert_array_equal(
            ds.index.meshes[i + 1].connectivity_indices,
            ds.index.meshes[i].connectivity_indices,
        )  # Checks Connectivity array is identical for all meshes.
