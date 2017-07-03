"""Predefined string patterns for use in Matcher.match_pattern methods.

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

alphal = 'abcdefghijklmnopqrstuvwxyz'
alphau = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alpha = alphal + alphau

number = '0123456789'
alnum = alpha + number

identifier = (alpha, alnum + '_')
qualified = (alpha, alnum + '_.')
integer = (number + '-', number)
