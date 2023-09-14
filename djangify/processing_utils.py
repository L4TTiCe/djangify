#!/usr/bin/env python

import re


def check_line(line: str):
    """
    A funtion that checks if a string passed to this function contains key
    words that need to be processed further

    Parameters
    ----------
    line : str\n
            a string that needs to be checked if it contains key words

    Returns
    -------
    list\n
            a list of words found in the string 'line', if the word is
            a keyword,then instead of only the word, a tuple in the
            form of (True, word) is added
    """
    exclude_tags = ["a"]
    key_words = ["src", "href", "url"]
    out = []
    for word in key_words:
        if line.__contains__(word):
            # Exclude if the line contains one of the exclude_tags
            if any(tag in line for tag in exclude_tags):
                continue
            out.append((True, word))

    # Check if output list is not empty
    if len(out) == 0:
        # If list is empty return None
        return None
    else:
        return out


def contains_url(line: str):
    """
    Checks if the line contains any URLs

    Parameters
    ----------
    line : str\n
            The string that needs to be checked if it countains URLs

    Returns
    -------
    bool\n
            True if it contains URL and False if no URL in 'line'
    """

    URL = (
        r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))"
        r"([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
    )
    if re.match(URL, line):
        return True
    else:
        return False


def get_index(line: str, word: str):
    """
    Get the starting and ending index of a word in a given string

    Parameters
    ----------
    line : str\n
            A string containing the 'word' from which indexes are
            to be extracted from
    word : str\n
            A string that need to be found in the 'line', and need indexes
            extracted

    Returns
    -------
    tuple\n
        A tuple of the form (start, end), where start and end are the starting
        and ending indexes of the 'word' in the given 'line'
    """

    index = line.find(word)

    if word in ["url"]:
        start = index + len(word) + 2
        quote = line[start - 1]
        if quote not in ["'", '"']:
            start = index + len(word) + 1
            quote = line[start - 1]
            if quote == "(":
                end = line.find(")", start)
            else:
                end = line.find(quote, start)
        else:
            end = line.find(quote, start)
    else:
        start = index + len(word) + 2
        quote = line[start - 1]
        end = line.find(quote, start)

    return start, end


def djangify(line: str, app_name: str):
    """
    Translates the string passed to the function to Django compatible HTML

    Parameters
    ----------
    line : str\n
            A string that contains native HTML that need translation
    app_name: str\n
            A string that informs about the app name to be used with static

    Returns
    -------
    str\n
            Translated HTML that is Django compatible
    """

    # Don't change the contents of the line if it contails a URL that links
    # outside content. Ex. www.example.com/webpage.html
    if contains_url(line):
        return line
    # Don't change the line if it contains placeholder URL like '#'
    if line == "#":
        return line
    # If line links to an internal file, make it Django compatible by loading
    # from static directory appended with app_name
    return " {% static '" + app_name + line + "' %} "


def process_line(line: str, app_name: str):
    """
    Processes the line (string) of text passed in as parameter into django
    compatible HTML by calling the djangify(...) function.

    Parameters
    ----------
    line : str\n
            A line (string) of HTML, that is yet to be made django compatible
    app_name: str\n
            A string that informs about the app name to be used with static

    Returns
    -------
    str\n
            Translated HTML that is Django compatible
    """

    # Converts line into a list of words, using checkLine()
    instances = check_line(line)

    buffer = line

    if instances:
        for instance in instances:
            index = get_index(buffer, instance[1])
            out = djangify(buffer[index[0] : index[1]], app_name)
            text = buffer[: index[0]] + out + buffer[index[1] :]
            buffer = text

    return buffer
