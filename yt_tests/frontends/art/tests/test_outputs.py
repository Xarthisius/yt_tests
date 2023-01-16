import pytest

from yt.frontends.art.api import ARTDataset

def test_d9p(ds):
    assert isinstance(ds, ARTDataset)
