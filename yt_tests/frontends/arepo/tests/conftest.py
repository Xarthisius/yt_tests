import os
from itertools import product

import pytest

from yt.utilities.answer_testing.framework import data_dir_load
from yt.utilities.exceptions import YTAmbiguousDataType, YTUnidentifiedDataType

cr_h5 = "ArepoCosmicRays/snapshot_039.hdf5"
bullet_h5 = "ArepoBullet/snapshot_150.hdf5"
tng59_h5 = "TNGHalo/halo_59.hdf5"
_tng59_bbox = [[40669.34, 56669.34], [45984.04, 61984.04], [54114.9, 70114.9]]
bullet_fields = [
    (("gas", "density"), None),
    (("gas", "temperature"), None),
    (("gas", "temperature"), ("gas", "density")),
    (("gas", "velocity_magnitude"), None),
]
cr_fields = [
    (("gas", "density"), None),
    (("gas", "cosmic_ray_energy_density"), None),
    (("gas", "cosmic_ray_pressure"), None),
]
tng59_fields = [
    (("gas", "density"), None),
    (("gas", "temperature"), None),
    (("gas", "temperature"), ("gas", "density")),
    (("gas", "H_number_density"), None),
    (("gas", "H_p0_number_density"), None),
    (("gas", "H_p1_number_density"), None),
    (("gas", "El_number_density"), None),
    (("gas", "C_number_density"), None),
    (("gas", "velocity_magnitude"), None),
    (("gas", "magnetic_field_strength"), None),
]


def pytest_generate_tests(metafunc):
    if "field" in metafunc.fixturenames:
        params = []
        for ds_name, fields in zip(
            [bullet_h5, tng59_h5, cr_h5], [bullet_fields, tng59_fields, cr_fields]
        ):
            params += [(_[0], *_[1]) for _ in product([ds_name], fields)]

            # (ds, ds_str_repr, ds_nparticles, field, weight, ds_obj, axis)
        ids = [
            (os.path.splitext(os.path.basename(dsname))[0], "_".join(f), "_".join(w))
            if w
            else (
                os.path.splitext(os.path.basename(dsname))[0],
                "_".join(f),
                "no_weight",
            )
            for dsname, f, w in params
        ]
        ids = ["-".join(_) for _ in ids]
        print(ids)
        metafunc.parametrize(
            "ds,field,weight_field",
            params,
            indirect=True,
            ids=ids,
        )
    elif "ds_str_repr" in metafunc.fixturenames:
        metafunc.parametrize(
            "ds,ds_str_repr,nparts",
            list(
                zip(
                    [bullet_h5, tng59_h5, cr_h5],
                    ["snapshot_150", "halo_59", "snapshot_039"],
                    [26529600, 10107142, 28313510],
                )
            ),
            indirect=True,
            ids=["bullet-basic-attrs", "tng59-basic-attrs", "cr-basic-attrs"],
        )


@pytest.fixture(scope="module")
def ds(request):
    try:
        if request.param == tng59_h5:
            return data_dir_load(tng59_h5, kwargs={"bounding_box": _tng59_bbox})
        elif request.param in (cr_h5, bullet_h5):
            return data_dir_load(request.param)
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


@pytest.fixture(scope="module")
def ds_str_repr(request):
    return request.param


@pytest.fixture(scope="module")
def nparts(request):
    return request.param


@pytest.fixture(scope="module")
def tng59_bbox():
    try:
        return data_dir_load(tng59_h5, kwargs={"bounding_box": _tng59_bbox})
    except (FileNotFoundError, YTUnidentifiedDataType, YTAmbiguousDataType) as exc:
        pytest.skip(reason=f"Loading {tng59_h5} raised {exc}")


@pytest.fixture(scope="module")
def tng59_nobbox():
    try:
        return data_dir_load(tng59_h5)
    except (FileNotFoundError, YTUnidentifiedDataType, YTAmbiguousDataType) as exc:
        pytest.skip(reason=f"Loading {tng59_h5} raised {exc}")


@pytest.fixture(scope="module")
def bullet():
    try:
        return data_dir_load(bullet_h5)
    except (FileNotFoundError, YTUnidentifiedDataType, YTAmbiguousDataType) as exc:
        pytest.skip(reason=f"Loading {bullet_h5} raised {exc}")
