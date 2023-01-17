# content of conftest.py
from collections import defaultdict
from itertools import product

import pytest

from yt.utilities.answer_testing.framework import data_dir_load

_datasets = {
    "blastwave_spherical_2D": "amrvac/bw_2d0000.dat",
    "khi_cartesian_2D": "amrvac/kh_2d0000.dat",
    "khi_cartesian_3D": "amrvac/kh_3D0000.dat",
    "jet_cylindrical_25D": "amrvac/Jet0003.dat",
    "riemann_cartesian_175D": "amrvac/R_1d0005.dat",
    "blastwave_cartesian_3D": "amrvac/bw_3d0000.dat",
    "blastwave_polar_2D": "amrvac/bw_polar_2D0000.dat",
    "blastwave_cylindrical_3D": "amrvac/bw_cylindrical_3D0000.dat",
    "rmi_cartesian_dust_2D": "amrvac/Richtmyer_Meshkov_dust_2D/RM2D_dust_Kwok0000.dat",
}

_fields = {
    "rmi_cartesian_dust_2D": [
        "density",
        "velocity_magnitude",
        "energy_density",
        "total_dust_density",
    ]
}
_fields = defaultdict(
    lambda: [
        "density",
        "velocity_magnitude",
        "magnetic_energy_density",
        "energy_density",
    ],  # default for everything else
    _fields,
)


def pytest_generate_tests(metafunc):
    if "ds" in metafunc.fixturenames:
        if "field" in metafunc.fixturenames:
            params = []
            for ds_name in _datasets:
                params += list(product([ds_name], _fields[ds_name]))
            metafunc.parametrize(
                "ds,field",
                params,
                indirect=True,
            )
        else:
            metafunc.parametrize("ds", list(_datasets), indirect=True)


@pytest.fixture(scope="module")
def ds(request):
    if request.param in _datasets:
        return data_dir_load(_datasets[request.param])
    else:
        raise ValueError("invalid internal test config")


@pytest.fixture(scope="module")
def field(request):
    return request.param
