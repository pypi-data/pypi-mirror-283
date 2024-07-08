
# RegexParser

## Installation for both xpath, regex parsers

```bash
pip install cd-parser
```
## update
```bash
pip install -U cd-parser
```

# all examples in the examples folder

A utility class for commonly used regex operations in Python.

## Features

- **Replace**: Easily replace occurrences of a regex pattern with a new string.
- **Find All**: Retrieve all occurrences of a regex pattern in a string.
- **Find First**: Get the first occurrence of a regex pattern in a string.
- **Find Before**: Extract the portion of text immediately before a given substring.
- **Find After**: Fetch the portion of text immediately after a given substring.
- **Find Between**: Find text between two specified substrings.
- **Is Match**: Check if the input text matches a given regex pattern from the start.
- **Split**: Divide the input text using a provided regex pattern.

## Usage

Here are some example usages of the `RegexParser` class:

```python
from cd_parser import regex


# Replace text
modified_text = regex.replace("old", "new", "This is an old text.")
print(modified_text)  # Output: "This is a new text."

# Find all matches
matches = regex.find_all("[A-Za-z]+", "123 apple 456 banana")
print(matches)  # Output: ['apple', 'banana']

# ... [You can add more examples for other methods]
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)


Absolutely. Here's a README.md file for the `XpathParser` class:

---

# XpathParser

A simple and lightweight XPath parser class for extracting data from HTML/XML content. Built on top of the `lxml` library, it offers a variety of methods for precise element extraction based on various criteria.

## Features
- Fetch multiple elements or a single element using a custom XPath query.
- Predefined methods for common XPath queries like selecting by tag, attribute, text, etc.
- Simple, user-friendly, and Pythonic API.



## Usage

### Initialization
Create an instance of the `XpathParser` class with your HTML/XML content:

```python
from cd_parser import XpathParser

doc_text = """
<html>
    <body>
        <a id="link1" href="https://example.com/page1">Link 1</a>
        <a id="link2" href="https://example.com/page2">Link 2</a>
    </body>
</html>
"""

parser = XpathParser(doc_text)
```

### Fetch Elements

Using custom XPath:
```python
links = parser.get_elements('//a')
print([link.text for link in links])
```

Get a single element (the first match):
```python
single_link = parser.get_element('//*[@id="link1"]')
if single_link:
    print(single_link.text)
```

### Predefined Queries

Select all nodes:
```python
all_nodes = parser.select_all_nodes()
```

Select by tag:
```python
anchors = parser.select_by_tag("a")
```

Select by attribute:
```python
divs_with_class = parser.select_by_class("div", "my-class")
```

... and many more. Refer to the class docstrings for details on each method.

## Clipboard

```python
from cd_parser import clipboard as cb

text = cb.copy("text you want to copy")

print(cb.paste())

```

## Contributing
Feel free to fork the repository, make your changes, and submit pull requests. We appreciate all contributions!



Please note:
1. The filename `xpath_parser.py` is assumed in the usage example. Adjust it accordingly if you're using a different filename.
2. Modify sections like "Contributing" as per your actual project needs and repository policies. This is a generic template to help you get started.

# All examples in examples folder


License

MIT License

More documentation at:
[Code Docta](https://codedocta.com "Code Docta")
