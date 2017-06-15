# Spell Checker
Write a Python module that implements a spell checker as described in problem P-10.55 in the book. You will create your lexicon by reading in a text file full of words that are spelled correctly. Then write a little program that uses your module. It should read in a text file specified at the command line and output a spell checking report.  The report  should show:
* The misspelled word and the line number on which it occurs,
* A list of possible corrections.
* It does not need to correct the misspellings in the input file.


# P-10.55
Write a spell-checker class that stores a lexicon of words, W, in a Python set,  and  implements  a method, check(s), which  performs  a spell  check on  the  string s with respect  to  the  set  of words, W.If s is in W,then the call  to check(s)  returns  a list containing  only s,  as it is assumed  to be spelled correctly in this case. If s is not in W, then the call to check(s) returns a list of every word in W that might be a correct spelling of s. Your program should be able to handle all the common ways that s might be a misspelling of a word in W, including swapping adjacent characters in a word, inserting a single character in between two adjacent characters in a word, deleting a single character from a word, and replacing a character in a word with another character.
