import pytest

from yatbaf.filters import Command
from yatbaf.filters import text
from yatbaf.group import OnMessage
from yatbaf.handler import on_message


@pytest.fixture(autouse=True)
def __reset_update(message):
    message.ctx["test"] = []


def create_handler(mark, filters=None):

    @on_message(filters=filters)
    async def handler(update):
        update.ctx["test"].append(mark)

    return handler


@pytest.mark.asyncio
async def test_fallback(message):
    router = OnMessage(handlers=[create_handler("f")])
    router.on_registration()

    await router.handle(message)
    assert message.ctx["test"] == ["f"]


@pytest.mark.asyncio
async def test_resolve_filters(message):
    router = OnMessage(
        handlers=[
            create_handler("f"),
            create_handler("foo", filters=[Command("foo")]),
        ]
    )
    router.on_registration()
    message.text = "/foo"

    await router.handle(message)
    assert message.ctx["test"] == ["foo"]


@pytest.mark.asyncio
async def test_resolve_stop_propagate(message):
    router = OnMessage(
        handlers=[
            create_handler("foo", filters=[Command("foo")]),
            create_handler("foo1", filters=[Command("foo")]),
            OnMessage(
                handlers=[create_handler("foo2", filters=[Command("foo")])],
            ),
        ],
    )
    router.on_registration()
    message.text = "/foo"

    await router.handle(message)
    assert message.ctx["test"] == ["foo"]


@pytest.mark.asyncio
async def test_resolve_nested_vert(message):
    router = OnMessage(
        handlers=[
            create_handler("bar1", filters=[Command("bar")]),
            OnMessage(
                handlers=[
                    create_handler("bar2", filters=[Command("bar")]),
                    OnMessage(
                        handlers=[
                            create_handler("foo", filters=[Command("foo")]),
                            OnMessage(
                                handlers=[
                                    create_handler(
                                        "bar3", filters=[Command("bar")]
                                    ),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
    router.on_registration()
    message.text = "/foo"

    await router.handle(message)
    assert message.ctx["test"] == ["foo"]


@pytest.mark.asyncio
async def test_resolve_nested_horiz(message):
    router = OnMessage(
        handlers=[
            OnMessage(
                handlers=[
                    create_handler("foo", filters=[Command("foo")]),
                ]
            ),
            OnMessage(
                handlers=[
                    create_handler("bar", filters=[Command("bar")]),
                ]
            ),
            OnMessage(
                handlers=[
                    create_handler("foo1", filters=[Command("foo")]),
                ]
            ),
        ],
    )
    router.on_registration()
    message.text = "/foo"

    await router.handle(message)
    assert message.ctx["test"] == ["foo"]


@pytest.mark.asyncio
async def test_stop_propagate_true_param(message, handler_fn, mock_mark):
    router = OnMessage(
        handlers=[
            OnMessage(stop_propagate=True),
            OnMessage(handlers=[on_message(handler_fn)]),
        ],
    )
    router.on_registration()
    await router.handle(message)
    mock_mark.assert_not_called()


@pytest.mark.asyncio
async def test_stop_propagate_true_filter(message, handler_fn, mock_mark):
    router = OnMessage(
        handlers=[
            OnMessage(filters=[text]),
            OnMessage(handlers=[on_message(handler_fn)]),
        ],
    )
    router.on_registration()
    message.text = "foo"
    await router.handle(message)
    mock_mark.assert_not_called()


@pytest.mark.asyncio
async def test_stop_propagate_true_filter_guard(
    message, handler_fn, mock_mark, guard_false
):
    router = OnMessage(
        handlers=[
            OnMessage(filters=[text], guards=[guard_false]),
            OnMessage(handlers=[on_message(handler_fn)]),
        ],
    )
    router.on_registration()
    message.text = "foo"
    await router.handle(message)
    mock_mark.assert_not_called()


@pytest.mark.asyncio
async def test_stop_propagate_false_filter(message, handler_fn, mock_mark):
    router = OnMessage(
        handlers=[
            OnMessage(filters=[text], stop_propagate=False),
            OnMessage(handlers=[on_message(handler_fn)]),
        ],
    )
    router.on_registration()
    message.text = "foo"
    await router.handle(message)
    mock_mark.assert_called_once()
