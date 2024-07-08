# HTML Serializer Parser


Based on html-to-json library [https://pypi.org/project/html-to-json/](https://pypi.org/project/html-to-json/) this
library extends its functionality adding an additional layer for extra information
like: query selector for every node, list of all query selectors, different return
options, by list, by tree dictionary and/or by dict, if adds an specific property
for every node

# How to run it

```python
import json
from html2json.parser import ParserOptions, html2json


if __name__ == "__main__":
    # You can use an HTML file, raw HTML String or and endpoint
    FILE_DIR = "./PATH_TO_YOUR_FILES/index.html"
    output = html2json(
        input_path=open(FILE_DIR).read(),
        options=ParserOptions.parser_factory(
            store_as_list=True,
            store_as_dict=True,
            store_as_tree_dict=True
        ),
        raw_content=False,
    )
    # Will retrieve a dict with follwing keys
    # as_list, as_dict, as_tree_dict, query_selectors
    json_output = json.dumps(output, ensure_ascii=True, indent=2)
    with open("data.json", "w") as o:
        o.write(json_output)
```

# TODOS
- Improve Readme
- Add docstrings
- Include more tests
