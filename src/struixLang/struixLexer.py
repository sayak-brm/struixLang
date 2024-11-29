import string

class Lexer:
    ''' Lexer for struixLang with line and column tracking. '''
    
    def __init__(self, text):
        self.text = text
        self.pos = 0  # Position in text
        self.line_number = 1
        self.column_number = 1
        self.length = len(text)
        self.eos = self.pos >= self.length

    def get_char(self):
        ''' Returns the character at the current position '''
        if self.pos < self.length:
            return self.text[self.pos]
        else:
            return ''

    def eat_char(self):
        ''' Consumes the current character and advances position '''
        char = self.get_char()
        if char == '\n':
            self.line_number += 1
            self.column_number = 1
        else:
            self.column_number += 1
        self.pos += 1
        self.eos = self.pos >= self.length
        return char

    def peekWord(self):
        ''' Extracts and returns the next word while not changing position. '''
        saved_pos = self.pos
        saved_line = self.line_number
        saved_column = self.column_number
        word = self.nextWord()
        self.pos = saved_pos
        self.line_number = saved_line
        self.column_number = saved_column
        self.eos = self.pos >= self.length
        return word

    def nextWord(self):
        ''' Returns the next word in the code. '''
        self.skipWhitespace()
        if self.eos:
            return ''
        word = ''
        while not self.eos:
            char = self.get_char()
            if char in string.whitespace:
                break
            word += char
            self.eat_char()
        return word

    def skipWhitespace(self):
        ''' Skips all consecutive whitespaces from current position. '''
        while not self.eos:
            char = self.get_char()
            if char not in string.whitespace:
                break
            self.eat_char()

    def charsTill(self, end):
        ''' Returns following characters till given character. '''
        s = ""
        while not self.eos:
            char = self.get_char()
            self.eat_char()
            if char == end:
                return s
            s += char
        raise SyntaxError(f"Unterminated string: Expected '{end}' at line {self.line_number}, column {self.column_number}")

    def charsTillMultiline(self, end):
        """ Returns all characters until the multi-line string delimiter is found. """
        s = ""
        while not self.eos:
            char = self.get_char()
            s += char
            self.eat_char()
            if s.endswith(end):  # Check for the complete end delimiter
                return s[:-len(end)]
        raise SyntaxError(f"Unterminated string: Expected '{end}' at line {self.line_number}, column {self.column_number}")

    def clear(self):
        ''' Clears the Lexer. '''
        while not self.eos:
            self.eat_char()
            
    def clearLine(self):
        ''' Clears the Lexer till the end of the line. '''
        self.charsTill('\n')
