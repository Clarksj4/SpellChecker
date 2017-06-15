# Spell Checker

Write a spell-checker class that stores a lexicon of words, __W__, in a Python set,  and  implements a method, _check(s)_, which  performs  a spell  check on  the  string __s__ with respect  to  the  set  of words, __W__.If __s__ is in __W__,then the call  to _check(s)_  returns  a list containing  only __s__,  as it is assumed  to be spelled correctly in this case. If s is not in __W__, then the call to _check(s)_ returns a list of every word in __W__ that might be a correct spelling of __s__. Your program should be able to handle all the common ways that __s__ might be a misspelling of a word in __W__, including:

- Swapping adjacent characters in a word, 
- Inserting a single character in between two adjacent characters in a word, 
- Deleting a single character from a word,
- Replacing a character in a word with another character.

## Document Checker

You will create your lexicon by reading in a text file full of words that are spelled correctly; then, write a program that uses your module. It should read in a text file specified at the command line and output a spell checking report.  The report  should show:

- The misspelled word and the line number on which it occurs,
- A list of possible corrections.
- It does not need to correct the misspellings in the input file.
