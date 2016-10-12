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

class AddWords:
    ''' Provides Built-in Words for the struixLang Interpreter. '''
    def __init__(self, terp, ENABLE_UNSAFE_OPERATIONS = False, wordSets = None):
        ''' Collects the primitive words and ipdates the dicionary. '''
        if wordSets is None:
            wordSets = ['lists',  'execution', 'math', 'stack', 'values',
                        'values', 'compiling', 'text', 'logic', 'control',
                        'io',  'pythonOps']
        self.unsafeOps = ENABLE_UNSAFE_OPERATIONS
        for wordSet in wordSets:
            terp.addWords(eval('self.words4{}()'.format(wordSet)))

    @staticmethod
    def makeWord(code):
        ''' Makes an executable word from list. '''
        def word(terp):
            ''' Template for a list executor. '''
            if isinstance(code, list):
                pointer = 0
                while pointer < len(code):
                    terp.interpret(code[pointer])
                    pointer += 1
            else:
                raise TypeError('Expected List')
        return word

    @staticmethod
    def words4io():
        ''' Provides Words for output operations. '''
        def PRINT(terp):
            ''' Pops & Displays the Top of Stack (ToS). '''
            if len(terp.stack) < 1:
                raise IndexError('Not enough items on stack.')
            print(terp.stack.pop())
        def PSTACK(terp):
            ''' Displays the complete stack. '''
            stackList = terp.stack
            stackList.reverse()
            print('\n'.join(repr(val) for val in stackList))
        def INPUT(terp):
            val = input()
            num = terp.parseNumber(val)
            if num:
                val = num
            terp.stack.append(val)
        return {
            "PRINT":  PRINT,
            "PSTACK": PSTACK,
            "INPUT":  INPUT # ,
#            ".":      PRINT,
#            ".S":     PSTACK
            }

    @staticmethod
    def words4execution():
        ''' Provides Words for controlling execution. '''
        def RAISE(terp):
            ''' Raises an error. '''
            error = terp.stack.pop()
            msg = terp.stack.pop()
            print('ERROR: {} - {}'.format(error, msg))
            try:
                exec('raise {}(\'{}\')'.format(error, msg))
            except NameError:
                raise RuntimeError('{} - {}'.format(error, msg))
        def EXIT(terp):
            ''' Terminates the execution. '''
            exit()
        return {
            "EXIT":  EXIT,
            "RAISE": RAISE
            }

    @staticmethod
    def words4math():
        ''' Provides Words for several operations. '''
        def CALCGEN(op):
            ''' Generates Words for a specific operation. '''
            def CALC(terp):
                ''' Template word for operations. '''
                if len(terp.stack) < 2:
                    raise IndexError('Not enough items on stack.')
                n1 = terp.stack.pop()
                n2 = terp.stack.pop()
                terp.stack.append(eval(repr(n2) + ' ' + op + ' ' + repr(n1)))
            return CALC
        ops = ['+',  '-',  '*',  '**',
               '/',  '//', '%',  '@',
               '<<', '>>', '&',  '|',
               '^',  '~',  '<',  '>',
               '<=', '>=', '==', '!=',
               'in', 'is', 'or', 'and']
        return dict(zip([op.upper() for op in ops], [CALCGEN(op) for op in ops]))

    @staticmethod
    def words4stack():
        ''' Provides Words for Stack Operations. '''
        def DUP(terp):
            ''' Duplicate Top of Stack (ToS). '''
            if len(terp.stack) < 1:
                raise IndexError('Not enough items on stack.')
            terp.stack.append(terp.stack[-1])
        def DROP(terp):
            ''' Remove Top of Stack (ToS). '''
            if len(terp.stack) < 1:
                raise IndexError('Not enough items on stack.')
            terp.stack.pop()
        def SWAP(terp):
            ''' Exchange positions of ToS and second item on stack (2oS). '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            tos = terp.stack.pop()
            _2os = terp.stack.pop()
            terp.stack.append(tos)
            terp.stack.append(_2os)
        def OVER(terp):
            ''' Copy 2oS on top of stack. '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            tos = terp.stack.pop()
            _2os = terp.stack.pop()
            terp.stack.append(_2os)
            terp.stack.append(tos)
            terp.stack.append(_2os)
        def ROT(terp):
            ''' Copy 3oS on top of stack. '''
            if len(terp.stack) < 3:
                raise IndexError('Not enough items on stack.')
            tos = terp.stack.pop()
            _2os = terp.stack.pop()
            _3os = terp.stack.pop()
            terp.stack.append(_2os)
            terp.stack.append(tos)
            terp.stack.append(_3os)
        return {
            "DUP":  DUP,
            "DROP": DROP,
            "SWAP": SWAP,
            "OVER": OVER,
            "ROT":  ROT
            }
    @staticmethod
    def words4values():
        ''' Provides support for variables and constants. '''
        def VAR(terp):
            ''' Provides creation of variables. '''
            class Variable:
                ''' Provides a template class for variables. '''
                def __init__(self, val=None):
                    ''' Initializes a Variable object. '''
                    self.val = val
                def access(self, terp):
                    ''' Puts a reference to the variable value on the stack. '''
                    terp.stack.append(self)
            name = terp.lexer.nextWord()
            if name is '':
                raise SyntaxError('Invalid Syntax')
            var = Variable()
            terp.define(name, var.access)
        def CONST(terp):
            ''' Provides creation of constants. '''
            class Constant:
                ''' Provides a template class with a write-once value. '''
                def __init__(self, val):
                    ''' Initializes a Constant object with a value. '''
                    object.__setattr__(self, 'val', val)
                def __setattr__(self, name, val):
                    ''' Provides a descriptor to prevent changing values. '''
                    if name is 'val':
                        raise AttributeError('Constant Attribute.')
                    object.__setattr__(self, name, val)
                def access(self, terp):
                    ''' Puts the value of the constant on the stack. '''
                    terp.stack.append(self.val)
            name = terp.lexer.nextWord()
            val = terp.lexer.nextWord()
            if name is '' or val is '':
                raise SyntaxError('Invalid Syntax')
            elif name in terp.dictionary:
                raise SyntaxError('Constant value set')
            const = Constant(val)
            terp.define(name, const.access)
        def STORE(terp):
            ''' Helps storing values to variables. '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            val = terp.stack.pop()
            ref = terp.stack.pop()
            ref.val = val
        def FETCH(terp):
            ''' Helps retrieviing values from variables. '''
            if len(terp.stack) < 1:
                raise IndexError('Not enough items on stack.')
            ref = terp.stack.pop()
            terp.stack.append(ref.val)
        CONST.__dict__['immediate'] = True
        VAR.__dict__['immediate'] = True
        return {
            "VAR":   VAR,
            "CONST": CONST,
            "STORE": STORE,
            "FETCH": FETCH # ,
#            "=":     STORE,
#            "@":     FETCH
            }
    
    @staticmethod
    def words4text():
        ''' Adds words for handling of comments. '''
        def COMMENT(terp):
            ''' Adds support for comments. '''
            terp.lexer.clear()
        COMMENT.__dict__['immediate'] = True
        return {
            "#":       COMMENT,
            "COMMENT": COMMENT
            }

    def words4pythonOps(self):
        ''' Provides interfaces to the Python backend. '''
        def PYEXEC(terp):
            ''' Executes Python code. '''
            if not self.unsafeOps:
                raise PermissionError('Unsafe Operations are disabled.')
            exec(terp.stack.pop())
        def PYEVAL(terp):
            ''' Evaluates value of Python code. '''
            if not self.unsafeOps:
                raise PermissionError('Unsafe Operations are disabled.')
            terp.stack.append(eval(terp.stack.pop()))
        def PYLITEVAL(terp):
            ''' Evaluates value of Python expressions. '''
            terp.stack.append(__import__('ast').literal_eval(terp.stack.pop()))
        return {
            "PYEVAL":    PYEVAL,
            "PYEXEC":    PYEXEC,
            "PYLITEVAL": PYLITEVAL
            }
    
    def words4compiling(self):
        ''' Supports creation of user-defined words. '''
        def DEF(terp):
            ''' Marks beginning of user-defined words. '''
            name = terp.lexer.nextWord()
            if name is '':
                raise SyntaxError('Invalid Syntax')
            terp.newWord = name
            terp.startCompile()
        def END(terp):
            ''' Marks end of user-defined words. '''
            code = terp.stack[:]
            terp.stack = []
            terp.define(terp.newWord, self.makeWord(code))
            terp.stopCompile()
        DEF.__dict__['immediate'] = True
        END.__dict__['immediate'] = True
        return {
            "DEF": DEF,
            "END": END # ,
#            ":":   DEF,
#            ";":   END
            }

    @staticmethod
    def words4lists():
        ''' Words for list management. '''
        def LIST(terp):
            ''' Creates a list. '''
            import types
            lst = []
            dataStack = terp.stack
            terp.stack = lst
            while True:
                nextWord = terp.lexer.nextWord()
                if nextWord == '':
                    terp.stack = dataStack
                    raise SyntaxError('Invalid Syntax')
                elif nextWord == ']':
                    break
                nextWord = terp.compile(nextWord)
                if isinstance(nextWord, types.FunctionType)\
                   and nextWord.__dict__.get('immediate', False):
                    nextWord(terp)
                else:
                    terp.stack.append(nextWord)
            terp.stack = dataStack
            terp.stack.append(lst)
        def LENGTH(terp):
            ''' Gives the length of a list. '''
            if len(terp.stack) < 1:
                raise IndexError('Not enough items on stack.')
            terp.stack.append(len(terp.stack.pop()))
        def ITEM(terp):
            ''' Gives an element of a list. '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            key = terp.stack.pop()
            terp.stack.append(terp.stack.pop()[key])
        LIST.__dict__['immediate'] = True
        return {
            "[":      LIST,
            "LENGTH": LENGTH,
            "LEN":    LENGTH,
            "ITEM":   ITEM
            }

    @staticmethod
    def words4logic():
        ''' Words for logical and boolean operations. '''
        def NOT(terp):
            ''' Provides logical operator NOT(!). '''
            if len(terp.stack) < 1:
                raise IndexError('Not enough items on stack.')
            terp.stack.append(not terp.stack.pop())
        def TRUE(terp):
            ''' Represents the boolean True. '''
            terp.stack.append(True)
        def FALSE(terp):
            ''' Represents the boolean False. '''
            terp.stack.append(False)
        return {
            "NOT":   NOT,
            "TRUE":  TRUE,
            "FALSE": FALSE
            }

    def words4control(self):
        ''' Provides control structures. '''
        def RUN(terp):
            ''' Provides execution of lists containing struixLang code. '''
            if len(terp.stack) < 1:
                raise IndexError('Not enough items on stack.')
            terp.interpret(self.makeWord(terp.stack.pop()))
        def TIMES(terp):
            ''' Iterating structure like for-loop. '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            n = terp.stack.pop()
            code = terp.stack.pop()
            word = self.makeWord(code)
            for _ in range(n):
                word(terp)
        def IFTRUE(terp):
            ''' Performs a task on recieving TRUE. '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            code = terp.stack.pop()
            if terp.stack.pop():
                terp.interpret(self.makeWord(code))
        def IFFALSE(terp):
            ''' Performs a task on recieving FALSE. '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            code = terp.stack.pop()
            if not terp.stack.pop():
                terp.interpret(self.makeWord(code))
        def IFELSE(terp):
            ''' Performs different task for different boolean values. '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            code2 = terp.stack.pop()
            code1 = terp.stack.pop()
            if terp.stack.pop():
                terp.interpret(self.makeWord(code1))
            else:
                terp.interpret(self.makeWord(code2))
        def WHILE(terp):
            ''' Variable-iteration, entry-control loop. '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            code = self.makeWord(terp.stack.pop())
            cond = self.makeWord(terp.stack.pop())
            while True:
                cond(terp)
                if len(terp.stack) < 1:
                    raise IndexError('Not enough items on stack.')
                if not terp.stack.pop():
                    break
                code(terp)
        def DOWHILE(terp):
            ''' Variable-iteration, exit-control loop. '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            code = self.makeWord(terp.stack.pop())
            cond = self.makeWord(terp.stack.pop())
            while True:
                code(terp)
                cond(terp)
                if len(terp.stack) < 1:
                    raise IndexError('Not enough items on stack.')
                if not terp.stack.pop():
                    break
        return {
            "RUN":     RUN,
            "TIMES":   TIMES,
            "IFTRUE":  IFTRUE,
            "IFFALSE": IFFALSE,
            "IFELSE":  IFELSE,
            "WHILE":   WHILE,
            "DOWHILE": DOWHILE
            }
