import re


def replace(regex_string, new_text, input_text):
    """
    Replace occurrences of a regex pattern with a new string.

    Args:
    - regex_string (str): The regex pattern.
    - new_text (str): The replacement string.
    - input_text (str): The text to be searched and replaced.

    Returns:
    - str: Modified string after replacements.
    """
    return re.sub(regex_string, new_text, input_text)


def find_all(regex_string, input_text):
    """
    Find all occurrences of a regex pattern in a string.

    Args:
    - regex_string (str): The regex pattern.
    - input_text (str): The text to be searched.

    Returns:
    - list: List of all matches.
    """
    return re.findall(regex_string, input_text)


def find_first(regex_string, input_text):
    """
    Find the first occurrence of a regex pattern in a string.

    Args:
    - regex_string (str): The regex pattern.
    - input_text (str): The text to be searched.

    Returns:
    - str: The first match, or None if no match is found.
    """
    match = re.search(regex_string, input_text)
    return match.group(0) if match else None


def find_before(search_text, input_text):
    """
    Find the portion of text immediately before a given substring.

    Args:
    - search_text (str): The substring to search for.
    - input_text (str): The text to be searched.

    Returns:
    - str: Text before the substring, or None if substring is not found.
    """
    reg_str = f'.+(?={search_text})'
    match = re.search(reg_str, input_text)
    return match.group(0) if match else None


def find_after(search_text, input_text):
    """
    Find the portion of text immediately after a given substring.

    Args:
    - search_text (str): The substring to search for.
    - input_text (str): The text to be searched.

    Returns:
    - str: Text after the substring, or None if substring is not found.
    """
    reg_str = f'(?<={search_text}).+'
    match = re.search(reg_str, input_text)
    return match.group(0) if match else None


def find_between(left_side, right_side, input_text):
    """
    Find text between two specified substrings.

    Args:
    - left_side (str): The left boundary substring.
    - right_side (str): The right boundary substring.
    - input_text (str): The text to be searched.

    Returns:
    - str: Text between the boundaries, or None if not found.
    """
    reg_str = f'(?<={left_side}).+(?={right_side})'
    match = re.search(reg_str, input_text)
    return match.group(0) if match else None


def is_match(regex_string, input_text):
    """
    Check if the input text matches the given regex pattern from the start.

    Args:
    - regex_string (str): The regex pattern.
    - input_text (str): The text to be checked.

    Returns:
    - bool: True if the input text matches the pattern, otherwise False.
    """
    return bool(re.match(regex_string, input_text))


def split(regex_string, input_text):
    """
    Split the input text using the provided regex pattern.

    Args:
    - regex_string (str): The regex pattern to split by.
    - input_text (str): The text to be split.

    Returns:
    - list: List of substrings obtained after splitting.
    """
    return re.split(regex_string, input_text)
