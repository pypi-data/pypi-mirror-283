# HTML Serializer Parser


Based on html-to-json library [https://pypi.org/project/html-to-json/](https://pypi.org/project/html-to-json/) this
library extends its functionality adding an additional layer for extra information
like: query selector for every node, list of all query selectors, different return
options, by list, by tree dictionary and/or by dict, if adds an specific property
for every node

# Quick Start

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
    # Will retrieve a dict with following keys
    # as_list, as_dict, as_tree_dict, query_selectors
    json_output = json.dumps(output, ensure_ascii=True, indent=2)
    with open("data.json", "w") as o:
        o.write(json_output)
```

# Some code examples

## Extracting query selectors

```python
from html2json.parser import ParserOptions, html2json
VALID_SCRAPPING_SITE = "https://www.scrapethissite.com/pages/simple/"

def get_query_selectors():
    output = html2json(
        input_path=VALID_SCRAPPING_SITE,
        options=ParserOptions.parser_factory(False, False, False),
        raw_content=False,
    )
    print(output['query_selectors'])

get_query_selectors()
```

## Let's create a block using the internal logic

If you wanna go deeper, maybe you want to build the logic by yourself replicating
the functionality of ```html2json```function

```python
import requests
from bs4 import BeautifulSoup
from html2json.parser import ParserOptions, Html2JsonParser
VALID_SCRAPPING_SITE = "https://www.scrapethissite.com/pages/simple/"

def step_by_step_usage():
    # We get the HTML content using Requests
    html_content = requests.get(VALID_SCRAPPING_SITE).content
    # We instantiate a BeautifulSoup object using the content
    soup_instance = BeautifulSoup(html_content, 'html.parser')
    # We get a Html2JsonParser instance, prepared to return the
    # data in a List, injecting a BeautifulSoup instance
    parser = Html2JsonParser(
        soup_instance=soup_instance,
        **ParserOptions.parser_factory(
            store_as_list=True,
            store_as_dict=False,
            store_as_tree_dict=False
        ).as_dict()
    )
    # We have to tell the parser that we want to process the information
    # if you don't call this method, the content won't be processed
    parser.process_parser()

    # We extract the query selectors that we collected before
    query_selectors = parser.query_selectors
    # We extract the list of all the nodes that we collected before
    process_list = parser.as_list()

    # We return the data
    return query_selectors, process_list

# Using the Jupyter blocks we will show the 5 first nodes that we collected before
_, process_list = step_by_step_usage()
print(process_list[:5])
```

## Let's use the library in a real case using Pandas

In this example we will extract the information with the library, load the dictionary
into a Pandas dataframe, apply some filters, and then store the information in CSV format

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
from html2json.parser import ParserOptions, Html2JsonParser
VALID_SCRAPPING_SITE = "https://www.scrapethissite.com/pages/simple/"

def get_pandas_info():
    # We get the HTML content using Requests
    html_content = requests.get(VALID_SCRAPPING_SITE).content
    # We instantiate a BeautifulSoup object using the content
    soup_instance = BeautifulSoup(html_content, 'html.parser')
    # We get a Html2JsonParser instance, prepared to return the
    # data in a List, injecting a BeautifulSoup instance
    parser = Html2JsonParser(
        soup_instance=soup_instance,
        **ParserOptions.parser_factory(
            store_as_list=True,
            store_as_dict=False,
            store_as_tree_dict=False
        ).as_dict()
    )
    # We have to tell the parser that we want to process the information
    # if you don't call this method, the content won't be processed
    parser.process_parser()

    # We extract the list of all the nodes that we collected before
    process_list = parser.as_list()

    # Based on the process list we build a Pandas DataFrame
    df = pd.DataFrame(process_list)

    # We know that, all the information that we want, is in an h3 tag
    # we will apply a filter just for having all the information that
    # we really want
    df = df[df['tag'] == 'h3']

    # We are going to reduce the columns that we really want
    # we obtain from the JSON: node_id, tag, children, attrs, query_selector
    # and content. we will store only node_id, tag and content
    df = df[['node_id', 'tag', 'content']]

    # We will return the generated CSV using Pandas method
    return df.to_csv()

csv_data = get_pandas_info()
print(csv_data)
```

# Changelog
- 0.0.3
  - Modified internal logic for allowing dependency injection
  - If a BeautifulSoup object is injected html_content is not required
  - If a BeautifulSoup object is injected library won't analyze html_content because is None
  - If a BeautifulSoup object is not injected and html_content is not provided it will raise an ```Html2JsonEmptyBody``` exception


# TODOS
- Improve Readme to be easier to understand
- Improve abstractions in order to be easier to modify specific steps
- Add docstrings
- Include more tests
- Avoid repeating node content extending ```bs4.element.Tag``` class
