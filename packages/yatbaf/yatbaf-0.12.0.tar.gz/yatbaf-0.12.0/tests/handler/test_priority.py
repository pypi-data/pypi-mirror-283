import pytest

from yatbaf import filters as f
from yatbaf.handler import Handler


class Filter(f.BaseFilter):
    priority = 100

    async def check(self, _):
        pass


@pytest.mark.parametrize(
    "filters,priority",
    [
        [
            [f.Command("foo")],
            ((1, (1000, 1000)), (0, (0, 0)), (0, (0, 0))),
        ],
        [
            [f.Command("foo") | f.Text(startswith="foo")],
            ((2, (1000, 150)), (0, (0, 0)), (0, (0, 0))),
        ],
        [
            [f.Command("foo"), f.Chat("private")],
            ((1, (1000, 1000)), (0, (0, 0)), (1, (100, 100))),
        ],
        [
            [f.Command("foo"), f.User(1), f.Chat("private")],
            ((1, (1000, 1000)), (1, (100, 100)), (1, (100, 100))),
        ],
        [
            [f.Command("foo", "bar"), f.User(1), f.Chat("private")],
            ((2, (1000, 1000)), (1, (100, 100)), (1, (100, 100))),
        ],
        [
            [f.Command("foo", "bar"), f.User(1), f.Chat("group"), f.ChatId(1)],
            ((2, (1000, 1000)), (1, (100, 100)), (2, (150, 100))),
        ],
        [
            [Filter()],
            ((1, (100, 100)), (0, (0, 0)), (0, (0, 0))),
        ],
    ],
)
def test_priority(filters, priority):
    assert Handler._parse_priority(filters) == priority
