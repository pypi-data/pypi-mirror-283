import pytest

from yatbaf.exceptions import BotWarning
from yatbaf.exceptions import FrozenInstanceError
from yatbaf.group import OnMessage
from yatbaf.group import OnPoll
from yatbaf.handler import Handler


def test_init():
    router = OnMessage(handlers=[nested := OnMessage()])
    assert router._handlers == [nested]
    assert nested.parent is router


def test_add_router():
    router = OnMessage()
    nested = OnMessage()
    router.add_handler(nested)
    assert router._handlers == [nested]
    assert nested.parent is router


def test_add_router_self():
    router = OnMessage()
    with pytest.raises(ValueError):
        router.add_handler(router)


def test_add_router_wrong_type():
    router = OnMessage()
    with pytest.raises(ValueError):
        router.add_handler(OnPoll())


def test_add_router_registered():
    _ = OnMessage(
        handlers=[
            nested := OnMessage(),
        ],
    )
    router2 = OnMessage()
    with pytest.raises(ValueError):
        router2.add_handler(nested)


def test_add_router_duplicate_same_obj():
    router = OnMessage(
        handlers=[
            nested := OnMessage(),
        ],
    )
    with pytest.warns(BotWarning):
        router.add_handler(nested)
    assert router._handlers == [nested]


def test_add_router_duplicate_equal_obj():

    async def fn(_):
        pass

    router = OnMessage(
        handlers=[  # yapf: disable
            nested := OnMessage(
                handlers=[
                    Handler(
                        fn=fn,
                        update_type="message",
                    ),
                ],
            ),
        ]
    )
    dup = OnMessage(handlers=[Handler(fn=fn, update_type="message")])
    with pytest.warns(BotWarning):
        router.add_handler(dup)
    assert router._handlers == [nested]


def test_add_router_frozen():
    router = OnMessage()
    router.on_registration()
    with pytest.raises(FrozenInstanceError):
        router.add_handler(OnMessage())
