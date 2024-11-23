##   Copyright 2016-24 Sayak Brahmachari

from . import struixLexer

class Terp:
    ''' Interpreter for struixLang. '''
    
    def __init__(self):
        self.dictionary = {}
        self.immediate = False
        self.immediate_compiled = False
        self.newWord = None
        self.compileStack = [[]]
        self.stack = self.compileStack[0]

    def addWords(self, newWords):
        ''' Adds given words to interpreter dictionary. '''
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
        ''' Starts processing of struixLang code with enhanced error reporting. '''
        self.lexer = struixLexer.Lexer(text)
        word = None
        while self.lexer.peekWord():
            try:
                word_text = self.lexer.nextWord()
                word = self.compile(word_text)
                self.interpret(word)
            except Exception as e:
                # Include the word and position in the exception message
                line_number = self.lexer.line_number
                column_number = self.lexer.column_number - len(word_text)
                raise Exception(f"Error processing word '{word_text}' at line {line_number}, column {column_number}: {e}") from e

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
        uword = word.upper() if isinstance(word, str) else word
        num = self.parseNumber(uword) if not isinstance(word, (types.FunctionType, types.MethodType)) else None
        fn = word if isinstance(uword, (types.FunctionType, types.MethodType)) else self.lookup(word)

        if fn:
            self.immediate = fn.__dict__.get('immediate', False)
            self.immediate_compiled |= self.immediate
            return fn
        elif isinstance(num, (int, float)):
            return num
        elif isinstance(uword, str) and uword.startswith(('"""', "'''")):
            return self.lexer.charsTillMultiline(uword[:3])  # Handle multi-line strings
        elif (uword := str(uword))[0] in ['\'', '\"']:
            word = str(word)
            if uword[-1] == uword[0]:
                return word[1:-1]
            return word[1:] + self.lexer.charsTill(word[0])
        else:
            raise ValueError(errMsg.format(word))

    def startCompile(self):
        ''' Discretely replaces the data stack with compile buffer. '''
        self.compileStack.append([])
        self.stack = self.compileStack[-1]

    def stopCompile(self):
        ''' Discretely replaces the compile buffer with data stack. '''
        if len(self.compileStack) > 1:
            self.immediate_compiled = False
            dataStack = self.compileStack.pop()
            self.stack = self.compileStack[-1]
            return dataStack
        return self.compileStack[0]

    def isCompiling(self):
        ''' Checks if the interpreter is in compile mode. '''
        return True if len(self.compileStack) > 1 else False
