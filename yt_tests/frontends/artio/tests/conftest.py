# content of conftest.py
import pytest

from yt.utilities.answer_testing.framework import data_dir_load
from yt_tests.small_patch import parameterize_sph_patch_tests

sizmbhloz = "sizmbhloz-clref04SNth-rs9_a0.9011/sizmbhloz-clref04SNth-rs9_a0.9011.art"
fields = (
    ("gas", "temperature"),
    ("gas", "density"),
    ("gas", "velocity_magnitude"),
    ("deposit", "all_density"),
    ("deposit", "all_count"),
)
weights = [None, ('gas', 'density')]


def pytest_generate_tests(metafunc):
    if "ds_str_repr" in metafunc.fixturenames:
        metafunc.parametrize(
            "ds,ds_str_repr,nparts",
            list(
                zip(
                    ["sizmbhloz"],
                    ["sizmbhloz-clref04SNth-rs9_a0.9011.art"],
                    [210650],
                )
            ),
            indirect=True,
            ids=["sizmbhloz-basic-attrs"],
        )
    elif "ds" in metafunc.fixturenames:
        if "field" in metafunc.fixturenames:
            params, ids = parameterize_sph_patch_tests(
                ["sizmbhloz"], [fields], weights=weights
            )
            metafunc.parametrize(
                "ds,field,weight_field",
                params,
                indirect=True,
                ids=ids,
            )
        else:
            metafunc.parametrize("ds", ["sizmbhloz"], indirect=True)


@pytest.fixture(scope="module")
def field(request):
    return request.param


@pytest.fixture(scope="module")
def weight_field(request):
    return request.param


@pytest.fixture(scope="module")
def ds_str_repr(request):
    return request.param


@pytest.fixture(scope="module")
def nparts(request):
    return request.param


@pytest.fixture(scope="module")
def ds(request):
    if request.param == "sizmbhloz":
        return data_dir_load(sizmbhloz)
    else:
        raise ValueError("invalid internal test config")
