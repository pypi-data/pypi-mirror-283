import pytest

from src.html2json.parser import Html2JsonParser, ParserOptions, html2json


def fixture_random_gen_id() -> str:
    return "000"


simple_parser_parametrized_data = [
    (
        {"store_as_list": True, "store_as_dict": False, "store_as_tree_dict": False},
        {
            "as_list": [
                {
                    "attrs": {},
                    "children": None,
                    "content": "\nHtml2Json\n",
                    "node_id": "<@000> html",
                    "query_selector": "html",
                    "tag": "html",
                }
            ],
            "as_dict": None,
            "as_tree_dict": None,
            "query_selectors": ["html"],
        },
    ),
    (
        {"store_as_list": False, "store_as_dict": True, "store_as_tree_dict": False},
        {
            "as_list": None,
            "as_dict": {
                "<@000> html": {
                    "attrs": {},
                    "children": None,
                    "content": "\nHtml2Json\n",
                    "node_id": "<@000> html",
                    "query_selector": "html",
                    "tag": "html",
                }
            },
            "as_tree_dict": None,
            "query_selectors": ["html"],
        },
    ),
    (
        {"store_as_list": False, "store_as_dict": False, "store_as_tree_dict": True},
        {
            "as_list": None,
            "as_dict": None,
            "as_tree_dict": {
                "nodes": [
                    {
                        "attrs": {},
                        "children": None,
                        "content": "\nHtml2Json\n",
                        "node_id": "<@000> html",
                        "query_selector": "html",
                        "tag": "html",
                    }
                ]
            },
            "query_selectors": ["html"],
        },
    ),
    (
        {"store_as_list": False, "store_as_dict": False, "store_as_tree_dict": False},
        {
            "as_list": None,
            "as_dict": None,
            "as_tree_dict": None,
            "query_selectors": ["html"],
        },
    ),
]


@pytest.mark.parametrize("options,expected", simple_parser_parametrized_data)
def test_simple_parser(options, expected):
    input_html = """
<!Doctype>
<html>
Html2Json
</html>
    """

    output = html2json(
        input_path=input_html,
        options=ParserOptions.parser_factory(**options),
        random_gen_funct=fixture_random_gen_id,
    )

    assert output == expected


def test_random_override_function():
    parser = Html2JsonParser(**ParserOptions.parser_factory().as_dict())

    parser.set_random_gen_funct(random_gen_funct=fixture_random_gen_id)

    expected = "000"

    assert parser.random_node_id == expected


def test_random_id_gen():
    parser = Html2JsonParser(**ParserOptions.parser_factory().as_dict())
    not_expected = "0"
    assert not parser.random_node_id == not_expected


def test_html_with_class_and_id():
    pass
