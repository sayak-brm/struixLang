##   Copyright 2016 Sayak Brahmachari
##
##   Licensed under the Apache License, Version 2.0 (the "License");
##   you may not use this file except in compliance with the License.
##   You may obtain a copy of the License at
##
##       http://www.apache.org/licenses/LICENSE-2.0
##
##   Unless required by applicable law or agreed to in writing, software
##   distributed under the License is distributed on an "AS IS" BASIS,
##   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##   See the License for the specific language governing permissions and
##   limitations under the License.

class Lexer:
    ''' Lexer for struixLang. '''
    def __init__(self, text):
        ''' Initializes the Lexer. '''
        self.text=text
        self.n = 0

    def getWord(self):
        ''' Returns the next word in the code. '''
        import string
        n1 = self.n
        while self.n < len(self.text) and self.text[self.n] not in string.whitespace:
            self.n += 1
        word = self.text[n1:self.n]
        return word

    def skipWhitespace(self):
        ''' Skips all consecutive whitespaces from current position. '''
        import string
        while self.n < len(self.text) and self.text[self.n] in string.whitespace:
            self.whitespace += self.text[self.n]
            self.n += 1
    
    def nextWord(self):
        ''' Extracts and returns the next word. '''
        import string
        self.whitespace = ''
        if self.n >= len(self.text):
            return ''
        self.skipWhitespace()
        word = self.getWord()
        return word
    
    def peekWord(self):
        ''' Extracts and returns the next word while not changing position. '''
        word = self.nextWord()
        self.rewind(len(word))
        return word

    def charsTill(self, end):
        ''' Returns following characters till given character. '''
        if self.n >= len(self.text):
            return ''
        n2 = self.n
        while self.text[n2] is not end:
            n2 += 1
            if n2 >= len(self.text):
                raise IndexError('string index out of range.')
        chars = self.text[self.n:n2]
        n2 += 1
        self.n = n2
        return chars
    
    def rewind(self, places):
        ''' Rewinds Lexer counter by given places. '''
        self.n -= places
        
    def clear(self):
        ''' Clears the Lexer. '''
        self.n = len(self.text)

    def clearLine(self):
        ''' Clears the Lexer. '''
        self.charsTill('\n')
