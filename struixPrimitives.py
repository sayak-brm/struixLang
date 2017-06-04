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

class AddWords:
    ''' Provides Built-in Words for the struixLang Interpreter. '''
    def __init__(self, terp, ENABLE_UNSAFE_OPERATIONS = False, wordSets = None):
        ''' Collects the primitive words and updates the dicionary. '''
        def IMPORT(terp):
            name = terp.lexer.nextWord()
            if name is '':
                raise SyntaxError('Invalid Syntax')
            try: lib = open('./lib/{}.sxLib'.format(name), 'r')
            except: raise ImportError('No library named {}.'.format(name))
            terp.run(lib.read())
            lib.close()
        IMPORT.__dict__['immediate'] = True
        terp.addWords({'IMPORT': IMPORT})
        self.unsafeOps = ENABLE_UNSAFE_OPERATIONS
        self.importWordSets(terp, wordSets)

    def importWordSets(self, terp, wordSets):
        if wordSets is None:
            wordSets = ['lists',  'execution', 'math', 'stack', 'values',
                        'values', 'functions', 'text', 'logic', 'control',
                        'io',  'pythonOps', 'shorthand']
        for wordSet in wordSets:
            try:
                terp.addWords(eval('self.words4{}()'.format(wordSet)))
            except AttributeError:
                terp.run('IMPORT {}'.format(wordSet))

    @staticmethod
    def makeWord(code, imm=False):
        ''' Makes an executable word from list. '''
        def word(terp):
            ''' Template for a list executor. '''
            if isinstance(code, list):
                pointer = 0
                while pointer < len(code):
                    if imm:
                        i=code[pointer].__dict__.get('immediate', False)
                        terp.immediate = i
                    terp.interpret(code[pointer])
                    pointer += 1
            elif isinstance(code, (types.FunctionType, types.MethodType)):
                code(terp)
            else:
                raise TypeError('Expected List')
        return word

    @staticmethod
    def getVal(terp, val, lvl):
        ''' Parses and gets next value from lexer. '''
        import types
        val = terp.compile(val)
        if isinstance(val, (types.FunctionType, types.MethodType)):
            ''' Evaluates before accepting. '''
            val(terp)
            while len(terp.compileStack) > lvl:
                word = terp.lexer.nextWord()
                terp.interpret(terp.compile(word))
            if len(terp.stack) < 1:
                while len(terp.compileStack) > lvl:
                    terp.compileStack.pop()
                raise SyntaxError('Invalid Syntax.')
            val = terp.stack.pop()
        return val
    
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
            stackList = terp.stack[:]
            stackList.reverse()
            print('\n'.join(repr(val) for val in stackList))
        def INPUT(terp):
            ''' Accepts value from user. '''
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
    
    def words4values(self):
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
            import types
            name = terp.lexer.nextWord()
            lvl = len(terp.compileStack)
            val = self.getVal(terp, terp.lexer.nextWord(), lvl)
            if name is '' or val is '':
                raise SyntaxError('Invalid Syntax')
            elif name in terp.dictionary:
                raise SyntaxError('Constant value set')
            const = Constant(val)
            terp.define(name, const.access)
        def ASSIGN(terp):
            ''' Helps storing values to variables. (INFIX) '''
            import types
            nxt = terp.lexer.nextWord()
            if nxt is '':
                raise SyntaxError('Invalid Syntax')
            lvl = len(terp.compileStack)
            val = self.getVal(terp, nxt, lvl)
            def helper(terp):
                if len(terp.stack) < 1:
                    raise IndexError('Not enough items on stack.')
                ref = terp.stack.pop()
                ref.val = val
            if not terp.isCompiling():
                helper(terp)
            else:
                terp.stack.append(helper)
        def STORE(terp):
            ''' Helps storing values to variables. (POSTFIX) '''
            import types
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
        ASSIGN.__dict__['immediate'] = True
        return {
            "VAR":   VAR,
            "CONST": CONST,
            "FETCH": FETCH,
            "=":     ASSIGN,
            "STORE": STORE #,
#            "@":     FETCH
            }
    
    @staticmethod
    def words4text():
        ''' Adds words for handling of comments. '''
        def COMMENT(terp):
            ''' Adds support for comments. '''
            terp.lexer.clearLine()
        COMMENT.__dict__['immediate'] = True
        return {
            "#":       COMMENT
            }

    def words4pythonOps(self):
        ''' Provides interfaces to the Python backend. '''
        def REQUESTUNSAFE(terp):
            if not self.unsafeOps:
                ans = input("Enter Y to allow potentially unsafe operations:")
                self.unsafeOps = True if ans.upper() == 'Y' else False
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
        def PYIMPORT(terp):
            ''' Evaluates value of Python code. '''
            if not self.unsafeOps:
                raise PermissionError('Unsafe Operations are disabled.')
            module = terp.stack.pop()
            exec('global {m}\nimport {m}'.format(m=module))
        def PYLITEVAL(terp):
            ''' Evaluates value of Python expressions. '''
            terp.stack.append(__import__('ast').literal_eval(terp.stack.pop()))
        return {
            "PYEVAL":        PYEVAL,
            "PYEXEC":        PYEXEC,
            "PYLITEVAL":     PYLITEVAL,
            "PYIMPORT":      PYIMPORT,
            "REQUESTUNSAFE": REQUESTUNSAFE
            }
    
    def words4functions(self):
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
            if terp.immediate_compiled: return IMMEND(terp)
            code = terp.stopCompile()
            terp.define(terp.newWord, self.makeWord(code))
            terp.newWord = None
        def IMMEND(terp):
            ''' Marks end of immediate user-defined words. '''
            code = terp.stopCompile()
            word = self.makeWord(code, True)
            word.__dict__['immediate'] = True
            terp.define(terp.newWord, word)
            terp.newWord = None
        def NEXT(terp):
            ''' Appends next word to stack and skips it during execution. '''
            def helper(terp):
                lvl = len(terp.compileStack)
                nxt = terp.lexer.nextWord()
                print(nxt)
                val = self.getVal(terp, nxt, lvl)
                terp.stack.append(val)
            helper.__dict__['immediate'] = True
            if terp.newWord == None:
                helper(terp)
            else:
                terp.stack.append(helper)
        NEXT.__dict__['immediate'] = True
        DEF.__dict__['immediate'] = True
        END.__dict__['immediate'] = True
        return {
            "DEF":  DEF,
            "END":  END,
            "NEXT": NEXT # ,
#            ":":   DEF,
#            ";":   END
            }

    @staticmethod
    def words4lists():
        ''' Words for list management. '''
        def LIST(terp):
            ''' Creates a list. '''
            terp.startCompile()
        def LIST_END(terp):
            ''' Marks end of list. '''
            lst = []
            lst += terp.stopCompile()
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
        LIST_END.__dict__['immediate'] = True
        return {
            "[":      LIST,
            "]":      LIST_END,
            "LENGTH": LENGTH,
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
            import types
            if len(terp.stack) < 1:
                raise IndexError('Not enough items on stack.')
            code = terp.stack.pop()
            if isinstance(code, (types.FunctionType, types.MethodType)):
                code(terp)
            if isinstance(code, list):
                terp.interpret(self.makeWord(code))
        def TIMES(terp):
            ''' Iterating structure like for-loop. '''
            if len(terp.stack) < 2:
                raise IndexError('Not enough items on stack.')
            n = terp.stack.pop()
            code = terp.stack.pop()
            word = self.makeWord(code)
            if n == float('inf'):
                while True:
                    word(terp)
            else:
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
