from typing import Any

import pytest

from aliceio.types import Interfaces


class TestInterfaces:
    @pytest.mark.parametrize(
        "kwargs",
        [
            {},
            {"account_linking": {}},
            {"screen": {}},
            {"audio_player": {}},
            {"payments": {}},
            {"account_linking": {}, "screen": {}, "audio_player": {}, "payments": {}},
        ],
    )
    def test_available_interfaces(self, kwargs: dict[str, Any]) -> None:
        interfaces = Interfaces(**kwargs)
        assert kwargs.keys() == interfaces.available_interfaces == interfaces.available

    def test_available_interfaces_incorrect_init(self) -> None:
        interfaces = Interfaces(amongus="kindasus")
        assert interfaces.available_interfaces == interfaces.available == set()

    @pytest.mark.parametrize(
        "kwargs",
        [
            {},
            {"account_linking": {}},
            {"screen": {}},
            {"audio_player": {}},
            {"payments": {}},
            {"account_linking": {}, "screen": {}, "audio_player": {}, "payments": {}},
        ],
    )
    def test_is_interface_available(self, kwargs: dict[str, Any]) -> None:
        interfaces = Interfaces(**kwargs)

        for interface in kwargs:
            assert interfaces.is_interface_available(interface)
            assert interfaces.has(interface)

    def test_is_intreface_available_incorrect_init(self) -> None:
        interfaces = Interfaces(amongus="kindasus")

        assert not interfaces.is_interface_available("amongus")
        assert not interfaces.has("amongus")
