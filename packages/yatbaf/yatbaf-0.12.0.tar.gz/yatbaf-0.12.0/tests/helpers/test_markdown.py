import pytest

from yatbaf.helpers import md


@pytest.mark.parametrize(
    "text,expect",
    (
        ("foo", "foo"),
        ("foo.", "foo\\."),
        ("*foo*.", "\\*foo\\*\\."),
        ("_*foo__.", "\\_\\*foo\\_\\_\\."),
        ("__foo__", "\\_\\_foo\\_\\_"),
        ("!foo__.", "\\!foo\\_\\_\\."),
        ("foo != bar", "foo \\!\\= bar"),
        ("foo|bar", "foo\\|bar"),
        ("foo {} bar", "foo \\{\\} bar"),
        ("foo > bar", "foo \\> bar"),
        ("#!/usr/foo/bar -baz", "\\#\\!/usr/foo/bar \\-baz"),
        ("#![!_foo(~bar_)`].", "\\#\\!\\[\\!\\_foo\\(\\~bar\\_\\)\\`\\]\\."),
    )
)
def test_markdown_escape(text, expect):
    assert (result := md.escape(text)) == expect, result


@pytest.mark.parametrize(
    "text,expect", (
        ("foo", "foo"),
        ("foo {}", "foo {}"),
        ("foo {0}", "foo {0}"),
    )
)
def test_markdown_escape_fstring(text, expect):
    assert (result := md.escape_f(text)) == expect, result
    assert result.format(s := "bar") == expect.format(s)


@pytest.mark.parametrize(
    "text,expect",
    (
        ("foo", "foo"),
        ("`foo`", "\\`foo\\`"),
        ("``\\foo\\``", "\\`\\`\\\\foo\\\\\\`\\`"),
    )
)
def test_markdown_escape_code_pre(text, expect):
    assert md.escape_code(text) == expect
    assert md.escape_code(text) == expect


@pytest.mark.parametrize(
    "text,expect",
    (
        ("foo", "foo"),
        ("http://foo.bar?q=(\\baz)", "http://foo.bar?q=(\\\\baz\\)"),
        ("http://foo.bar?q=\\))\\!baz", "http://foo.bar?q=\\\\\\)\\)\\\\!baz"),
    )
)
def test_markdown_escape_link_emoji(text, expect):
    assert md.escape_link(text) == expect
    assert md.escape_link(text) == expect


def test_markdown_bold():
    assert md.bold("bold") == "*bold*"


def test_markdown_italic():
    assert md.italic("italic") == "_italic_"


def test_markdown_underline():
    assert md.underline("underline") == "__underline__"


def test_markdown_strikethrough():
    assert md.strikethrough("strikethrough") == "~strikethrough~"


def test_markdown_spoiler():
    assert md.spoiler("spoiler") == "||spoiler||"


def test_markdown_url():
    assert (
        md.url("url title", "https://foo.bar") == "[url title](https://foo.bar)"
    )


def test_markdown_mention():
    assert md.mention("user", 1234) == "[user](tg://user?id=1234)"


def test_markdown_emoji():
    assert md.emoji(1234, "emoji") == "![emoji](tg://emoji?id=1234)"


def test_markdown_inline():
    assert md.inline("foo") == "`foo`"


def test_markdown_code():
    assert md.code("print('foo')") == "```\nprint('foo')\n```"
    assert md.code("print('foo')", "python") == "```python\nprint('foo')\n```"
