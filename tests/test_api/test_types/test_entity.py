from typing import Any

import pytest

from aliceio.enums import EntityType
from aliceio.types import (
    NLU,
    DateTimeEntity,
    Entity,
    FIOEntity,
    GeoEntity,
    Message,
    NLUEntity,
    NumberEntity,
    Update,
)


class TestEntity:
    @pytest.mark.parametrize(
        "data",
        [
            {
                "type": "unknown",
                "value": {
                    "field": "value",
                    "pole": "znachenie",
                },
            },
            {
                "type": "YANDEX.UNKNOWN",
                "value": {
                    "1": "2",
                    "3": "4",
                },
            },
        ],
    )
    def test_unknown_entity(self, data: dict[str, Any]) -> None:
        data.update({"tokens": {"start": 0, "end": 0}})
        entity = Entity.model_validate(data)

        assert isinstance(entity.value, NLUEntity)

    @pytest.mark.parametrize(
        "nlu_type,nlu_entity,data",
        [
            [
                EntityType.YANDEX_FIO,
                FIOEntity,
                {
                    "type": "YANDEX.FIO",
                    "value": {
                        "first_name": "антон",
                        "patronymic_name": "павлович",
                        "last_name": "чехов",
                    },
                },
            ],
            [
                EntityType.YANDEX_FIO,
                FIOEntity,
                {
                    "type": "YANDEX.FIO",
                    "value": {
                        "first_name": "лев",
                        "last_name": "толстой",
                    },
                },
            ],
            [
                EntityType.YANDEX_FIO,
                FIOEntity,
                {
                    "type": "YANDEX.FIO",
                    "value": {
                        "first_name": "лев",
                    },
                },
            ],
            [
                EntityType.YANDEX_GEO,
                GeoEntity,
                {
                    "type": "YANDEX.GEO",
                    "value": {
                        "country": "россия",
                        "city": "москва",
                        "street": "улица льва толстого",
                        "house_number": "16",
                    },
                },
            ],
            [
                EntityType.YANDEX_GEO,
                GeoEntity,
                {
                    "type": "YANDEX.GEO",
                    "value": {
                        "airport": "аэропорт внуково",
                    },
                },
            ],
            [
                EntityType.YANDEX_DATETIME,
                DateTimeEntity,
                {
                    "type": "YANDEX.DATETIME",
                    "value": {
                        "year": 1982,
                        "month": 9,
                        "day": 15,
                        "hour": 22,
                        "minute": 30,
                    },
                },
            ],
            [
                EntityType.YANDEX_DATETIME,
                DateTimeEntity,
                {
                    "type": "YANDEX.DATETIME",
                    "value": {
                        "day": -1,
                        "day_is_relative": True,
                    },
                },
            ],
        ],
    )
    def test_known_entity(
        self,
        nlu_type: str,
        nlu_entity: type[NLUEntity],
        data: dict[str, Any],
    ) -> None:
        data.update({"tokens": {"start": 0, "end": 0}})
        entity = Entity.model_validate(data)

        assert entity.type == nlu_type
        assert isinstance(entity.value, NLUEntity)
        assert isinstance(entity.value, nlu_entity)
        assert type(entity.value) == nlu_entity

    @pytest.mark.parametrize(
        "nlu_type,nlu_entity,data",
        [
            [
                EntityType.YANDEX_NUMBER,
                int,
                {
                    "type": "YANDEX.NUMBER",
                    "value": 33,
                },
            ],
            [
                EntityType.YANDEX_NUMBER,
                float,
                {
                    "type": "YANDEX.NUMBER",
                    "value": 4.5,
                },
            ],
        ],
    )
    def test_number_entity(
        self,
        nlu_type: str,
        nlu_entity: type[NumberEntity],
        data: dict[str, Any],
    ) -> None:
        data.update({"tokens": {"start": 0, "end": 0}})
        entity = Entity.model_validate(data)

        assert entity.type == nlu_type
        assert isinstance(entity.value, nlu_entity)
        assert type(entity.value) == nlu_entity

    def test_entities_types_in_event(self) -> None:
        update_dict = {
            "meta": {"locale": "", "timezone": "", "client_id": "", "interfaces": {}},
            "session": {
                "message_id": 0,
                "session_id": "",
                "skill_id": "",
                "user": {"user_id": ""},
                "application": {"application_id": ""},
                "new": False,
                "user_id": "",
            },
            "request": {
                "command": "иван иванов 4 улица прямая 5 января сегодня",
                "original_utterance": "иван иванов 4 улица Прямая пятое января сегодня",
                "nlu": {
                    "tokens": [
                        "иван",
                        "иванов",
                        "4",
                        "5",
                        "улица",
                        "прямая",
                        "5",
                        "января",
                        "сегодня",
                    ],
                    "entities": [
                        {
                            "type": "YANDEX.FIO",
                            "tokens": {"start": 0, "end": 2},
                            "value": {"first_name": "иван", "last_name": "иванов"},
                        },
                        {
                            "type": "YANDEX.NUMBER",
                            "tokens": {"start": 2, "end": 4},
                            "value": 4.5,
                        },
                        {
                            "type": "YANDEX.GEO",
                            "tokens": {"start": 4, "end": 7},
                            "value": {"street": "улица прямая", "house_number": "5"},
                        },
                        {
                            "type": "YANDEX.NUMBER",
                            "tokens": {"start": 6, "end": 7},
                            "value": 5,
                        },
                        {
                            "type": "YANDEX.DATETIME",
                            "tokens": {"start": 6, "end": 8},
                            "value": {
                                "month": 1,
                                "day": 5,
                                "month_is_relative": False,
                                "day_is_relative": False,
                            },
                        },
                        {
                            "type": "YANDEX.DATETIME",
                            "tokens": {"start": 8, "end": 9},
                            "value": {"day": 0, "day_is_relative": True},
                        },
                    ],
                    "intents": {},
                },
                "markup": {"dangerous_context": False},
                "type": "SimpleUtterance",
            },
            "state": {"session": {}, "user": {"data": {}}, "application": {}},
            "version": "1.0",
        }
        update = Update.model_validate(update_dict)

        message = update.message
        assert isinstance(message, Message)

        nlu = message.nlu
        assert isinstance(nlu, NLU)

        assert len(nlu.entities) == 6
        fio, num4_5, geo, num5, date, today = nlu.entities

        assert isinstance(fio.value, FIOEntity)
        assert fio.value.first_name == "иван"
        assert fio.value.last_name == "иванов"

        assert isinstance(num4_5.value, float)
        assert num4_5.value == 4.5

        assert isinstance(geo.value, GeoEntity)
        assert geo.value.street == "улица прямая"
        assert geo.value.house_number == 5

        assert isinstance(num5.value, int)
        assert num5.value == 5

        assert isinstance(date.value, DateTimeEntity)
        assert date.value.month == 1
        assert date.value.day == 5
        assert date.value.month_is_relative is False
        assert date.value.day_is_relative is False

        assert isinstance(today.value, DateTimeEntity)
        assert today.value.day == 0
        assert today.value.day_is_relative is True
