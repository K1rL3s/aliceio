from typing import Any, Dict, Type

import pytest

from aliceio.enums import EntityType
from aliceio.types import (
    DateTimeEntity,
    Entity,
    FIOEntity,
    GeoEntity,
    NLUEntity,
    NumberEntity,
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
    def test_unknown_entity(self, data: Dict[str, Any]) -> None:
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
        nlu_entity: Type[NLUEntity],
        data: Dict[str, Any],
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
        nlu_entity: Type[NumberEntity],
        data: Dict[str, Any],
    ) -> None:
        data.update({"tokens": {"start": 0, "end": 0}})
        entity = Entity.model_validate(data)

        assert entity.type == nlu_type
        assert isinstance(entity.value, nlu_entity)
        assert type(entity.value) == nlu_entity
