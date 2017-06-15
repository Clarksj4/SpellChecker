__author__ = 'Stephen'


import argparse
import SpellChecker
import re
import sys


def check(spell_checker, doc_path):
    """Checks the given document for errors in spelling according to the vocabulary, checks, and formatting contained in
    the given spell checker. Each line is separated into words by splitting in on hyphens and whitespace. Returns a
    generator that iterates through each spelling error in the document. Each yield returns a tuple containing: the line
    index of the error, the error as it was spelt, a set of possible corrections."""
    with open(doc_path, 'r') as document:
        line_index = 0
        for line in document:
            for word in re.split(r'[\s-]+', line):                              # split line on whitespace and hyphens
                corrections = spell_checker.check(word)
                if not (len(corrections) is 1 and word in corrections):         # if the word is not in the set of
                    yield line_index, word, corrections                         # corrections then it was misspelt
            line_index += 1


def raw_output(spell_checker, doc_path):
    """Prints the results of a document check. Each yield is printed to a new line."""
    for correction in check(spell_checker, doc_path):
        print correction


def tabular_output(spell_checker, doc_path):
    """Prints the results of a document check. The misspelt word column is right aligned. Each yield is printed to a new
    line."""
    for correction in check(spell_checker, doc_path):
        print "{0} >> {1} >> {2}".format(correction[0], ("'"+correction[1]+"'").rjust(15), list(correction[2]))


if __name__ == "__main__":
    # argparser handles command line input
    parser = argparse.ArgumentParser(description="Perform spell checking on words in a given file. Spell checking \
                                                 occurs by testing each word for membership in a set of vocabulary \
                                                 words. Possible corrections are obtained by performing mutative \
                                                 operations on each word and testing the new word for membership in the \
                                                 vocabulary set. The following operations are performed on misspelt \
                                                 words: character swapping on adjacent characters, replacement of \
                                                 characters by each possible alphabet character, character deletion, \
                                                 insertion of each possible alphabet character between characters in \
                                                 the given word. In addition to these operations formatting is applied \
                                                  to the word before its membership is tested. The formatting \
                                                 operations are as follows: removal of non-alphabet characters, \
                                                 conversion to lowercase. All of the listed operations can be switched \
                                                  off with the appropriate command-line argument.")
    parser.add_argument("document_path", help="path to document in need of spell checking")
    parser.add_argument("-v", "--vocabulary", default="vocabulary.txt", help="path to vocabulary file")
    parser.add_argument("--console", action="store_true", default=False, help="display output in a new console")
    parser.add_argument("-t", "--table", action="store_true", default=False, help="display output in a table")
    parser.add_argument("-s", "--swap", action="store_false", default=True,
                        help="perform character swapping on misspelt words when searching for possible corrections")
    parser.add_argument("-r", "--replace", action="store_false", default=True,
                        help="perform character replacement on misspelt words when searching for possible corrections")
    parser.add_argument("-d", "--delete", action="store_false", default=True,
                        help="perform character deletion on misspelt words when searching for possible corrections")
    parser.add_argument("-i", "--insert", action="store_false", default=True,
                        help="perform character insertion on misspelt words when searching for possible corrections")
    parser.add_argument("-a", "--alphabetical", action="store_false", default=True,
                        help="remove non-alphabet characters from words before checking for correct spelling")
    parser.add_argument("-l", "--lowercase", action="store_false", default=True,
                        help="convert words to lowercase before checking for correct spelling")
    # get command line arguments
    args = parser.parse_args()

    # if user wants report to output in new console window
    if args.console:
        """Create a subprocess with the same arguments that were passed to this process, with the "--console" argument
        removed. Subprocess will execute a call to the main method defined in DocumentChecker.py because the first
        argument in sys.argv is the name of the file called."""
        from sys import executable
        from subprocess import Popen, CREATE_NEW_CONSOLE

        sys.argv.remove("--console")
        sys.argv.insert(0, executable)
        process = Popen(sys.argv, creationflags=CREATE_NEW_CONSOLE)
    else:
        """Get vocabulary from the file passed, or from the "vocabulary.txt" file located in the same directory as this
        module. "vocabulary.txt" is passed as a default argument to argparser."""
        vocabulary = SpellChecker.extract_vocabulary(args.vocabulary)

        # construct list of desired checks, default uses all checks.
        checks = []
        if args.swap:
            checks.append(SpellChecker.swap)
        if args.delete:
            checks.append(SpellChecker.delete)
        if args.insert:
            checks.append(SpellChecker.insert)
        if args.replace:
            checks.append(SpellChecker.replace)

        # construct list of desired formatting, defaults uses all formatting
        formatting = []
        if args.alphabetical:
            formatting.append(SpellChecker.alphabetical)
        if args.lowercase:
            formatting.append(SpellChecker.lowercase)

        # construct spellchecker and check given file, output according to args
        checker = SpellChecker.SpellChecker(vocabulary, checks, formatting)
        if args.table:                              # output
            tabular_output(checker, args.document_path)
        else:
            raw_output(checker, args.document_path)
        raw_input("Press return to exit...")
