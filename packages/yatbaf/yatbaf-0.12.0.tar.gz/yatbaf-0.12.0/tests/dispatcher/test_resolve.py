import pytest

from yatbaf.dispatcher import Dispatcher
from yatbaf.group import OnMessage
from yatbaf.group import OnPoll
from yatbaf.handler import Handler


@pytest.mark.asyncio
async def test_resolve(handler_fn, update, mock_mark):
    router = OnMessage(handlers=[Handler(fn=handler_fn, update_type="message")])
    router.on_registration()

    dispatcher = Dispatcher(handlers={"message": router})
    await dispatcher.resolve(update)
    mock_mark.assert_called_once_with(update.event)


@pytest.mark.asyncio
async def test_resolve_none(handler_fn, update, mock_mark):
    dispatcher = Dispatcher(
        handlers={
            "poll": OnPoll(
                handlers=[
                    Handler(
                        fn=handler_fn,
                        update_type="poll",
                    ),
                ],
            ),
        }
    )
    await dispatcher.resolve(update)
    mock_mark.assert_not_called()
