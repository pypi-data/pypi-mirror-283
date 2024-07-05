from yatbaf.types import Update


def test_ctx_empty():
    obj = Update(update_id=1)
    assert obj.__usrctx__ == {"ctx": {}}
    assert not obj.ctx


def test_ctx():
    obj = Update(update_id=1)
    obj.ctx["foo"] = "bar"
    assert "foo" in obj.__usrctx__["ctx"]
    assert obj.__usrctx__["ctx"]["foo"] == "bar"
