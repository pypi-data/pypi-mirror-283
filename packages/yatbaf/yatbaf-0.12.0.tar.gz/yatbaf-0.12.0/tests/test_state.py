import pytest

from yatbaf.state import State
from yatbaf.storage import Memory


@pytest.fixture
def storage():
    return Memory()


@pytest.mark.asyncio
async def test_set(storage):
    state = State(storage=storage)

    await state.set(1, 2, "foo")
    assert storage._data["s:1.2"] == "foo"

    await state.set(1, 2, None)
    assert storage._data.get("s:1.2") is None

    await state.set(1, 2, "bar", business_id=3)
    assert storage._data["s:1.2.3"] == "bar"


@pytest.mark.asyncio
async def test_set_data(storage):
    state = State(storage=storage)

    await state.set_data(1, 2, "foo")
    assert storage._data["d:1.2"] == "foo"

    await state.set_data(1, 2, None)
    assert storage._data.get("d:1.2") is None

    await state.set_data(1, 2, "bar", business_id=3)
    assert storage._data["d:1.2.3"] == "bar"


@pytest.mark.asyncio
async def test_get(storage):
    state = State(storage=storage)

    storage._data["s:1.2"] = "foo"
    storage._data["s:1.2.3"] = "bar"

    assert await state.get(1, 2) == "foo"
    assert await state.get(1, 2, business_id=3) == "bar"


@pytest.mark.asyncio
async def test_get_data(storage):
    state = State(storage=storage)

    storage._data["d:1.2"] = "foo"
    storage._data["d:1.2.3"] = "bar"

    assert await state.get_data(1, 2) == "foo"
    assert await state.get_data(1, 2, business_id=3) == "bar"
