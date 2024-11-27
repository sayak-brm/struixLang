##   Copyright 2016-24 Sayak Brahmachari

import traceback
from . import struixLexer

class Terp:
    ''' Interpreter for struixLang. '''
    
    def __init__(self):
        self.scopedDictionaries = [{}]
        self.dictionary = self.scopedDictionaries[0]
        self.immediate = False
        self.immediate_compiled = False
        self.wordNameStack = []
        self.scopedStacks = [[]]
        self.stack = self.scopedStacks[0]
        self.areScopesFn = [True]
        self.lexerQueue = []
        self.lexer = struixLexer.Lexer("")

    def addWords(self, newWords):
        ''' Adds given words to interpreter dictionary. '''
        self.dictionary.update(newWords)

    def define(self, word, code, is_global=True):
        ''' Defines (or redefines) a word in the dictionary. '''
        if is_global:
            for scoped_dict in reversed(self.scopedDictionaries):
                if word in scoped_dict.keys():
                    scoped_dict[word] = code
                    return
        self.dictionary[word] = code

    def lookup(self, word):
        ''' Returns a word with given key from dictionary. '''
        if not isinstance(word, str): return None
        for scoped_dict in reversed(self.scopedDictionaries):
            if word in scoped_dict.keys():
                return scoped_dict[word]
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
        ''' Starts processing of struixLang code with enhanced error reporting. '''
        try:
            self.lexerQueue.append(self.lexer)
            self.lexer = struixLexer.Lexer(text)

            while self.lexer.peekWord():
                try:
                    word_text = self.lexer.nextWord()
                    word = self.compile(word_text)
                    self.interpret(word)
                except Exception as e:
                    # Include the word and position in the exception message
                    traceback.print_exc()
                    line_number = self.lexer.line_number
                    column_number = self.lexer.column_number - len(word_text)
                    raise Exception(f"Error processing word '{word_text}' at line {line_number}, column {column_number}: {e}") from e
        finally:
            self.lexer = self.lexerQueue.pop()

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

    def compile(self, word, errMsg='Unknown Word: {}'):
        """ Compiles struixLang code to its internal representation. """
        import types
        num = self.parseNumber(word) if not isinstance(word, (types.FunctionType, types.MethodType)) else None
        fn = word if isinstance(word, (types.FunctionType, types.MethodType)) else self.lookup(word)

        if fn:
            self.immediate = fn.__dict__.get('immediate', False) and self.getScopeDepth() > 1
            self.immediate_compiled |= self.immediate
            # if self.immediate_compiled:
            #     print(f"Warning: Immediate word '{word}' is being {'compiled' if self.isCompiling() else 'interpreted'}.")
            return fn
        elif isinstance(num, (int, float)):
            return num
        elif isinstance(word, str) and word.startswith(('"""', "'''")):
            return self.lexer.charsTillMultiline(word[:3])  # Handle multi-line strings
        elif (word := str(word))[0] in ['\'', '\"']:
            word = str(word)
            if word[-1] == word[0]:
                return word[1:-1]
            return word[1:] + self.lexer.charsTill(word[0])
        else:
            # if self.isCompiling() and not dehydrated:
            #     def dehydrated_compile(terp):
            #         print(f"Hydrated lookup: {word} {terp.lexer.line_number} {terp.lexer.column_number}")
            #         fn = terp.compile(word, 'Runtime Error: Undefined symbol: {}', dehydrated=True)
            #         fn(terp)
            #     dehydrated_compile.__dict__['dehydrated'] = True
            #     return dehydrated_compile
            raise ValueError(errMsg.format(word))

    def newBlockScope(self):
        ''' Switches to a new block scope buffer. '''
        self.areScopesFn.append(True)
        self.newScope()

    def newAotScope(self):
        ''' Switches to a new AOT scope buffer. '''
        self.areScopesFn.append(False)
        self.newScope()

    def newScope(self):
        ''' Discretely replaces the data stack with a new scope buffer. '''

        # Push words dict to new AOT/BLOCK scope
        self.scopedDictionaries.append({})
        self.dictionary = self.scopedDictionaries[-1]

        # Push data stack to new AOT/BLOCK scope
        self.scopedStacks.append([])
        self.stack = self.scopedStacks[-1]

    def popScope(self):
        ''' Discretely replaces the compile buffer with a new scope stack. '''
        if self.getScopeDepth() > 1:
            self.immediate_compiled = False
            self.areScopesFn.pop()

            # Pop and garbage collect words dict from AOT/BLOCK scope
            self.scopedDictionaries.pop()
            self.dictionary = self.scopedDictionaries[-1]

            # Pop and return data stack from AOT/BLOCK scope
            dataStack = self.scopedStacks.pop()
            self.stack = self.scopedStacks[-1]
            return dataStack
        return self.scopedStacks[0]

    def getScopeDepth(self):
        ''' Returns the depth of the current scope. '''
        return len(self.areScopesFn)

    def isCompiling(self):
        ''' Checks if the interpreter is in compile mode. '''
        return not self.areScopesFn[-1]
