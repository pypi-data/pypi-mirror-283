import pytest

from yatbaf.di import Provide
from yatbaf.group import OnCallbackQuery
from yatbaf.group import OnMessage
from yatbaf.group import OnPoll
from yatbaf.group import parse_handlers
from yatbaf.handler import on_business_connection
from yatbaf.handler import on_business_message
from yatbaf.handler import on_callback_query
from yatbaf.handler import on_channel_post
from yatbaf.handler import on_chat_boost
from yatbaf.handler import on_chat_join_request
from yatbaf.handler import on_chat_member
from yatbaf.handler import on_chosen_inline_result
from yatbaf.handler import on_deleted_business_messages
from yatbaf.handler import on_edited_business_message
from yatbaf.handler import on_edited_channel_post
from yatbaf.handler import on_edited_message
from yatbaf.handler import on_inline_query
from yatbaf.handler import on_message
from yatbaf.handler import on_message_reaction
from yatbaf.handler import on_message_reaction_count
from yatbaf.handler import on_my_chat_member
from yatbaf.handler import on_poll
from yatbaf.handler import on_poll_answer
from yatbaf.handler import on_pre_checkout_query
from yatbaf.handler import on_removed_chat_boost
from yatbaf.handler import on_shipping_query


async def fn(_):
    pass


@pytest.mark.parametrize(
    "handler,exp",
    [
        [
            on_message(fn),
            {
                "message": on_message(fn)
            },
        ],
        [
            on_edited_message(fn),
            {
                "edited_message": on_edited_message(fn)
            },
        ],
        [
            on_channel_post(fn),
            {
                "channel_post": on_channel_post(fn)
            },
        ],
        [
            on_edited_channel_post(fn),
            {
                "edited_channel_post": on_edited_channel_post(fn)
            },
        ],
        [
            on_inline_query(fn),
            {
                "inline_query": on_inline_query(fn)
            },
        ],
        [
            on_chosen_inline_result(fn),
            {
                "chosen_inline_result": on_chosen_inline_result(fn)
            },
        ],
        [
            on_callback_query(fn),
            {
                "callback_query": on_callback_query(fn)
            },
        ],
        [
            on_shipping_query(fn),
            {
                "shipping_query": on_shipping_query(fn),
            },
        ],
        [
            on_pre_checkout_query(fn),
            {
                "pre_checkout_query": on_pre_checkout_query(fn),
            },
        ],
        [
            on_poll(fn),
            {
                "poll": on_poll(fn),
            },
        ],
        [
            on_poll_answer(fn),
            {
                "poll_answer": on_poll_answer(fn)
            },
        ],
        [
            on_my_chat_member(fn),
            {
                "my_chat_member": on_my_chat_member(fn)
            },
        ],
        [
            on_chat_member(fn),
            {
                "chat_member": on_chat_member(fn),
            },
        ],
        [
            on_chat_join_request(fn),
            {
                "chat_join_request": on_chat_join_request(fn)
            },
        ],
        [
            on_message_reaction(fn),
            {
                "message_reaction": on_message_reaction(fn)
            },
        ],
        [
            on_message_reaction_count(fn),
            {
                "message_reaction_count": on_message_reaction_count(fn)
            },
        ],
        [
            on_chat_boost(fn),
            {
                "chat_boost": on_chat_boost(fn)
            },
        ],
        [
            on_removed_chat_boost(fn),
            {
                "removed_chat_boost": on_removed_chat_boost(fn)
            },
        ],
        [
            on_business_connection(fn),
            {
                "business_connection": on_business_connection(fn)
            },
        ],
        [
            on_business_message(fn),
            {
                "business_message": on_business_message(fn)
            },
        ],
        [
            on_edited_business_message(fn),
            {
                "edited_business_message": on_edited_business_message(fn)
            },
        ],
        [
            on_deleted_business_messages(fn),
            {
                "deleted_business_messages": on_deleted_business_messages(fn)
            },
        ],
    ]
)
def test_parse(handler, exp):
    assert parse_handlers(handlers=[handler]) == exp


