import os
import pytest
from yt.config import ytcfg
from yt.data_objects.static_output import Dataset
from yt.loaders import load
from yt.utilities.exceptions import (
    YTAmbiguousDataType,
    YTUnidentifiedDataType,
)


def dataset_exists(fname, file_check=False):
    if isinstance(fname, Dataset):
        return
    test_root = ytcfg.get("yt", "test_data_dir")
    if not os.path.isdir(test_root):
        pytest.skip(f"{test_root=} does not exist (yt-cfg['yt', 'test_data_dir'])")

    if file_check and not os.path.isfile(os.path.join(test_root, fname)):
        pytest.skip(f"{fname} doesn't exist in {test_root}")

    try:
        load(fname)
    except FileNotFoundError:
        pytest.fail("...")
    except (YTUnidentifiedDataType, YTAmbiguousDataType) as exc:
        pytest.skip(f"Loading data raised: {exc}")


@pytest.fixture
def requires_ds():
    pytest.requires_ds = dataset_exists
