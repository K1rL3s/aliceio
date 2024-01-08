from magic_filter import AttrDict

from aliceio import F
from aliceio.filters import MagicData
from aliceio.types import AliceRequest


class TestMagicDataFilter:
    async def test_call(self, event: AliceRequest):
        called = False

        def check(value):
            nonlocal called
            called = True

            assert isinstance(value, AttrDict)
            assert value[0] == "foo"
            assert value[1] == "bar"
            assert value["spam"] is True
            assert value.spam is True
            return value

        f = MagicData(magic_data=F.func(check).as_("test"))
        result = await f(event, "foo", "bar", spam=True)

        assert called
        assert isinstance(result, dict)
        assert result["test"]

    def test_str(self):
        f = MagicData(magic_data=F.event.text == "test")
        assert str(f).startswith("MagicData(magic_data=")
