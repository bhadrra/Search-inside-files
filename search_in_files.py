#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Multithreaded, recursive text or regex search in all text-containing files
in a directory (pure Python).

Additional features:
    - Case sensitivity
    - print results as PrettyTable
        (one table for all files or one table per file)
    - can also return the result as an OrderedDict 

Usage examples: 
    - Real example of what I wanted to do when I wrote this program: 
python search_in_files.py "sleep" -d beloglazov-openstack-neat-a5a853a -fn *.py

    - Other possible examples:
python search_in_files.py " Watson " -d sherlockHolmesBooks -fn *.txt -s
python search_in_files.py caseSensitiveWord -C -d ../foldername -fn *.txt
python search_in_files.py #FIXME -fn *.py
python search_in_files.py #[A-Z]{3,5} -r -C -fn *.py
python search_in_files.py "Hello World"
"""

import os
import sys
import re
from glob import glob
from collections import OrderedDict, defaultdict, namedtuple
from functools import partial
import multiprocessing
from multiprocessing.dummy import Pool
import argparse

from prettytable import PrettyTable

class cd:
    """Context manager for changing the current working directory.
    http://stackoverflow.com/questions/431684/how-do-i-cd-in-python/13197763#13197763
    """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def search_in_files(expression, isRegex=False, case_sensitive=False,
    folderpath='.', filename_regex='*',
    printPrettyTable=True, separate_tables=False):
    
    def select_line_matcher(expression=expression, isRegex=isRegex):
        def line_matches_regex(expression, line):
            return re.search(expression, line) is not None

        def line_matches_expr(expression, line):
            return expression in line

        if not case_sensitive:
            expression = expression.lower()
        if isRegex:
            return partial(line_matches_regex, expression=expression)
        else:
            return partial(line_matches_expr, expression=expression)

    def _search_in_file(filepath, case_sensitive):
        fileResults = []
        try:
            with open(filepath, 'r') as file:
                for lineNumber, lineText in enumerate(file):
                    if match_found(line=lineText if case_sensitive
                                        else lineText.lower()):
                        fileResults.append(
                            MatchedLine(lineNumber+1, lineText.strip('\n')))
        except:
            pass
        return fileResults

    match_found = select_line_matcher()
    results = defaultdict(list)
    MatchedLine = namedtuple('MatchedLine', ['num', 'text'])
    pool = Pool()
    search_in_file = partial(_search_in_file, case_sensitive=case_sensitive)

    #Change current directory to folderpath
    with cd(folderpath):
        #Recursively lists all file paths that match filename_regex
        filepaths = glob("**/"+filename_regex, recursive=True)
        #Open each file, search for the expression, list all matching lines
        #in order
        filematches = pool.map(search_in_file, filepaths)
        pool.close()
        pool.join()
        #Map each filepath to its list of matching lines
        for filepath, filematch in zip(filepaths, filematches):
            results[filepath] = filematch
    
    #Order the results by file path
    orderedResults = OrderedDict(sorted(
        {k:v for (k,v) in results.items() if len(k.split('\\')) == 1}.items()))
    orderedResultsRest = OrderedDict(sorted(
        {k:v for (k,v) in results.items() if len(k.split('\\')) != 1}.items()))
    orderedResultsDicts = [orderedResults, orderedResultsRest]

    #Turn the orderedResultsDicts into a PrettyTable and print it
    if printPrettyTable:
        prettyTableColumns = ["File Path", "Line n°", "Line Text"]
        if separate_tables:
            for orderedResultsDict in orderedResultsDicts:
                for (filepath, matchedLines) in orderedResultsDict.items():
                    x = PrettyTable(prettyTableColumns)
                    x.align[prettyTableColumns[-1]] = 'l'
                    for matchedLine in matchedLines:
                        x.add_row(
                            [filepath, matchedLine.num, matchedLine.text])
                    if matchedLines:
                        print(x)
        else:
            x = PrettyTable(prettyTableColumns)
            x.align[prettyTableColumns[-1]] = 'l'
            for orderedResultsDict in orderedResultsDicts:
                for (filepath, matchedLines) in orderedResultsDict.items():
                    for matchedLine in matchedLines:
                        x.add_row(
                            [filepath, matchedLine.num, matchedLine.text])
                    if matchedLines:
                        x.add_row(["", "", ""])
                if orderedResultsDict != orderedResultsDicts[-1] \
                    and sum([len(vals) for vals in orderedResultsDict.values()
                            ]) != 0:
                    x.add_row(["-----\n" for _ in range(len(x.field_names))])
            print(x)
    else:
        return orderedResults


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("e", type=str, help="the expression to search for")
    parser.add_argument("-r", "--regex", action="store_true",
        help="evaluate the expression as a regex")
    parser.add_argument("-d", "--directory", type=str,
        help="the path to the containing directory")
    parser.add_argument("-fn", "--filenameregex", type=str, 
        help="search only in the files whose name match this regex")
    parser.add_argument("-s", "--separatetables", action="store_true",
        help="prints the search results in separate tables for each file")
    parser.add_argument("-C", "--casesensitive", action="store_true",
        help="enable case-sensitive matching")

    args = parser.parse_args()
    expression = args.e
    isRegex = args.regex
    folderpath = args.directory if args.directory else "."
    filename_regex = args.filenameregex if args.filenameregex else "*"
    separate_tables = args.separatetables
    case_sensitive = args.casesensitive

    search_in_files(expression=expression,
                    isRegex=isRegex,
                    case_sensitive = case_sensitive,
                    folderpath=folderpath,
                    filename_regex=filename_regex, 
                    separate_tables=separate_tables)