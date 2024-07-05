from yatbaf import filters as f
from yatbaf.group import OnMessage
from yatbaf.handler import Handler
from yatbaf.handler import on_message


def test_fallback():

    @on_message
    async def any_message(_):
        pass

    @on_message(filters=[f.Command("foo"), f.Chat("private")])
    async def foo_private(_):
        pass

    @on_message(filters=[f.Command("foo")])
    async def foo_any(_):
        pass

    router = OnMessage(handlers=[
        any_message,
        foo_any,
        foo_private,
    ])

    assert router._handlers == [
        any_message,
        foo_any,
        foo_private,
    ]

    router.on_registration()
    assert router._handlers == [
        foo_private,
        foo_any,
        any_message,
    ]


def test_handler_group(handler_fn):
    nested_group = OnMessage()
    handler = Handler(fn=handler_fn, update_type="message")
    hg = OnMessage(handlers=[handler, nested_group])
    hg.on_registration()
    assert hg._handlers == [handler, nested_group]


def test_handler_group_filters(handler_fn):
    nested_group = OnMessage(filters=[f.User(123)])
    handler = Handler(fn=handler_fn, update_type="message")
    hg = OnMessage(handlers=[handler, nested_group])
    hg.on_registration()
    assert hg._handlers == [nested_group, handler]
