from __future__ import annotations

import random
import re
from typing import Any, Dict, List, Set

import attr
import bs4
import requests


class BeautifulSoupParserEnum:
    _class_types: Dict[str, Any] = {
        "doctype": bs4.element.Doctype,
        "tag": bs4.element.Tag,
        "navigable_string": bs4.element.NavigableString,
    }

    @property
    def VALID_CHILDREN_CLASS(self):
        return [self._class_types["tag"]]

    @property
    def VALID_TEXT_NODE_CLASS(self):
        return [self._class_types["navigable_string"]]


class Html2JsonParser:
    _store_as_list: bool = False
    _store_as_dict: bool = False
    _store_as_tree_dict: bool = False
    _store_list: List[Dict[str, Any]] = []
    _store_dict: Dict[str, Any] = {}
    _store_tree_dict: Dict[str, Any] = {}
    _query_selectors: Set[str] = set()
    _override_random_id: bool = False
    _random_id_funct: callable = None

    def __init__(
        self,
        store_as_list: bool = False,
        store_as_dict: bool = False,
        store_as_tree_dict: bool = False,
    ):
        self._store_as_list = store_as_list
        self._store_as_dict = store_as_dict
        self._store_as_tree_dict = store_as_tree_dict

    def set_random_gen_funct(self, random_gen_funct: callable) -> None:
        self._random_id_funct = random_gen_funct
        self._override_random_id = True

    @property
    def bs4_handler(self) -> str:
        # FIXME add html5lib
        return "html.parser"

    def _random_generator(self) -> str:
        if self._override_random_id and self._random_id_funct:
            return self._random_id_funct()

        return "{d1}{d2}{d3}".format(
            d1=random.randint(0, 9), d2=random.randint(0, 9), d3=random.randint(0, 9)
        )

    @property
    def random_node_id(self) -> str:
        return self._random_generator()

    def parse_node(
        self,
        page_element: bs4.element.PageElement,
        base_query_selector: str,
        raw_content: bool = False,
    ) -> Dict[str, Any] | None:
        empty = len(page_element.text.strip()) == 0
        if empty and not page_element.name:
            return None

        explicit_query_selector = page_element.name
        text_only = (
            page_element.__class__ in BeautifulSoupParserEnum().VALID_TEXT_NODE_CLASS
        )
        valid_children = (
            page_element.__class__ in BeautifulSoupParserEnum().VALID_CHILDREN_CLASS
        )

        try:
            attrs = page_element.attrs
            if attrs.get("id"):
                explicit_query_selector = f"{explicit_query_selector}#{attrs.get('id')}"
            elif attrs.get("class"):
                explicit_query_selector = (
                    f"{explicit_query_selector}.{'.'.join(attrs.get('class'))}"
                )
            # TODO: Consider adding dataset for making better
        except AttributeError:
            attrs = {}

        if not page_element.name:
            # Yes it also can be None
            query_selector = explicit_query_selector
        else:
            query_selector = "{base_query_selector}{query_selector}".format(
                base_query_selector=base_query_selector + " > "
                if base_query_selector and base_query_selector != page_element.name
                else "",
                query_selector=explicit_query_selector,
            )

            self._query_selectors.add(query_selector)

        children = []
        if valid_children and not text_only:
            for n in page_element.children:
                if n.__class__ not in BeautifulSoupParserEnum().VALID_TEXT_NODE_CLASS:
                    res = self.parse_node(n, query_selector, raw_content)
                    if res:
                        if self._store_as_tree_dict:
                            children.append(res)

        node_dict = {
            "node_id": f"<@{self.random_node_id}> {query_selector}",
            "tag": page_element.name,
            "children": children if len(children) > 0 else None,
            "attrs": attrs,
            "query_selector": query_selector,
            "content": page_element.text,
        }

        if raw_content:
            node_dict["raw_content"] = str(page_element)
        if self._store_as_dict:
            self._store_dict[node_dict["node_id"]] = node_dict
        if self._store_as_list:
            self._store_list.append(node_dict)
        if not self._store_as_tree_dict:
            pass
        return node_dict

    def _parse_html_file(self, html_content: str, raw_content: bool = False) -> None:
        external_dict = {"nodes": []}
        soup = bs4.BeautifulSoup(html_content, self.bs4_handler)
        for node in soup:
            query_selector = node.name
            node_result = self.parse_node(node, query_selector, raw_content)
            if node_result:
                self._query_selectors.add(query_selector)

                external_dict["nodes"].append(node_result)

        if self._store_as_tree_dict:
            self._store_tree_dict = external_dict

    def process_parser(self, html_content: str, raw_content: bool = False) -> None:
        self._store_list: List[Dict[str, Any]] = []
        self._store_dict: Dict[str, Any] = {}
        self._store_tree_dict: Dict[str, Any] = {}
        self._query_selectors: Set[str] = set()
        self._parse_html_file(html_content, raw_content)

    def return_data(self) -> Dict[str, Any] | List[Any] | None:
        if self._store_as_tree_dict:
            return self._store_tree_dict
        elif self._store_as_dict:
            return self._store_dict
        elif self._store_as_list:
            return self._store_list

    def as_dict(self) -> Dict[str, Any] | None:
        if self._store_as_dict:
            return self._store_dict

    def as_list(self) -> List[Any] | None:
        if self._store_as_list:
            return self._store_list

    def as_tree_dict(self) -> Dict[str, Any] | None:
        if self._store_as_tree_dict:
            return self._store_tree_dict

    @property
    def query_selectors(self) -> List[str]:
        query_selectors = list(self._query_selectors)
        query_selectors.sort()
        return query_selectors


@attr.s(auto_attribs=True)
class ParserOptions:
    store_as_list: bool = False
    store_as_dict: bool = False
    store_as_tree_dict: bool = False

    def as_dict(self) -> Dict[str, bool]:
        return attr.asdict(self)

    @classmethod
    def parser_factory(
        cls,
        store_as_list: bool = False,
        store_as_dict: bool = False,
        store_as_tree_dict: bool = False,
    ) -> ParserOptions:
        return cls(
            store_as_list=store_as_list,
            store_as_dict=store_as_dict,
            store_as_tree_dict=store_as_tree_dict,
        )


def html2json(
    input_path: str,
    options: ParserOptions,
    raw_content: bool = False,
    random_gen_funct: callable = None,
) -> Dict[str, Any] | List[Any]:
    parser = Html2JsonParser(**options.as_dict())
    if random_gen_funct:
        parser.set_random_gen_funct(random_gen_funct)

    url_regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    path_regex = re.compile(r"^[/|.]+.*.\w$")
    # If it is not a URL or a path, it only allows HTML like files
    process_content = input_path
    if url_regex.match(input_path):
        # Is a URL
        process_content = requests.get(input_path).content
    elif path_regex.match(input_path):
        # Is a path
        process_content = open(input_path).read()
    parser.process_parser(process_content, raw_content)

    return {
        "as_list": parser.as_list(),
        "as_dict": parser.as_dict(),
        "as_tree_dict": parser.as_tree_dict(),
        "query_selectors": parser.query_selectors,
    }
