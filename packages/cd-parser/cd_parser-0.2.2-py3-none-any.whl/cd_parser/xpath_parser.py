from lxml import html


class XpathParser:
    def __init__(self, doc_text):
        """
        Initialize the scraper with a provided HTML or XML document text.

        Parameters:
        - doc_text (str): The raw HTML or XML document string to be parsed.
        """
        self.tree = html.fromstring(doc_text)

    def get_elements(self, x_path):
        """
        Fetches elements from the document using the specified XPath query.

        Parameters:
        - x_path (str): The XPath query to fetch elements.

        Returns:
        - list: List of nodes matching the provided XPath query.
        """
        return self.tree.xpath(x_path)

    def get_element(self, x_path):
        """
        Fetches a single element (the first match) from the document using the specified XPath query.

        Parameters:
        - x_path (str): The XPath query to fetch the element.

        Returns:
        - lxml.html.HtmlElement or None: The first node matching the provided XPath query or None if no match is found.
        """
        elements = self.tree.xpath(x_path)
        return elements[0] if elements else None

    def select_all_nodes(self):
        """
        Select and return all nodes in the document.

        Returns:
        - list: List of all nodes in the document.
        """
        return self.tree.xpath('.//*')

    def select_by_tag(self, tag_name):
        """
        Select nodes in the document by their tag name.

        Parameters:
        - tag_name (str): Name of the tag to select.

        Returns:
        - list: List of nodes matching the given tag name.
        """
        return self.tree.xpath(f'//{tag_name}')

    def select_by_attribute(self, tag_name, attribute, value):
        """
        Select nodes with a specific attribute and value.

        Parameters:
        - tag_name (str): Name of the tag to select.
        - attribute (str): Name of the attribute to check.
        - value (str): Expected value of the attribute.

        Returns:
        - list: List of nodes matching the given criteria.
        """
        return self.tree.xpath(f'//{tag_name}[@{attribute}="{value}"]')

    def select_partial_attribute(self, tag_name, attribute, value_substring):
        """
        Select nodes based on a partial match for an attribute's value.

        Parameters:
        - tag_name (str): Name of the tag to select.
        - attribute (str): Name of the attribute to check.
        - value_substring (str): Substring to check within the attribute value.

        Returns:
        - list: List of nodes matching the given criteria.
        """
        return self.tree.xpath(f'//{tag_name}[contains(@{attribute}, "{value_substring}")]')

    def select_by_text(self, tag_name, exact_text):
        """
        Select nodes based on their exact text content.

        Parameters:
        - tag_name (str): Name of the tag to select.
        - exact_text (str): Expected exact text content of the node.

        Returns:
        - list: List of nodes matching the given criteria.
        """
        return self.tree.xpath(f'//{tag_name}[text()="{exact_text}"]')

    def select_partial_text(self, tag_name, partial_text):
        """
        Select nodes containing a specified substring in their text content.

        Parameters:
        - tag_name (str): Name of the tag to select.
        - partial_text (str): Expected substring within the node's text content.

        Returns:
        - list: List of nodes matching the given criteria.
        """
        return self.tree.xpath(f'//{tag_name}[contains(text(), "{partial_text}")]')

    def select_nth_child(self, parent_tag, child_tag, n):
        """
        Select the nth child of a given parent node.

        Parameters:
        - parent_tag (str): Name of the parent tag.
        - child_tag (str): Name of the child tag.
        - n (int): Index (1-based) of the child to select.

        Returns:
        - list: List of nodes matching the given criteria.
        """
        return self.tree.xpath(f'//{parent_tag}/{child_tag}[{n}]')

    def select_by_class(self, tag_name, class_name):
        """
        Select nodes with a specific CSS class.

        Parameters:
        - tag_name (str): Name of the tag to select.
        - class_name (str): Name of the CSS class.

        Returns:
        - list: List of nodes matching the given criteria.
        """
        return self.tree.xpath(f'//{tag_name}[@class="{class_name}"]')

    def select_by_id(self, element_id):
        """
        Select a node by its unique ID.

        Parameters:
        - element_id (str): The 'id' attribute value of the node.

        Returns:
        - list: List of nodes (usually a single node) with the specified ID.
        """
        return self.tree.xpath(f'//*[@id="{element_id}"]')
