from typing import Any, Dict, List, Optional

from aliceio.enums.entity import EntityType
from aliceio.enums.update import RequestType
from aliceio.types import (
    NLU,
    AliceRequest,
    ApiState,
    Application,
    DateTimeEntity,
    Entity,
    FIOEntity,
    GeoEntity,
    Interfaces,
    Markup,
    Meta,
    Payload,
    Session,
    TokensEntity,
    Update,
    User,
)
from aliceio.types.nlu import Intents
from tests.mocked.mocked_skill import MockedSkill


def create_mocked_update(
    skill: Optional[MockedSkill] = None,
    meta: Optional[Meta] = None,
    interfaces: Optional[Interfaces] = None,
    user: Optional[User] = None,
    application: Optional[Application] = None,
    is_new: Optional[bool] = None,
    session: Optional[Session] = None,
    request: Optional[AliceRequest] = None,
    request_type: Optional[str] = None,
    payload: Optional[Payload] = None,
    command: Optional[str] = None,
    original_utterance: Optional[str] = None,
    markup: Optional[Markup] = None,
    nlu: Optional[NLU] = None,
    tokens: Optional[List[str]] = None,
    intents: Optional[Dict[str, Any]] = None,
    entities: Optional[List[Entity]] = None,
    state: Optional[ApiState] = None,
) -> Update:
    meta = create_mocked_meta(meta, interfaces)
    session = create_mocked_session(session, user, application, is_new)
    request = create_mocked_alice_request(
        request,
        request_type,
        payload,
        command,
        original_utterance,
        markup,
        nlu,
        tokens,
        intents,
        entities,
    )

    return Update(
        meta=meta,
        session=session,
        request=request,
        version="1.0",
        context={"skill": skill} if skill else None,
        state=state or ApiState(session={}, user={}, application={}),
    )


def create_mocked_meta(
    meta: Optional[Meta] = None,
    interfaces: Optional[Interfaces] = None,
) -> Meta:
    return meta or Meta(
        locale="ru-RU",
        timezone="Europe/Moscow",
        client_id="none/none (none none; none none)",
        interfaces=interfaces
        or Interfaces(
            screen={},
            account_linking={},
            payments={},
        ),
    )


def create_mocked_session(
    session: Optional[Session] = None,
    user: Optional[User] = None,
    application: Optional[Application] = None,
    is_new: Optional[bool] = None,
) -> Session:
    return session or Session(
        message_id=0,
        session_id="42:SESSION_ID",
        skill_id="42:SKILL_ID",
        user=user
        or User(
            user_id="42:USER_ID",
            access_token="42:ACCESS_TOKEN",
        ),
        application=application
        or Application(
            application_id="42:APP_ID",
        ),
        new=bool(is_new),
    )


def create_mocked_alice_request(
    request: Optional[AliceRequest] = None,
    request_type: Optional[str] = None,
    payload: Optional[Payload] = None,
    command: Optional[str] = None,
    original_utterance: Optional[str] = None,
    markup: Optional[Markup] = None,
    nlu: Optional[NLU] = None,
    tokens: Optional[List[str]] = None,
    intents: Optional[Intents] = None,
    entities: Optional[List[Entity]] = None,
) -> AliceRequest:
    return request or AliceRequest(
        type=request_type or RequestType.SIMPLE_UTTERANCE,
        payload=payload or {},
        command=command or "закажи пиццу на улицу льва толстого 16 на завтра",
        original_utterance=(
            original_utterance or "закажи пиццу на улицу льва толстого, 16 на завтра"
        ),
        markup=markup
        or Markup(
            dangerous_context=True,
        ),
        nlu=nlu
        or NLU(
            tokens=tokens
            or [
                "закажи",
                "пиццу",
                "на",
                "льва",
                "толстого",
                "16",
                "на",
                "завтра",
            ],
            intents=intents or {},
            entities=entities
            or [
                Entity(
                    tokens=TokensEntity(
                        start=2,
                        end=6,
                    ),
                    type=EntityType.YANDEX_GEO,
                    value=GeoEntity(
                        house_number=16,
                        street="льва толстого",
                    ),
                ),
                Entity(
                    tokens=TokensEntity(
                        start=3,
                        end=5,
                    ),
                    type=EntityType.YANDEX_FIO,
                    value=FIOEntity(
                        first_name="лев",
                        last_name="толстой",
                    ),
                ),
                Entity(
                    tokens=TokensEntity(
                        start=6,
                        end=8,
                    ),
                    type=EntityType.YANDEX_DATETIME,
                    value=DateTimeEntity(
                        day=1,
                        day_is_relative=True,
                    ),
                ),
            ],
        ),
    )
