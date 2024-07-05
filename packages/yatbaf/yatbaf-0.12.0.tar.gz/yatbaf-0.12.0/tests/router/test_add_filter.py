from yatbaf import OnMessage
from yatbaf import filters as f


def test_add_filter():
    router = OnMessage()
    assert router._filters == []
    filter = f.User(123)
    router.add_filter(filter)
    assert router._filters == [filter]
