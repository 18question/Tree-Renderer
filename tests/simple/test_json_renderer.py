from tree_renderer.simple.json_renderer import render


def test_scalar():
    assert str(render(42)) == "42"
    assert str(render("abc")) == "'abc'"
    assert str(render(True)) == "True"
    assert str(render(None)) == "None"


def test_empty_list():
    assert str(render([])) == "\n".join(
        (
            "[",
            "]",
        ),
    )


def test_empty_dict():
    assert str(render({})) == "\n".join(
        (
            "{",
            "}",
        ),
    )


def test_single_key():
    assert str(render({"a": 1})) == "\n".join(
        (
            "{",
            "    'a': 1",
            "}",
        ),
    )


def test_nested_dict():
    assert str(render({"a": {"b": 1}})) == "\n".join(
        (
            "{",
            "    'a': {",
            "        'b': 1",
            "    }",
            "}",
        ),
    )


def test_list_in_dict():
    assert str(render({"a": [1, 2]})) == "\n".join(
        (
            "{",
            "    'a': [",
            "        1",
            "        2",
            "    ]",
            "}",
        ),
    )


def test_dict_in_list():
    assert str(render([{"a": 1}])) == "\n".join(
        (
            "[",
            "    {",
            "        'a': 1",
            "    }",
            "]",
        ),
    )
