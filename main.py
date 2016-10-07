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

import primitives

class Lexer:
    ''' Lexer for struixLang. '''
    def __init__(self, text):
        self.text=text
        self.n = 0
        
    def nextWord(self):
        import string
        self.whitespace = ''
        if self.n >= len(self.text): return ''
        while self.text[self.n] in string.whitespace:
            self.whitespace += self.text[self.n]
            self.n += 1
            if self.n >= len(self.text): return ''
        n2 = self.n
        while self.text[n2] not in string.whitespace:
            n2 += 1
            if n2 >= len(self.text): break
        word = self.text[self.n:n2]
        n2 += 1
        self.n = n2
        return word
    
    def peekWord(self):
        import string
        n1 = self.n
        if n1 >= len(self.text): return ''
        while self.text[n1] in string.whitespace:
            n1 += 1
            if n1 >= len(self.text): return ''
        n2 = n1
        while self.text[n2] not in string.whitespace:
            n2 += 1
            if n2 >= len(self.text): break
        word = self.text[n1:n2]
        return word

    def charsTill(self, end):
        if self.n >= len(self.text): return ''
        n2 = self.n
        while self.text[n2] is not end:
            n2 += 1
            if n2 >= len(self.text): raise IndexError('string index out of range.')
        chars = self.text[self.n:n2]
        n2 += 1
        self.n = n2
        return chars
    
    def pushWord(self, word):
        self.n -= len(word) + 1
        
    def clear(self):
        self.n = len(self.text)

class Terp:
    ''' Interpreter for struixLang. '''
    def __init__(self):
        self.dictionary = {}
        self.stack = []
        
    def addWords(self, newWords):
        self.dictionary.update(newWords)

    def define(self, word, code):
        self.dictionary[word.upper()] = code
        
    def run(self, text):
        ''' Executes struixLang code. '''
        self.lexer = Lexer(text)
        word = None
        num = None
        while self.lexer.peekWord():
            word = self.lexer.nextWord()
            try: num = int(word)
            except ValueError:
                try: num = float(word)
                except ValueError: num = None
            if word.upper() in self.dictionary.keys():
                self.dictionary[word.upper()](self)
            elif num is not None:
                self.stack.append(num)
            elif word[0] in ['\'', '\"']:
                self.lexer.pushWord(word[1:])
                self.dictionary['STRING'](self, word[0])
            else:
                raise ValueError('Unknown Word: {}'.format(word))

terp = Terp()
primitives.AddWords(terp)
while True:
    terp.run(input('>>> '))
