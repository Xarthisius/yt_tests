import os
import tempfile

import pytest

from yt.frontends.arepo.api import ArepoHDF5Dataset
from yt.testing import ParticleSelectionComparison, assert_allclose_units
from yt.utilities.answer_testing.framework import data_dir_load

try:
    import h5py  # NoQA
except ImportError:
    pytest.skip("h5py not available", allow_module_level=True)

tng59_h5 = "TNGHalo/halo_59.hdf5"
_tng59_bbox = [[40669.34, 56669.34], [45984.04, 61984.04], [54114.9, 70114.9]]


def test_arepo_hdf5_selection(bullet):
    assert isinstance(bullet, ArepoHDF5Dataset)
    psc = ParticleSelectionComparison(bullet)
    psc.run_defaults()


def test_index_override():
    # This tests that we can supply an index_filename, and that when we do, it
    # doesn't get written if our bounding_box is overwritten.
    tmpfd, tmpname = tempfile.mkstemp(suffix=".index6_4.ewah")
    os.close(tmpfd)
    ds = data_dir_load(
        tng59_h5, kwargs={"index_filename": tmpname, "bounding_box": _tng59_bbox}
    )
    assert isinstance(ds, ArepoHDF5Dataset)
    ds.index
    assert os.stat(tmpname).st_size > 0


def test_arepo_tng59_periodicity(tng59_nobbox):
    assert tng59_nobbox.periodicity == (True, True, True)


def test_arepo_tng59_periodicity_with_bbox(tng59_bbox):
    assert tng59_bbox.periodicity == (False, False, False)


def test_nh_density(tng59_bbox):
    ad = tng59_bbox.all_data()
    assert_allclose_units(
        ad["gas", "H_number_density"], (ad["gas", "H_nuclei_density"])
    )


def test_arepo_tng59_selection(tng59_bbox):
    psc = ParticleSelectionComparison(tng59_bbox)
    psc.run_defaults()