def test_one_router(handler_fn):
    router = OnMessage(handlers=[on_message(handler_fn)])
    result = parse_handlers(handlers=[router])
    assert result == {"message": router}
    assert result["message"] is router


def test_routers(handler_fn):
    result = parse_handlers(
        handlers=[
            OnMessage(),
            OnMessage(handlers=[on_message(handler_fn)]),
            OnPoll(handlers=[on_poll(handler_fn)]),
            OnCallbackQuery(handlers=[on_callback_query(handler_fn)])
        ]
    )
    assert result == {
        "message": OnMessage(
            handlers=[
                OnMessage(),
                OnMessage(handlers=[on_message(handler_fn)]),
            ],
        ),
        "callback_query": OnCallbackQuery(
            handlers=[on_callback_query(handler_fn)]
        ),
        "poll": OnPoll(handlers=[on_poll(handler_fn)]),
    }


def test_handlers_routers(handler_fn):
    result = parse_handlers(
        handlers=[
            on_poll(handler_fn),
            on_message(handler_fn),
            on_callback_query(handler_fn),
            OnMessage(handlers=[on_message(handler_fn)]),
            OnCallbackQuery(handlers=[on_callback_query(handler_fn)]),
        ],
    )
    assert result == {
        "message": OnMessage(
            handlers=[
                on_message(handler_fn),
                OnMessage(handlers=[on_message(handler_fn)])
            ],
        ),
        "poll": on_poll(handler_fn),
        "callback_query": OnCallbackQuery(
            handlers=[
                on_callback_query(handler_fn),
                OnCallbackQuery(handlers=[on_callback_query(handler_fn)]),
            ]
        ),
    }


async def provide_data1():
    return 1


async def provide_data2():
    return 2


@pytest.mark.parametrize(
    "gd,rd,exp",
    [  # yapf: disable
        [{}, {}, {}],
        [
            {"data1": Provide(provide_data1)},
            {},
            {"data1": Provide(provide_data1)},
        ],
        [
            {},
            {"data1": Provide(provide_data1)},
            {"data1": Provide(provide_data1)},
        ],
        [
            {"data1": Provide(provide_data1)},
            {"data1": Provide(provide_data2)},
            {"data1": Provide(provide_data2)},
        ],
        [
            {"data1": Provide(provide_data1)},
            {"data2": Provide(provide_data2)},
            {
                "data1": Provide(provide_data1),
                "data2": Provide(provide_data2),
            },
        ],
    ]
)
def test_deps_one_router_merge(gd, rd, exp):
    router = OnMessage(dependencies=rd)
    result = parse_handlers(handlers=[router], dependencies=gd)
    assert result == {"message": OnMessage(dependencies=exp)}


def test_deps_handler(handler_fn):
    dependencies = {"data": Provide(provide_data1)}
    result = parse_handlers(
        handlers=[on_message(handler_fn)],
        dependencies=dependencies,
    )
    assert result == {
        "message": on_message(
            handler_fn,
            dependencies=dependencies,
        )
    }


def test_deps_routers():
    router1 = OnMessage(dependencies={"data1": Provide(provide_data1)})
    router2 = OnMessage(dependencies={"data2": Provide(provide_data2)})
    router3 = OnCallbackQuery()
    result = parse_handlers(
        handlers=[router1, router2, router3],
        dependencies={"data1": Provide(provide_data1)}
    )
    assert result == {
        "message": OnMessage(
            handlers=[
                OnMessage(dependencies={"data1": Provide(provide_data1)}),
                OnMessage(dependencies={"data2": Provide(provide_data2)}),
            ],
            dependencies={"data1": Provide(provide_data1)},
        ),
        "callback_query": OnCallbackQuery(
            dependencies={"data1": Provide(provide_data1)},
        )
    }
