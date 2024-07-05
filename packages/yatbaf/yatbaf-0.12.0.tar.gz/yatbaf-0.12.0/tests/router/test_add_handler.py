import pytest

from yatbaf.enums import Event
from yatbaf.exceptions import BotWarning
from yatbaf.filters import Command
from yatbaf.group import OnMessage
from yatbaf.handler import Handler


def test_init_param(handler_fn):
    router = OnMessage(
        handlers=[
            handler := Handler(fn=handler_fn, update_type="message"),
        ],
    )
    assert router._handlers == [Handler(fn=handler_fn, update_type="message")]
    assert handler.parent is router


def test_add_handler_fn(handler_fn):
    router = OnMessage()
    router.add_handler(handler_fn)
    assert router._handlers == [Handler(Event.MESSAGE, fn=handler_fn)]


def test_add_handler_obj(handler_fn):
    router = OnMessage()
    router.add_handler(Handler(Event.MESSAGE, fn=handler_fn))
    assert router._handlers == [Handler(Event.MESSAGE, fn=handler_fn)]


def test_add_handler_type_error(handler_fn):
    router = OnMessage()
    handler = Handler(Event.POLL, fn=handler_fn)
    with pytest.raises(ValueError):
        router.add_handler(handler)


def test_add_handler_registered(handler_fn):
    handler = Handler(Event.MESSAGE, fn=handler_fn)
    _ = OnMessage(handlers=[handler])
    with pytest.raises(ValueError):
        OnMessage(handlers=[handler])


def test_add_handler_registered_same_router(handler_fn):
    router = OnMessage(
        handlers=[
            handler := Handler(Event.MESSAGE, fn=handler_fn),
        ]
    )
    with pytest.warns(BotWarning):
        router.add_handler(handler)
    assert router._handlers == [Handler(Event.MESSAGE, fn=handler_fn)]


def test_init_duplicate(handler_fn):
    with pytest.warns(BotWarning):
        router = OnMessage(
            handlers=[
                handler1 := Handler(Event.MESSAGE, fn=handler_fn),
                Handler(
                    fn=handler_fn,
                    update_type=Event.MESSAGE,
                    filters=[Command("foo")],
                ),
            ]
        )
    assert router._handlers == [Handler(Event.MESSAGE, fn=handler_fn)]
    assert router._handlers[0] is handler1


def test_add_handler_duplicate(handler_fn):
    router = OnMessage()
    handler1 = Handler(Event.MESSAGE, fn=handler_fn)
    handler2 = Handler(
        fn=handler_fn,
        update_type=Event.MESSAGE,
        filters=[Command("foo")],
    )
    router.add_handler(handler1)
    with pytest.warns(BotWarning):
        router.add_handler(handler2)
    assert router._handlers == [Handler(Event.MESSAGE, fn=handler_fn)]
    assert router._handlers[0] is handler1


def test_add_handler_duplicate_1(handler_fn):
    router = OnMessage()
    router.add_handler(handler_fn)
    with pytest.warns(BotWarning):
        router.add_handler(handler_fn, filters=[Command("foo")])
    assert router._handlers == [Handler(Event.MESSAGE, fn=handler_fn)]


def test_decorator_fallback():
    router = OnMessage()

    @router
    async def handler(_):  # noqa: U101
        pass

    assert router._handlers == [Handler(Event.MESSAGE, fn=handler)]


def test_decorator(guard_true):
    router = OnMessage()

    def middleware(h):

        async def w(u):
            await h(u)

        return w

    @router(
        middleware=[middleware],
        filters=[filter := Command("foo")],
        guards=[guard_true]
    )
    async def handler(_) -> None:  # noqa: U101
        pass

    assert router._handlers == [
        Handler(
            fn=handler,
            update_type=Event.MESSAGE,
            middleware=[middleware],
        )
    ]
    assert router._handlers[0]._middleware == [middleware]
    assert router._handlers[0]._filters == [filter]
    assert router._handlers[0]._guards == [guard_true]


def test_decorator_duplicate():
    router = OnMessage()

    with pytest.warns(BotWarning):

        @router
        @router(filters=[Command("foo")])
        async def handler(_):
            pass

    assert router._handlers == [Handler(Event.MESSAGE, fn=handler)]
