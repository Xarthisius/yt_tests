import pytest
from yt_tests.small_patch import SPHSmallPatchTest


class TestArepoSPHSmallPatchTest(SPHSmallPatchTest):
    @pytest.mark.answer_test
    @pytest.mark.parametrize(
        "dobj_name",
        [None, ("sphere", ("max", (0.1, "unitary")))],
        ids=("entire_domain", "small_sphere"),
    )
    def test_field_values(self, ds, dobj_name, weight_field, field):
        """Test common combination of field values (answer test)."""
        if weight_field:
            pytest.skip("Duplicate test")
        return super().test_field_values(ds, dobj_name, weight_field, field)
