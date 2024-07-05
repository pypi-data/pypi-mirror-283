import pytest

from yatbaf.enums import Event
from yatbaf.group import OnMessage
from yatbaf.handler import Handler


def create_middleware(obj):

    def middleware(handler):

        async def wrapper(update):
            update.ctx["test"].append(obj)
            await handler(update)

        return wrapper

    return middleware


def create_callback(obj):

    async def handler(update):
        update.ctx["test"].append(obj)

    return handler


def test_no_middleware(handler_fn):
    handler = Handler(fn=handler_fn, update_type=Event.MESSAGE)
    handler._resolve_middleware()
    assert handler._middleware_stack == handler._handle


@pytest.mark.asyncio
async def test_middleware(message):
    message.ctx["test"] = []
    handler = Handler(
        fn=create_callback("h"),
        update_type=Event.MESSAGE,
        middleware=[create_middleware("m")],
    )
    handler._resolve_middleware()
    await handler.handle(message)
    assert message.ctx["test"] == ["m", "h"]


@pytest.mark.asyncio
async def test_middleware_order(message):
    message.ctx["test"] = []
    handler = Handler(
        fn=create_callback("h"),
        update_type=Event.MESSAGE,
        middleware=[
            create_middleware("m1"),
            create_middleware("m2"),
            create_middleware("m3"),
        ],
    )
    handler._resolve_middleware()
    await handler.handle(message)
    assert message.ctx["test"] == ["m1", "m2", "m3", "h"]


@pytest.mark.asyncio
async def test_middleware_order_parent(message):
    message.ctx["test"] = []
    handler = Handler(
        fn=create_callback("h"),
        update_type=Event.MESSAGE,
        middleware=[
            create_middleware("hm1"),
            create_middleware("hm2"),
        ],
    )
    router = OnMessage(
        handler_middleware=[
            create_middleware("rm1"),
            create_middleware("rm2"),
        ],
        handlers=[
            OnMessage(
                handlers=[handler],
                handler_middleware=[create_middleware("rm3")],
            )
        ]
    )
    router.on_registration()
    await handler.handle(message)
    assert message.ctx["test"] == ["rm1", "rm2", "rm3", "hm1", "hm2", "h"]


@pytest.mark.asyncio
async def test_middleware_order_parent_local(message):
    message.ctx["test"] = []
    handler = Handler(
        fn=create_callback("h"),
        update_type=Event.MESSAGE,
        middleware=[
            create_middleware("hm1"),
            create_middleware("hm2"),
        ],
    )
    router = OnMessage(
        handler_middleware=[
            create_middleware("rm1"),
            (create_middleware("rm2"), "local"),
        ],
        handlers=[
            OnMessage(
                handlers=[handler],
                handler_middleware=[create_middleware("rm3")],
            )
        ]
    )
    router.on_registration()
    await handler.handle(message)
    assert message.ctx["test"] == ["rm1", "rm3", "hm1", "hm2", "h"]


@pytest.mark.asyncio
async def test_middleware_order_parent_duplicate(message):
    middleware = create_middleware("dup")
    message.ctx["test"] = []
    handler = Handler(
        fn=create_callback("h"),
        update_type=Event.MESSAGE,
        middleware=[
            create_middleware("hm1"),
            create_middleware("hm2"),
        ],
    )
    router = OnMessage(
        handler_middleware=[
            create_middleware("rm1"),
            create_middleware("rm2"),
            middleware,
        ],
        handlers=[
            OnMessage(
                handlers=[handler],
                handler_middleware=[
                    middleware,
                    create_middleware("rm3"),
                ],
            )
        ]
    )
    router.on_registration()
    await handler.handle(message)
    assert message.ctx["test"] == [
        "rm1", "rm2", "dup", "rm3", "hm1", "hm2", "h"
    ]
