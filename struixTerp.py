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
        while self.text[self.n] not in string.whitespace:
            self.n += 1
            if self.n >= len(self.text): break
        word = self.text[n1:self.n]
        return word

    def skipWhitespace(self):
        ''' Skips all consecutive whitespaces from current position. '''
        import string
        while self.text[self.n] in string.whitespace:
            self.whitespace += self.text[self.n]
            self.n += 1
            if self.n >= len(self.text):
                return ''
    
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
        ''' Adds given words to interpretor dictionary. '''
        self.dictionary.update(newWords)

    def define(self, word, code):
        ''' Defines (or redefines) a word in the dictionary. '''
        self.dictionary[word.upper()] = code

    def lookup(self, word):
        ''' Returns a word with given key from dictionary. '''
        if isinstance(word, str) and word.upper() in self.dictionary.keys():
            return self.dictionary[word.upper()]
        return None

    @staticmethod
    def parseNumber(string):
        ''' Parses a string to either an integer or a float. '''
        try:
            num = int(string)
        except ValueError:
            try:
                num = float(string)
            except ValueError:
                num = None
        return num
        
    def run(self, text):
        ''' Starts processing of struixLang code. '''
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
        ''' Executes struixLang code. '''
        import types
        if isinstance(word, (types.FunctionType, types.MethodType)):
            word(self)
        else:
            self.stack.append(word)

    def compile(self, word, errMsg = 'Unknown Word: {}'):
        ''' Compiles struixLang code to its internal representation. '''
        import types
        word = word.upper() if isinstance(word, str) else word
        num = self.parseNumber(word) if not isinstance(word, (types.FunctionType, types.MethodType)) else None
        fn = word if isinstance(word, (types.FunctionType, types.MethodType)) else self.lookup(word)
        if fn:
            self.immediate = fn.__dict__.get('immediate', False)
            return fn
        elif isinstance(num, (int, float)):
            return num
        elif word[0] in ['\'', '\"']:
            self.lexer.rewind(len(word[1:]))
            return self.lexer.charsTill(word[0])
        else:
            raise ValueError(errMsg.format(word))

    def startCompile(self):
        ''' Discretely replaces the data stack with compile buffer. '''
        self.stack = self.compileBuffer

    def stopCompile(self):
        ''' Discretely replaces the compile buffer with data stack. '''
        self.stack = self.dataStack

    def isCompiling(self):
        ''' Checks if the interpretor is in compile mode. '''
        return self.stack is self.compileBuffer
