from itertools import product

import pytest

from yt.loaders import load
from yt.utilities.answer_testing.framework import data_dir_load
from yt.utilities.exceptions import YTAmbiguousDataType, YTUnidentifiedDataType

datasets = {
    "cloud": "ShockCloud/id0/Cloud.0050.vtk",
    "blast": "MHDBlast/id0/Blast.0100.vtk",
    "stripping": "RamPressureStripping/id0/rps.0062.vtk",
    "sloshing": "MHDSloshing/virgo_low_res.0054.vtk",
}

fields = {
    "blast": (
        ("gas", "temperature"),
        ("gas", "density"),
        ("gas", "velocity_magnitude"),
    ),
    "cloud": (
        ("athena", "scalar[0]"),
        ("gas", "density"),
        ("gas", "total_energy_density"),
    ),
    "stripping": (
        ("gas", "temperature"),
        ("gas", "density"),
        ("athena", "specific_scalar[0]"),
    ),
}

units_override = {
    "blast": {
        "length_unit": (1.0, "pc"),
        "mass_unit": (2.38858753789e-24, "g/cm**3*pc**3"),
        "time_unit": (1.0, "s*pc/km"),
    },
    "stripping": {
        "time_unit": 3.086e14,
        "length_unit": 8.0236e22,
        "mass_unit": 9.999e-30 * 8.0236e22**3,
    },
    "sloshing": {
        "length_unit": (1.0, "Mpc"),
        "time_unit": (1.0, "Myr"),
        "mass_unit": (1.0e14, "Msun"),
    },
}


def pytest_generate_tests(metafunc):
    if "ds" in metafunc.fixturenames:
        if "field" in metafunc.fixturenames:
            params = []
            for ds_name, ds_fields in fields.items():
                params += list(product([ds_name], ds_fields))
            metafunc.parametrize(
                "ds,field",
                params,
                indirect=True,
                ids=[f"{param[0]}-{param[1][0]}_{param[1][1]}" for param in params]
            )
        else:
            metafunc.parametrize("ds", list(datasets), indirect=True)


@pytest.fixture(scope="module")
def ds(request):
    try:
        if request.param in datasets:
            try:
                load_kwargs = {"units_override": units_override[request.param]}
            except KeyError:
                load_kwargs = None
            return data_dir_load(datasets[request.param], kwargs=load_kwargs)
        else:
            raise ValueError("invalid internal test config")
    except (FileNotFoundError, YTUnidentifiedDataType, YTAmbiguousDataType) as exc:
        pytest.skip(reason=f"Loading {request.param} raised {exc}")


@pytest.fixture(scope="module")
def field(request):
    return request.param


@pytest.fixture(scope="module")
def weight_field(request):
    return request.param


def get_dataset(key, uo=True, nprocs=1, mag_norm="gaussian"):
    try:
        if uo:
            return load(
                datasets[key],
                units_override=units_override[key],
                nprocs=nprocs,
                magnetic_normalization=mag_norm
            )
        else:
            return load(datasets[key], nprocs=nprocs, magnetic_normalization=mag_norm)
    except (FileNotFoundError, YTUnidentifiedDataType, YTAmbiguousDataType) as exc:
        pytest.skip(reason=f"Loading {datasets[key]} raised {exc}")


@pytest.fixture(scope="module")
def blast_uo():
    return get_dataset("blast")


@pytest.fixture(scope="module")
def cloud():
    return get_dataset("cloud", uo=False)


@pytest.fixture(scope="module")
def sloshing_uo():
    return get_dataset("sloshing")


@pytest.fixture(scope="module")
def sloshing_uo_lorentz():
    return get_dataset("sloshing", mag_norm="lorentz_heaviside")


@pytest.fixture(scope="module")
def sloshing_uo_np8():
    return get_dataset("sloshing", nprocs=8)
