import pytest

from yatbaf.enums import Event
from yatbaf.filters import Command
from yatbaf.filters import User
from yatbaf.handler import Handler


@pytest.mark.asyncio
async def test_match_empty_true(handler_fn, message):
    handler = Handler(
        fn=handler_fn,
        update_type=Event.MESSAGE,
    )
    handler.on_registration()
    assert await handler.match(message)


@pytest.mark.asyncio
async def test_match_true(handler_fn, message):
    message.text = "/foo"
    handler = Handler(
        fn=handler_fn,
        update_type=Event.MESSAGE,
        filters=[Command("foo")],
    )
    handler.on_registration()
    assert await handler.match(message)


@pytest.mark.asyncio
async def test_match_true1(handler_fn, message):
    message.text = "/foo"
    handler = Handler(
        fn=handler_fn,
        update_type=Event.MESSAGE,
        filters=[
            Command("foo"),
            User(message.from_.id),
        ]
    )
    handler.on_registration()
    assert await handler.match(message)


@pytest.mark.asyncio
async def test_match_false(handler_fn, message):
    message.text = "/bar"
    handler = Handler(
        fn=handler_fn,
        update_type=Event.MESSAGE,
        filters=[Command("foo")],
    )
    handler.on_registration()
    assert not await handler.match(message)


@pytest.mark.asyncio
async def test_match_false1(handler_fn, message):
    message.text = "/foo"
    handler = Handler(
        fn=handler_fn,
        update_type=Event.MESSAGE,
        filters=[
            Command("bar"),
            User(1),
        ],
    )
    handler.on_registration()
    assert not await handler.match(message)
