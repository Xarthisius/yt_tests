from itertools import product
import pytest

from yt.utilities.answer_testing.framework import data_dir_load
from yt.utilities.exceptions import YTAmbiguousDataType, YTUnidentifiedDataType


datasets = {
    "Two_D": "F37_80/chimera_00001_grid_1_01.h5",
    "Three_D": "C15-3D-3deg/chimera_002715000_grid_1_01.h5"
}

fields = [
    ("chimera", "a_nuc_rep_c"),
    ("chimera", "abar"),
    ("chimera", "ar36"),
    ("chimera", "be_nuc_rep_c"),
    ("chimera", "c12"),
    ("chimera", "ca40"),
    ("chimera", "cr48"),
    ("chimera", "dudt_nu"),
    ("chimera", "dudt_nuc"),
    ("chimera", "e_book"),
    ("chimera", "e_int"),
    ("chimera", "e_rms_1"),
    ("chimera", "e_rms_2"),
    ("chimera", "e_rms_3"),
    ("chimera", "e_rms_4"),
    ("chimera", "entropy"),
    ("chimera", "fe52"),
    ("chimera", "fe56"),
    ("chimera", "grav_x_c"),
    ("chimera", "grav_y_c"),
    ("chimera", "grav_z_c"),
    ("chimera", "he4"),
    ("chimera", "lumin_1"),
    ("chimera", "lumin_2"),
    ("chimera", "lumin_3"),
    ("chimera", "lumin_4"),
    ("chimera", "mg24"),
    ("chimera", "n"),
    ("chimera", "ne20"),
    ("chimera", "ni56"),
    ("chimera", "nse_c"),
    ("chimera", "num_lumin_1"),
    ("chimera", "num_lumin_2"),
    ("chimera", "num_lumin_3"),
    ("chimera", "num_lumin_4"),
    ("chimera", "o16"),
    ("chimera", "p"),
    ("chimera", "press"),
    ("chimera", "rho_c"),
    ("chimera", "s32"),
    ("chimera", "si28"),
    ("chimera", "t_c"),
    ("chimera", "ti44"),
    ("chimera", "u_c"),
    ("chimera", "v_c"),
    ("chimera", "v_csound"),
    ("chimera", "wBVMD"),
    ("chimera", "w_c"),
    ("chimera", "ye_c"),
    ("chimera", "ylep"),
    ("chimera", "z_nuc_rep_c"),
    ("chimera", "zn60"),
]


def pytest_configure():
    pytest.chimera_fields = fields


def pytest_generate_tests(metafunc):
    if "ds" in metafunc.fixturenames and "field" in metafunc.fixturenames:
        params = list(product(list(datasets), fields))
        metafunc.parametrize(
            "ds,field",
            params,
            indirect=True,
            ids=[f"{param[0]}-{param[1][0]}_{param[1][1]}" for param in params]
        )


def get_dataset(key):
    try:
        return data_dir_load(datasets[key])
    except (FileNotFoundError, YTUnidentifiedDataType, YTAmbiguousDataType) as exc:
        pytest.skip(reason=f"Loading {key} raised {exc}")
    except KeyError:
        raise ValueError("invalid internal test config")


@pytest.fixture(scope="module")
def ds(request):
    return get_dataset(request.param)


@pytest.fixture(scope="module")
def field(request):
    return request.param


@pytest.fixture(scope="module")
def Two_D():
    return get_dataset("Two_D")


@pytest.fixture(scope="module")
def Three_D():
    return get_dataset("Three_D")
