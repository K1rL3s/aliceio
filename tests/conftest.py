from pathlib import Path
from typing import AsyncGenerator, List, Optional

import pytest
from _pytest.config import Config, UsageError
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from redis.asyncio.connection import parse_url as parse_redis_url

from aliceio import Dispatcher
from aliceio.fsm.storage.memory import MemoryStorage
from aliceio.fsm.storage.redis import RedisStorage
from aliceio.types import Update
from aliceio.types.base import MutableAliceObject
from tests.mocked.mocked_skill import MockedSkill
from tests.mocked.mocked_update import create_mocked_update

DATA_DIR = Path(__file__).parent / "data"


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--redis",
        default=None,
        help="run tests which require redis connection",
    )


def pytest_configure(config: Config) -> None:
    config.addinivalue_line(
        "markers",
        "redis: marked tests require redis connection to run",
    )


def pytest_collection_modifyitems(config: Config, items: List[Function]) -> None:
    redis_uri = config.getoption("--redis")
    if redis_uri is None:
        skip_redis = pytest.mark.skip(
            reason="need --redis option with redis URI to run",
        )
        for item in items:
            if "redis" in item.keywords:
                item.add_marker(skip_redis)
        return
    try:
        parse_redis_url(redis_uri)
    except ValueError as e:
        raise UsageError(f"Invalid redis URI {redis_uri!r}: {e}")


@pytest.fixture()
def redis_server(request: SubRequest) -> Optional[str]:
    redis_uri = request.config.getoption("--redis")
    return redis_uri


@pytest.fixture()
@pytest.mark.redis
async def redis_storage(redis_server) -> AsyncGenerator[RedisStorage, None]:
    if not redis_server:
        pytest.skip("Redis is not available here")
    storage = RedisStorage.from_url(redis_server)
    try:
        await storage.redis.info()
    except ConnectionError as e:
        pytest.skip(str(e))
    try:
        yield storage
    finally:
        conn = await storage.redis
        await conn.flushdb()
        await storage.close()


@pytest.fixture()
async def memory_storage() -> AsyncGenerator[MemoryStorage, None]:
    storage = MemoryStorage()
    try:
        yield storage
    finally:
        await storage.close()


@pytest.fixture()
def skill() -> MockedSkill:
    return MockedSkill()


@pytest.fixture()
def update(skill: MockedSkill) -> Update:
    return create_mocked_update(skill)


@pytest.fixture()
def event(skill: MockedSkill, update: Update) -> MutableAliceObject:
    return update.event


@pytest.fixture()
async def dispatcher() -> AsyncGenerator[Dispatcher, None]:
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()
