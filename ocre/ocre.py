#!/usr/bin/env python3

from nltk.corpus import words as nltk_words
from nltk.corpus import wordnet as nltk_wordnet
from nltk.stem import SnowballStemmer
from nostril import nonsense
import plac
import os
import sys
from tabulate import tabulate
try:
    from termcolor import colored
except ImportError:
    pass


# Global constants.
# .............................................................................

DICTIONARY = None
STEMMER = None


# Main class
# .............................................................................

@plac.annotations(
    quiet    = ('do not print messages while working',             'flag', 'q'),
    no_color = ('do not color-code terminal output (default: do)', 'flag', 'C'),
    files    = 'list of files',
)

def main(quiet = False, no_color = False, *files):
    colorize = 'termcolor' in sys.modules and not no_color
    if not files:
        raise SystemExit(color('Need to provide a list of files', 'error', colorize))
    try:
        init_dictionary()
        init_stemmer()
        for f in files:
            with open(f) as input:
                print(tabulate(ratings(input.read()),
                               headers = ['Word', 'Dictionary?', 'Nostril?']))
    except KeyboardInterrupt:
        msg('Quitting.')


def ratings(text):
    table = []
    for word in text.split():
        if not word:
            continue
        if ignore(word):
            row = [word, '--', '--']
        else:
            row = [word,
                   'y' if in_dictionary(word) else 'n',
                   'n' if nonsense(word) else 'y']
        table.append(row)
    return table


def ignore(s):
    # Min 6 length is the default for Nostril.  Could change that but let's
    # try this for now.
    return len(s) < 6 or not s.isalpha()


def in_dictionary(s):
    if len(s) <= 1:
        return False
    return (s.lower() in DICTIONARY or stem(s.lower()) in DICTIONARY)


def stem(s):
    return STEMMER.stem(s)


def init_dictionary():
    # Note: I also tried adding the words from /usr/share/dict/web,
    # but the only additional words it had that were not already in
    # the next two dicts were people's proper names. Not useful.
    global DICTIONARY
    DICTIONARY = set(nltk_words.words())
    DICTIONARY.update(nltk_wordnet.all_lemma_names())


def init_stemmer():
    global STEMMER
    STEMMER = SnowballStemmer('english')


# Main entry point.
# ......................................................................
# The following allows users to invoke this using "python3 -m urlup".

if __name__ == '__main__':
    plac.call(main)
