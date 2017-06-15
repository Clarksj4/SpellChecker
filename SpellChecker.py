__author__ = 'Stephen'


import re
import string


class SpellChecker:
    """Class for checking the spelling of words. Stores a vocabulary set that it checks words for membership in to test
    for correct spelling."""
    def __init__(self, vocabulary, checks, formatting):
        self.vocabulary = vocabulary
        self._checks = checks
        self._formatting = formatting

    def check(self, word):
        """Checks the given word for correct spelling. The word is formatted prior to checking for correct spelling. The
        strength of the check is related to the vocabulary, and check and formatting methods passed to this object.
        Returns a set containing: in the case of correct spelling, the given word only; otherwise, a collection of all
        possible corrections to the given word."""
        original = word
        for format in self._formatting:
            word = format(word)
        if word in self.vocabulary or not word:                         # word is correct, or empty
            return {original}
        else:
            corrections = set()
            for check in self._checks:                                  # apply all check methods to word
                corrections.update(check(self.vocabulary, word))
            return corrections


def extract_vocabulary(doc_path):
    """Extracts a set of a words from the given file, by splitting each line by white-space and storing the resulting
    strings. Returns the set of words."""
    with open(doc_path, 'r') as document:
        vocabulary = set()
        for line in document:
            for word in line.split():
                vocabulary.add(word)
        return vocabulary


def swap(vocabulary, misspelling):
    """Swaps each character in the given word with each adjacent character, one at a time, testing for membership in
    the given vocabulary set after each swap operation. Returns a set that is the words created by swapping characters
    in the given word, if the created word is also present in the vocabulary set."""
    corrections = set()
    for i in xrange(len(misspelling) - 1):
        sliced = list(misspelling)
        sliced[i], sliced[i + 1] = sliced[i + 1], sliced[i]
        word = ''.join(sliced)
        if word in vocabulary:                     # check if the new word in the vocabulary
            corrections.add(word)
    return corrections


def insert(vocabulary, misspelling):
    """Inserts each alphabet character at each position in the given word, one at a time, testing for mmbership in the
    given vocabulary set after each insert operation. Returns a set that is the words created by inserting characters
    in the given word, if the created word is also present in the vocabulary set."""
    corrections = set()
    characters = string.ascii_lowercase
    for i in xrange(len(misspelling) + 1):
        for character in characters:
            word = misspelling[:i] + character + misspelling[i:]    # insert character into new string
            if word in vocabulary:
                corrections.add(word)
    return corrections


def delete(vocabulary, misspelling):
    """Deletes each character in the word, one at a time, testing for membership in the given vocabulary set after each
    delete operation. Returns a set that is the words created by deleting characters in the given word, if the created
    word is also present in the vocabulary set."""
    corrections = set()
    for i in xrange(len(misspelling)):
        word = misspelling[:i] + misspelling[i + 1:]
        if word in vocabulary:
            corrections.add(word)
    return corrections


def replace(vocabulary, misspelling):
    """Replaces each character in the word with each alphabet character, one at a time, testing for membership in the
    given vocabulary set after each replace operation. Returns a set that is the words created by replacing characters
    in the given word, if the created word ia also present in the vocabulary set."""
    corrections = set()
    characters = string.ascii_lowercase
    for i in xrange(len(misspelling)):
        for character in characters:
            word = misspelling[:i] + character + misspelling[i + 1:]    # replace character at i in misspelling
            if word in vocabulary:
                corrections.add(word)
    return corrections


def alphabetical(word):
    """Removes characters not in ranges a-z, A-Z from the given word."""
    return re.sub('[^a-zA-Z]', "", word)


def lowercase(word):
    """Converts the given word to lowercase"""
    return word.lower()


if __name__ == "__main__":
    import argparse
    # argparser handles command line input
    parser = argparse.ArgumentParser(description="Perform spell checking on a given word. Spell checking occurs by "
                                                 "testing the given word for membership in a set of vocabulary words. "
                                                 "Possible corrections are obtained by performing mutative operations "
                                                 "on the given word and testing the new word for membership in the "
                                                 "vocabulary set. The following operations are performed on misspelt "
                                                 "words: character swapping on adjacent characters, replacement of "
                                                 "characters by each possible alphabet character, character deletion, "
                                                 "insertion of each possible alphabet character between characters in "
                                                 "the given word. In addition to these operations formatting is applied"
                                                 " to the word before its membership is tested. The formatting"
                                                 "operations are as follows: removal of non-alphabet characters, "
                                                 "conversion to lowercase. All of the listed operations can be switched"
                                                 " off with the appropriate command-line argument.")
    parser.add_argument("word", help="word to check for spelling errors")
    parser.add_argument("-v", "--vocabulary", default="vocabulary.txt", help="path to vocabulary file")
    parser.add_argument("-s", "--swap", action="store_false", default=True,
                        help="perform character swapping on misspelt word when searching for possible corrections")
    parser.add_argument("-r", "--replace", action="store_false", default=True,
                        help="perform character replacement on misspelt word when searching for possible corrections")
    parser.add_argument("-d", "--delete", action="store_false", default=True,
                        help="perform character deletion on misspelt word when searching for possible corrections")
    parser.add_argument("-i", "--insert", action="store_false", default=True,
                        help="perform character insertion on misspelt word when searching for possible corrections")
    parser.add_argument("-a", "--alphabetical", action="store_false", default=True,
                        help="remove non-alphabet characters from word before checking for correct spelling")
    parser.add_argument("-l", "--lowercase", action="store_false", default=True,
                        help="convert word to lowercase before checking for correct spelling")
    # get args given at command line
    args = parser.parse_args()

    # get vocabulary from given vocab file or default vocab file
    vocabulary = extract_vocabulary(args.vocabulary)

    # get list of checks to preform on word
    checks = []
    if args.swap:
        checks.append(swap)
    if args.delete:
        checks.append(delete)
    if args.insert:
        checks.append(insert)
    if args.replace:
        checks.append(replace)

    # get list of formatting to apply to word
    formatting = []
    if args.alphabetical:
        formatting.append(alphabetical)
    if args.lowercase:
        formatting.append(lowercase)

    # create spellchecker and check word
    checker = SpellChecker(vocabulary, checks, formatting)
    corrections = checker.check(args.word)

    # output
    if not (len(corrections) is 1 and args.word in corrections):
        print "Unknown word: '" + args.word + "' >> " + str(list(corrections))
    else:
        print "Spelling is ok: " + args.word
