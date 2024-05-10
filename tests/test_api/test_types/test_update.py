from typing import Any, Dict, Type

import pytest

from aliceio.types import (
    AudioPlayer,
    ButtonPressed,
    Message,
    Purchase,
    ShowPull,
    Update,
)
from aliceio.types.base import MutableAliceObject


class TestUpdate:
    @pytest.mark.parametrize(
        "event,event_type,attr",
        [
            [
                {"request": {"type": "AudioPlayer.PlaybackStarted"}},
                AudioPlayer,
                "audio_player",
            ],
            [
                {"request": {"type": "AudioPlayer.PlaybackNearlyFinished"}},
                AudioPlayer,
                "audio_player",
            ],
            [
                {"request": {"type": "AudioPlayer.PlaybackFinished"}},
                AudioPlayer,
                "audio_player",
            ],
            [
                {"request": {"type": "AudioPlayer.PlaybackStopped"}},
                AudioPlayer,
                "audio_player",
            ],
            [
                {"request": {"type": "AudioPlayer.PlaybackFailed"}},
                AudioPlayer,
                "audio_player",
            ],
            [
                {"request": {"payload": {}, "type": "ButtonPressed"}},
                ButtonPressed,
                "button_pressed",
            ],
            [
                {
                    "request": {
                        "type": "Purchase.Confirmation",
                        "purchase_request_id": "d432de19be8347d09f656d9fe966e2f9",
                        "purchase_token": "token_value",
                        "order_id": "eeb59d64-9e6a-11ea-bb37-0242ac130002",
                        "purchase_timestamp": 1590399311,
                        "purchase_payload": {"value": "payload"},
                        "signed_data": "purchase_request_id=id_value&...",
                        "signature": "Pi6JNCFeeleRa...",
                    },
                },
                Purchase,
                "purchase",
            ],
            [
                {"request": {"type": "Show.Pull", "show_type": "MORNING"}},
                ShowPull,
                "show_pull",
            ],
            [
                {
                    "request": {
                        "type": "SimpleUtterance",
                        "command": "test",
                        "original_utterance": "test",
                    },
                },
                Message,
                "message",
            ],
        ],
    )
    def test_event(
        self,
        event: Dict[str, Any],
        event_type: Type[MutableAliceObject],
        attr: str,
    ):
        event.update(
            {
                "meta": {
                    "locale": "ru-RU",
                    "timezone": "Europe/Moscow",
                    "client_id": "yandex.searchplugin/7.16 (none none; android 4.4.2)",
                    "interfaces": {
                        "screen": {},
                        "account_linking": {},
                        "audio_player": {},
                    },
                },
                "session": {
                    "message_id": 0,
                    "session_id": "42:SESSION",
                    "skill_id": "42:SKILL_ID",
                    "user_id": "42:USER",
                    "user": {"user_id": "42:USER", "access_token": "42:TOKEN"},
                    "application": {"application_id": "42:APP"},
                    "new": True,
                },
                "state": {"session": {}, "user": {}, "application": {}},
                "version": "1.0",
            },
        )

        update = Update.model_validate(event)

        assert isinstance(update.event, event_type)
        assert type(update.event) == event_type

        assert update.event == getattr(update, attr)
        assert isinstance(getattr(update, attr), event_type)
        assert type(getattr(update, attr)) == event_type
