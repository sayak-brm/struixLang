##   Copyright 2016-17 Sayak Brahmachari
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

import struixLexer

class Terp:
    ''' Interpreter for struixLang. '''

    ENABLE_UNSAFE_OPERATIONS = True
    
    def __init__(self):
        self.dictionary = {}
        self.immediate = False
        self.newWord = None
        self.compileStack = [[]]
        self.stack = self.compileStack[0]
        
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
        self.lexer = struixLexer.Lexer(text)
        word = None
        while self.lexer.peekWord():
            word = self.compile(self.lexer.nextWord())
            self.interpret(word)

    def interpret(self, word):
        ''' Executes struixLang code. '''
        import types
        if not self.isCompiling() or self.immediate:
            if isinstance(word, (types.FunctionType, types.MethodType)):
                word(self)
            else:
                self.stack.append(word)
            self.immediate = False
        else:
            self.stack.append(word)
            
    def interpret_old(self, word):
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
        self.compileStack.append([])
        self.stack = self.compileStack[-1]

    def stopCompile(self):
        ''' Discretely replaces the compile buffer with data stack. '''
        if len(self.compileStack) > 1:
            dataStack = self.compileStack.pop()
            self.stack = self.compileStack[-1]
            return dataStack
        return self.compileStack[0]

    def isCompiling(self):
        ''' Checks if the interpretor is in compile mode. '''
        return True if len(self.compileStack) > 1 else False
