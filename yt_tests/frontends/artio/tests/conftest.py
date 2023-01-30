# content of conftest.py
import pytest

from yt.utilities.answer_testing.framework import data_dir_load

sizmbhloz = "sizmbhloz-clref04SNth-rs9_a0.9011/sizmbhloz-clref04SNth-rs9_a0.9011.art"


def pytest_generate_tests(metafunc):
    if "ds" in metafunc.fixturenames:
        metafunc.parametrize("ds", ["sizmbhloz"], indirect=True)


@pytest.fixture(scope="module")
def ds(request):
    if request.param == "sizmbhloz":
        return data_dir_load(sizmbhloz)
    else:
        raise ValueError("invalid internal test config")
