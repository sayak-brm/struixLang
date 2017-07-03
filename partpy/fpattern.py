"""Predefined function patterns for use in Matcher.match_function methods.

Defines the following:
    - alphal = lower case alphabet
    - alphau = upper case alphabet
    - alpha = lower and upper case alphabet
    - number = digits
    - alnum = digits or lower and upper case alphabet
    - identifier = first(alpha) rest(alnum | '_')
    - qualified = first(alpha) rest(alnum | '.' | '_')
    - integer = first(number | '-') rest(number)
"""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

alphal = str.islower
alphau = str.isupper
alpha = str.isalpha

number = str.isdigit
alnum = str.isalnum


def _identifier_rest(char):
    return alnum(char) or char == '_'

identifier = (alpha, _identifier_rest)


def _qualified_rest(char):
    return alnum(char) or char in '_.'

qualified = (alpha, _qualified_rest)


def _integer_first(char):
    return number(char) or char == '-'

integer = (_integer_first, number)
