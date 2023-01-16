# content of conftest.py
import pytest

from yt.utilities.answer_testing.framework import data_dir_load


def pytest_generate_tests(metafunc):
    if "ds" in metafunc.fixturenames:
        metafunc.parametrize("ds", ["d9p"], indirect=True)


@pytest.fixture
def ds(request):
    if request.param == "d9p":
        return data_dir_load("D9p_500/10MpcBox_HartGal_csf_a0.500.d")
    else:
        raise ValueError("invalid internal test config")
