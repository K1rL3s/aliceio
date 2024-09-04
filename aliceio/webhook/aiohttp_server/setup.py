from typing import Any

from aiohttp.abc import Application

from aliceio import Dispatcher


def setup_application(
    app: Application,
    dispatcher: Dispatcher,
    /,
    **kwargs: Any,
) -> None:
    """
    Эта функция помогает настроить процесс запуска-выключения.

    :param app: aiohttp app
    :param dispatcher: aliceio dispatcher
    :param kwargs: additional data
    :return:
    """
    workflow_data = {
        "app": app,
        "dispatcher": dispatcher,
        **dispatcher.workflow_data,
        **kwargs,
    }

    async def on_startup(*_: Any, **__: Any) -> None:  # pragma: no cover
        await dispatcher.emit_startup(**workflow_data)

    async def on_shutdown(*_: Any, **__: Any) -> None:  # pragma: no cover
        await dispatcher.emit_shutdown(**workflow_data)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
