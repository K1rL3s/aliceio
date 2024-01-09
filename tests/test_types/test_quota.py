import pytest

from aliceio.types import Quota


class TestQuota:
    @pytest.mark.parametrize(
        "total,used,available",
        [
            [10, 5, 5],
            [1, 0, 1],
            [0, 0, 0],
            [1024, 24, 1000],
            [1024, 1024, 0],
        ]
    )
    def test_available(self, total: int, used: int, available: int) -> None:
        quota = Quota(total=total, used=used)
        assert quota.available == available
