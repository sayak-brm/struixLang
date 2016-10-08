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
    def __init__(self, terp, ENABLE_UNSAFE_OPERATIONS = False,
                 wordSets = ['output', 'control', 'math', 'stack',
                             'variables', 'text', 'unsafeOps', 'compiling']):
        self.unsafeOps = ENABLE_UNSAFE_OPERATIONS
        for wordSet in wordSets:
            terp.addWords(eval('self.words4{}()'.format(wordSet)))

    @staticmethod
    def words4output():
        ''' Provides Words for output operations. '''
        def PRINT(terp):
            ''' Pops & Displays the Top of Stack (ToS). '''
            if terp.stack.__len__() < 1:
                raise IndexError('Not enough items on stack.')
            print(terp.stack.pop())
        def PSTACK(terp):
            ''' Displays the complete stack. '''
            stackList = terp.stack
            stackList.reverse()
            print('\n'.join(str(val) for val in stackList))
        return {
            "PRINT":  PRINT,
            "PSTACK": PSTACK
            }

    @staticmethod
    def words4control():
        ''' Provides Words for controlling execution. '''
        def RAISE(terp):
            error = terp.stack.pop()
            msg = terp.stack.pop()
            print('ERROR: {} - {}'.format(error, msg))
            try:
                exec('raise {}(\'{}\')'.format(error, msg))
            except NameError:
                raise RuntimeError('{} - {}'.format(error,
                                                    msg))from exc
                
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
                if terp.stack.__len__() < 2:
                    raise IndexError('Not enough items on stack.')
                n1 = terp.stack.pop()
                n2 = terp.stack.pop()
                terp.stack.append(eval(str(n1) + '{}'.format(op) + str(n2)))
            return CALC
        ops = ['+', '-', '*', '**',
               '/', '//', '%', '@',
               '<<', '>>', '&', '|',
               '^', '~', '<', '>',
               '<=', '>=', '==', '!=']
        return dict(zip(ops, [CALCGEN(op) for op in ops]))

    @staticmethod
    def words4stack():
        ''' Provides Words for Stack Operations. '''
        def DUP(terp):
            ''' Duplicate Top of Stack (ToS). '''
            if terp.stack.__len__() < 1:
                raise IndexError('Not enough items on stack.')
            terp.stack.append(terp.stack[-1])
        def DROP(terp):
            ''' Remove Top of Stack (ToS). '''
            if terp.stack.__len__() < 1:
                raise IndexError('Not enough items on stack.')
            terp.stack.pop()
        def SWAP(terp):
            ''' Exchange positions of ToS and second item on stack (2oS). '''
            if terp.stack.__len__() < 2:
                raise IndexError('Not enough items on stack.')
            tos = terp.stack.pop()
            _2os = terp.stack.pop()
            terp.stack.append(tos)
            terp.stack.append(_2os)
        def OVER(terp):
            ''' Copy 2oS on top of stack. '''
            if terp.stack.__len__() < 2:
                raise IndexError('Not enough items on stack.')
            tos = terp.stack.pop()
            _2os = terp.stack.pop()
            terp.stack.append(_2os)
            terp.stack.append(tos)
            terp.stack.append(_2os)
        def ROT(terp):
            ''' Copy 3oS on top of stack. '''
            if terp.stack.__len__() < 3:
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
    def words4variables():
        def VAR(terp):
            class Variable:
                def __init__(self, val=None):
                    self.value = val
                def access(self, terp):
                    terp.stack.append(self)
            name = terp.lexer.nextWord()
            if name is '':
                raise SyntaxError('Invalid Syntax')
            var = Variable()
            terp.define(name, var.access)
        def CONST(terp):
            class Constant:
                def __init__(self, val):
                    object.__setattr__(self, 'val', val)
                def __setattr__(self, name, val):
                    if name is 'val':
                        raise AttributeError('Constant Attribute.')
                    object.__setattr__(self, name, val)
                def access(self, terp):
                    terp.stack.append(self.val)
            name = terp.lexer.nextWord()
            val = terp.lexer.nextWord()
            if name is '' or val is '':
                raise SyntaxError('Invalid Syntax')
            const = Constant(val)
            terp.define(name, const.access)
        def STORE(terp):
            if terp.stack.__len__() < 2:
                raise IndexError('Not enough items on stack.')
            val = terp.stack.pop()
            ref = terp.stack.pop()
            ref.value = val
        def FETCH(terp):
            if terp.stack.__len__() < 1:
                raise IndexError('Not enough items on stack.')
            ref = terp.stack.pop()
            terp.stack.append(ref.value)
        CONST.__dict__['immediate'] = True
        VAR.__dict__['immediate'] = True
        return {
            "VAR":   VAR,
            "CONST": CONST,
            "STORE": STORE,
            "FETCH": FETCH
            }
    @staticmethod
    def words4text():
        def COMMENT(terp):
            terp.lexer.clear()
        def STRING(terp, quote):
            return terp.lexer.charsTill(quote)
        STRING.__dict__['immediate'] = True
        COMMENT.__dict__['immediate'] = True
        return {
            "#":       COMMENT,
            "STRING":  STRING
            }

    def words4unsafeOps(self):
        def PYEXEC(terp):
            if not self.unsafeOps:
                raise PermissionError('Unsafe Operations are disabled.')
            exec(terp.stack.pop())
        def PYEVAL(terp):
            if not self.unsafeOps:
                raise PermissionError('Unsafe Operations are disabled.')
            terp.stack.append(eval(terp.stack.pop()))
        def PYLITEVAL(terp):
            terp.stack.append(__import__('ast').literal_eval(terp.stack.pop()))
        return {
            "PYEVAL":    PYEVAL,
            "PYEXEC":    PYEXEC,
            "PYLITEVAL": PYLITEVAL
            }
    @staticmethod
    def words4compiling():
        def DEF(terp):
            name = terp.lexer.nextWord()
            if name is '':
                raise SyntaxError('Invalid Syntax')
            terp.newWord = name
            terp.startCompile()
        def END(terp):
            def makeWord(code):
                def word(terp):
                    pointer = 0
                    while pointer < len(code):
                        terp.interpret(code[pointer])
                        pointer += 1
                return word
            code = terp.stack[:]
            terp.stack = []
            terp.define(terp.newWord, makeWord(code))
            terp.stopCompile()
        DEF.__dict__['immediate'] = True
        END.__dict__['immediate'] = True
        return {
            "DEF": DEF,
            "END": END
            }
            
