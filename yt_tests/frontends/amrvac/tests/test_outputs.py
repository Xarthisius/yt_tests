"""Basic tests for AMRVAC frontend."""
import pytest
import numpy as np

from yt.frontends.amrvac.api import AMRVACDataset
from yt.utilities.answer_testing.framework import data_dir_load
from yt.utilities.answer_testing.testing_utilities import can_run_ds

from yt_tests.small_patch import SmallPatchTest

khi_cartesian_2D = "amrvac/kh_2d0000.dat"
blastwave_cartesian_3D = "amrvac/bw_3d0000.dat"


@pytest.mark.skipif(
    not can_run_ds(khi_cartesian_2D), reason=f"Dataset {khi_cartesian_2D} not found."
)
def test_AMRVACDataset():
    """Check if a sample file is recognized as a proper dataset."""
    assert isinstance(data_dir_load(khi_cartesian_2D), AMRVACDataset)


@pytest.mark.skipif(
    not can_run_ds(blastwave_cartesian_3D),
    reason=f"Dataset {blastwave_cartesian_3D} not found.",
)
def test_domain_size():
    """Check for correct box size, see bw_3d.par."""
    ds = data_dir_load(blastwave_cartesian_3D)
    for obj in (ds.domain_left_edge, ds.domain_right_edge, ds.domain_width):
        assert isinstance(obj, np.ndarray)
        assert len(obj) == 3
    for lb in ds.domain_left_edge:
        assert int(lb) == 0
    for rb in ds.domain_right_edge:
        assert int(rb) == 2
    for w in ds.domain_width:
        assert int(w) == 2


class TestAMRVACSmallPatch(SmallPatchTest):

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
        if ds.geometry == "cylindrical" and axis == 1:
            pytest.skip(f"Projection along 'y' is not supported for {ds.geometry} geometry")
        if ds.geometry == "polar" and axis == 2:
            pytest.skip(f"Projection along 'z' is not supported for {ds.geometry} geometry")

        return super().test_pixelized_projection(ds, axis, field, dobj_name, weight_field)
