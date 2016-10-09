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
        self.text=text
        self.n = 0
        
    def nextWord(self):
        import string
        self.whitespace = ''
        if self.n >= len(self.text):
            return ''
        while self.text[self.n] in string.whitespace:
            self.whitespace += self.text[self.n]
            self.n += 1
            if self.n >= len(self.text):
                return ''
        n2 = self.n
        while self.text[n2] not in string.whitespace:
            n2 += 1
            if n2 >= len(self.text): break
        word = self.text[self.n:n2]
        n2 += 1
        self.n = n2
        return word
    
    def peekWord(self):
        word = self.nextWord()
        self.rewind(len(word))
        return word

    def charsTill(self, end):
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
        self.n -= places + 1
        
    def clear(self):
        self.n = len(self.text)

class Terp:
    ''' Interpreter for struixLang. '''

    ENABLE_UNSAFE_OPERATIONS = True
    
    def __init__(self):
        self.dictionary = {}
        self.dataStack = []
        self.compileBuffer = []
        self.stack = self.dataStack
        self.immediate = False
        self.newWord = None
        
    def addWords(self, newWords):
        self.dictionary.update(newWords)

    def define(self, word, code):
        self.dictionary[word.upper()] = code

    def lookup(self, word):
        if word.upper() in self.dictionary.keys():
            return self.dictionary[word.upper()]
        return None

    @staticmethod
    def parseNumber(string):
        try:
            num = int(string)
        except ValueError:
            try:
                num = float(string)
            except ValueError:
                num = None
        return num
        
    def run(self, text):
        ''' Executes struixLang code. '''
        self.lexer = Lexer(text)
        word = None
        while self.lexer.peekWord():
            word = self.compile(self.lexer.nextWord())
            if self.immediate or not self.isCompiling():
                self.interpret(word)
                self.immediate = False
            else:
                self.stack.append(word)

    def interpret(self, word):
        import types
        if isinstance(word, types.FunctionType):
            word(self)
        else:
            self.stack.append(word)

    def compile(self, word):
        word = word.upper()
        num = self.parseNumber(word)
        fn = self.lookup(word)
        if fn:
            self.immediate = fn.__dict__.get('immediate', False)
            return fn
        elif num:
            return num
        elif word[0] in ['\'', '\"']:
            self.lexer.rewind(len(word[1:]))
            return self.lookup('STRING')(self, word[0])
        else:
            raise ValueError('Unknown Word: {}'.format(word))

    def startCompile(self):
        self.stack = self.compileBuffer

    def stopCompile(self):
        self.stack = self.dataStack

    def isCompiling(self):
        return self.stack is self.compileBuffer
