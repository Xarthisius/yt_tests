"""Basic tests for AMRVAC frontend."""
import pytest

from yt.utilities.answer_testing.answer_tests import field_values


@pytest.mark.answer_test
@pytest.mark.parametrize(
    "dobj_name",
    [None, ("sphere", ("max", (0.1, "unitary")))],
    ids=("entire_domain", "small_sphere"),
)
def test_field_values(ds, field, dobj_name):
    """Test common combination of field values (answer test)."""
    return field_values(ds, field, obj_type=dobj_name, particle_type=False)
