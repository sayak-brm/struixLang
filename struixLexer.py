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

    def clear(self):
        ''' Clears the Lexer. '''
        while not self.eos: self.eat_length(1)
        
    def clearLine(self):
        ''' Clears the Lexer till the end of the line. '''
        self.charsTill('\n')
