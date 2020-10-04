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
import argparse
import logging

from .processing_utils import process_line

# Set default logging level to INFO
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# Initialize global variable APP_NAME
APP_NAME = ""


def display_path_info():
    # TODO: Remove unwanted / unused functions
    """
    A simple function to state the current and working directory
    """

    dirpath = os.getcwd()
    logging.info("Current Directory is : " + dirpath)
    foldername = os.path.basename(dirpath)
    logging.info("Directory name is : " + foldername)


def process_file(directory: str, filepath: str, fname: str, app_name: str = APP_NAME):
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
    app_name: str\n
            name of the application to be used, defaults to none
    """

    fname = fname.split(".")[0]
    extension = "html"

    # Generate filename and directory of the files to be created
    save_path = os.path.join(directory, "Modified_files")
    save_path = os.path.join(save_path, fname)
    # Open a blank file to write translated HTML to
    f = open(save_path + "." + extension, "w+")
    f.write("{% load static %}")
    f.write("\n")

    try:
        # Opening the file
        with open(filepath) as fp:
            # Reading data line-by-line
            line = fp.readline()
            cnt = 1
            while line:
                # process the line extracted
                temp = process_line(line, app_name)
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
        description='Converts specified html files or '
                    'all html files to django format within '
                    'a \n specified directory.'
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

    if files:
        print("here")
        for file in files:
            process_file(directory, directory + "/" + file, file)

    else:
        print("no files found")
        # If no file was passed in as input, then extract all files in the
        # directory passed in, with extension '.html'
        for file in os.listdir(directory):
            if file.endswith(".html"):
                process_file(directory, directory + "/" + file, file)
