##   Copyright 2016-2024 Sayak Brahmachari

from partpy import SourceString
import string

class Lexer(SourceString):
    ''' Lexer for struixLang. '''
    def nextWord(self):
        ''' Returns the next word in the code. '''
        word = self.peekWord()
        self.eat_string(word)
        return word

    def skipWhitespace(self):
        ''' Skips all consecutive whitespaces from current position. '''
        while not self.eos:
            if self.get_char() not in string.whitespace: break
            self.eat_string(self.get_char())

    def peekWord(self):
        ''' Extracts and returns the next word while not changing position. '''
        self.skipWhitespace()
        while not self.eos:
            word = self.get_string()
            return word
        return ''

    def charsTill(self, end):
        ''' Returns following characters till given character. '''
        s = ""
        while not self.eos:
            char = self.get_char()
            self.eat_length(1)
            if char == end:
                return s
            s += char
        raise SyntaxError(f"Unterminated string: Expected '{end}'")

    def charsTillMultiline(self, end):
        """ Returns all characters until the multi-line string delimiter is found. """
        s = ""
        while not self.eos:
            char = self.get_char()
            self.eat_length(1)
            s += char
            if s.endswith(end):  # Check for the complete end delimiter
                return s[:-len(end)]
        raise SyntaxError(f"Unterminated string: Expected '{end}'")

    def clear(self):
        ''' Clears the Lexer. '''
        while not self.eos: self.eat_length(1)
        
    def clearLine(self):
        ''' Clears the Lexer till the end of the line. '''
        self.charsTill('\n')
