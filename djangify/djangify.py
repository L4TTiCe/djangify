#!/usr/bin/env python

""" Djangify

A Python script that converts HTML Files / Templates to Django
compatible HTML Templates.

This script allows the user to translate HTML Files from any source
(Tempates, Auto-generated etc.) to Django compatible HTML files
by translating 'href' and 'src' attributes from fetching files directly
to fetching through static directory.

usage: djangify [-h] [-d [BASE_DIRECTORY]] [-a [APP_NAME]] [f [f ...]]

Converts specified html files or all html files to django format within a
specified directory.

positional arguments:
  f                    provide file names to convert

optional arguments:
  -h, --help           show this help message and exit
  -d [BASE_DIRECTORY]  Provide base directory
  -a [APP_NAME]        provide django app name

"""

import os
import re
import argparse
import logging

# Set default logging level to INFO
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# Initialize global variable APP_NAME
APP_NAME = ""


def displayPathInfo():
    # TODO: Remove unwanted / unused functions
    """
    A simple function to state the current and working directory
    """

    dirpath = os.getcwd()
    logging.info("Current Directory is : " + dirpath)
    foldername = os.path.basename(dirpath)
    logging.info("Directory name is : " + foldername)


def checkLine(line: str):
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
            a list of words found in the string 'line', if the word is a keyword,
            then instead of only the word, a tuple in the form of (True, word) is
            added
    """

    key_words = ['src', 'href', 'url']
    out = list()
    for word in key_words:
        if line.__contains__(word):
            out.append((True, word))

    # Check if output list is not empty
    if len(out) == 0:
        # If list is empty return None
        return None
    else:
        return out


def containsURL(line: str):
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

    URL = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))" \
        "([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
    if re.match(URL, line):
        return True
    else:
        return False


def getIndex(line: str, word: str):
    """
    Get the starting and ending index of a word in a given string

    Parameters
    ----------
    line : str\n
            A string containing the 'word' from which indexes are to be extracted
            from
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

    if word in ['url']:
        start = (index + len(word) + 2)
        quote = line[start - 1]
        if quote not in ['\'', '"']:
            start = (index + len(word) + 1)
            quote = line[start - 1]
            if quote == '(':
                end = line.find(')', start)
            else:
                end = line.find(quote, start)
        else:
            end = line.find(quote, start)
    else:
        start = (index + len(word) + 2)
        quote = line[start - 1]
        end = line.find(quote, start)
        
    return (start, end)


def djangify(line: str):
    """
    Translates the string passed to the function to Django compatible HTML

    Parameters
    ----------
    line : str\n
            A string that contains native HTML that need translation

    Returns
    -------
    str\n
            Translated HTML that is Django compatible
    """

    global APP_NAME

    # Don't change the contents of the line if it contails a URL that links
    # outside content. Ex. www.example.com/webpage.html
    if containsURL(line):
        return line
    # Don't change the line if it contains placeholder URL like '#'
    if line == '#':
        return line
    # If line links to an internal file, make it Django compatible by loading
    # from static directory appended with APP_NAME
    return " {% static '" + APP_NAME + line + "' %} "


def processLine(line: str):
    """
    Processes the line (string) of text passed in as parameter into django
    compatible HTML by calling the djangify(...) function.

    Parameters
    ----------
    line : str\n
            A line (string) of HTML, that is yet to be made django compatible

    Returns
    -------
    str\n
            Translated HTML that is Django compatible
    """
    
    # Converts line into a list of words, using checkLine()
    instances = checkLine(line)

    buffer = line

    if instances:
        for instance in instances:
            index = getIndex(buffer, instance[1])
            out = djangify(buffer[index[0]: index[1]])
            text = buffer[: index[0]] + out + buffer[index[1]:]
            buffer = text

    return buffer


def processFile(directory: str, filepath: str, fname: str):
    """
    Prcocesses the file passed in as parameter, translating it into django
    friendly HTML.

    Saves the translated files in a newly created directory, "Modified_files"
    
    Parameters
    ----------
    directory : str\n
            directory that contains the file that is to be translated
    filepath : str\n
            path of the file that is to be translated
    fname : fname\n
            name of the file to be translated
    """

    fname = fname.split(".")[0]
    extension = "html"

    # Generate filename and directory of the files to be created
    save_path = os.path.join(directory, "Modified_files")
    save_path = os.path.join(save_path, fname)
    # Open a blank file to write translated HTML to
    f = open(save_path + "." + extension, "w+")

    try:
        # Opening the file
        with open(filepath) as fp:
            # Reading data line-by-line
            line = fp.readline()
            cnt = 1
            while line:
                # process the line extracted
                temp = processLine(line)
                line = fp.readline()
                cnt += 1
                # write the processed line to the newly created file
                f.write(temp)
    except IOError:
        logging.error('An error occurred trying to read the file.')
    finally:
        # Close the file to save changes
        f.close()

    logging.info("Succeeded.. Generated Modified_Files/" + fname +
                 "." + extension + " in the directory passed.")


def main():
    """
    The main wrapper function, to process args from the user
    """

    global APP_NAME

    # Defines Argument Parser and fefines flags and expected inputs
    parser = argparse.ArgumentParser(
        description='Converts specified html files or all html files to \
			django format within a \n specified directory.'
    )
    # Defines the -f flag, standing for files, to gey file nameof the HTML
    # file to convert
    parser.add_argument(
        'files',
        metavar='f',
        type=str,
        nargs='*',
        help='provide file names to convert'
    )
    # Defines the -a flag, for defining the APP_NAME, you want the file
    # converted to, for.
    parser.add_argument(
        '-a',
        dest='app_name',
        type=str,
        nargs='?',
        help='provide django app name'
    )
    # Defines the -d flag, standing for directory, which accepts the path
    # to a directory containing the files to be translated
    parser.add_argument(
        '-d',
        dest='base_directory',
        type=str,
        nargs='?',
        help='Provide base directory'
    )

    # Parse the Arguments from the user
    args = parser.parse_args()

    # Deconstruct the arguments from the parser
    files = args.files
    directory = args.base_directory
    app_name = args.app_name

    # If APP_NAME is not passes in as an argument, leave it as ''(empty)
    if app_name is not None:
        APP_NAME = app_name + "/"

    # If directory is not passed in as an argument, use the current working
    # directory to fetch files
    if directory is None:
        directory = os.getcwd()

    logging.info("Directory : " + str(directory))
    logging.info("app_name  : " + str(app_name))

    # Check if the directory passed in as argument already has the directory 
    # 'Modified_files', else create it.
    if not os.path.exists(os.path.join(directory, "Modified_files")):
        os.mkdir(os.path.join(directory, "Modified_files"))

    if files != []:
        for file in files:
            processFile(directory, directory + "/" + file, file)

    else:
        # If no file was passed in as input, then extract all files in the 
        # directory passed in, with extension '.html'
        for file in os.listdir(directory):
            if file.endswith(".html"):
                processFile(directory, directory + "/" + file, file)

main()
