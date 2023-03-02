from itertools import product

import pytest

from yt.loaders import load
from yt.utilities.answer_testing.framework import data_dir_load
from yt.utilities.exceptions import YTAmbiguousDataType, YTUnidentifiedDataType

datasets = {
    "AM06": "AM06/AM06.out1.00400.athdf",
}

fields = {
    "AM06": (
        ("gas", "temperature"),
        ("gas", "density"),
        ("gas", "velocity_magnitude"),
        ("gas", "magnetic_field_x"),
    ),
}

units_override = {
    "AM06": {
        "length_unit": (1.0, "kpc"),
        "mass_unit": (1.0, "Msun"),
        "time_unit": (1.0, "Myr"),
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


def get_dataset(key, uo=True, mag_norm="gaussian"):
    try:
        if uo:
            return load(
                datasets[key],
                units_override=units_override[key],
                magnetic_normalization=mag_norm
            )
        else:
            return load(datasets[key], magnetic_normalization=mag_norm)
    except (FileNotFoundError, YTUnidentifiedDataType, YTAmbiguousDataType) as exc:
        pytest.skip(reason=f"Loading {datasets[key]} raised {exc}")


@pytest.fixture(scope="module")
def AM06_uo():
    return get_dataset("AM06")


@pytest.fixture(scope="module")
def AM06():
    return get_dataset("AM06", uo=False)


@pytest.fixture(scope="module")
def AM06_uo_lorentz():
    return get_dataset("AM06", mag_norm="lorentz_heaviside")


@pytest.fixture(scope="module")
def AM06_code():
    try:
        return load(datasets["AM06"], unit_system="code")
    except (FileNotFoundError, YTUnidentifiedDataType, YTAmbiguousDataType) as exc:
        pytest.skip(reason=f"Loading {datasets['AM06']} raised {exc}")
