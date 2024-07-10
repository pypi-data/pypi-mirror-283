import pytest

from src.html2json.parser import Html2JsonParser


def fixture_random_gen_id() -> str:
    return "000"


html_with_class_parameters = [
    ("<@000> html.main", "html.main", "main"),
    ("<@000> html.home", "html.home", "home"),
    ("<@000> html.test", "html.test", "test"),
]


@pytest.mark.parametrize("node_id,query_selector,classname", html_with_class_parameters)
def test_html_with_class(node_id, query_selector, classname):
    parser = Html2JsonParser(
        **{"store_as_list": True, "store_as_dict": False, "store_as_tree_dict": False}
    )
    parser.set_random_gen_funct(random_gen_funct=fixture_random_gen_id)
    parser.process_parser(
        html_content=f"""<html class="{classname}">Html2Json</html>"""
    )

    expected = [
        {
            "attrs": {"class": [classname]},
            "children": None,
            "content": "Html2Json",
            "node_id": node_id,
            "query_selector": query_selector,
            "tag": "html",
        }
    ]

    assert parser.as_list() == expected
