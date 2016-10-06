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
    def __init__(self, terp):
        wordSets = ['output', 'control', 'math', 'stack', 'variables', 'text']
        for wordSet in wordSets:
            terp.addWords(eval('self.words4{}()'.format(wordSet)))

    @staticmethod
    def words4output():
        ''' Provides Words for output operations. '''
        def PRINT(terp):
            ''' Pops & Displays the Top of Stack (ToS). '''
            if terp.stack.__len__() < 1: raise IndexError('Not enough items on stack')
            print(terp.stack.pop())
        def PSTACK(terp):
            ''' Displays the complete stack. '''
            print("\n".join(str(val) for val in terp.stack))
        return {
            "PRINT":  PRINT,
            "PSTACK": PSTACK
            }

    @staticmethod
    def words4control():
        ''' Provides Words for controlling execution. '''
        def EXIT(terp):
            ''' Terminates the execution. '''
            exit()
        return {
            "EXIT": EXIT
            }

    @staticmethod
    def words4math():
        ''' Provides Words for several mathematical and logical operations. '''
        def CALCGEN(op):
            ''' Generates Words for a specefic operation. '''
            def CALC(terp):
                if terp.stack.__len__() < 2: raise IndexError('Not enough items on stack')
                terp.stack.append(eval('terp.stack.pop(){}terp.stack.pop()'.format(op)))
            return CALC
        ops = ['+', '-', '*', '/', '%', '//', '**', '|', '^', '&', '<<', '>>']
        return dict(zip(ops, [CALCGEN(op) for op in ops]))

    @staticmethod
    def words4stack():
        ''' Provides Words for Stack Operations. '''
        def DUP(terp):
            ''' Duplicate Top of Stack (ToS). '''
            if terp.stack.__len__() < 1: raise IndexError('Not enough items on stack')
            terp.stack.append(terp.stack[-1])
        def DROP(terp):
            ''' Remove Top of Stack (ToS). '''
            if terp.stack.__len__() < 1: raise IndexError('Not enough items on stack')
            terp.stack.pop()
        def SWAP(terp):
            ''' Exchange positions of ToS and second item on stack (2oS). '''
            if terp.stack.__len__() < 2: raise IndexError('Not enough items on stack')
            tos = terp.stack.pop()
            _2os = terp.stack.pop()
            terp.stack.append(tos)
            terp.stack.append(_2os)
        def OVER(terp):
            ''' Copy 2oS on top of stack. '''
            if terp.stack.__len__() < 2: raise IndexError('Not enough items on stack')
            tos = terp.stack.pop()
            _2os = terp.stack.pop()
            terp.stack.append(_2os)
            terp.stack.append(tos)
            terp.stack.append(_2os)
        def ROT(terp):
            ''' Copy 3oS on top of stack. '''
            if terp.stack.__len__() < 3: raise IndexError('Not enough items on stack')
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
        class Variable:
            def __init__(self, val=None):
                self.value = val
            def access(self, terp):
                terp.stack.append(self)
        class Constant:
            def __init__(self, val):
                import random
                self.__vHjp3nfr6N3JJs9y = random.randint(-1000, 0)
                self.__vHjp3nG4qN3JJs9y = random.uniform(-100, 100)
                self.__vH5WKNf5y96k3a9y = random.randint(0, 1000)
                self.__vHjp3nG4qN3JJs9y = val
                self.__vHAKUW42nQaCpm9y = random.uniform(-1000, 0)
                self.__vH5WKNG4y96k3a9y = random.randint(-100, 100)
                self.__vHjp3nfr6NEJJs9y = random.uniform(0, 1000)
                self.__dict__['_Constant__vHjp3n4GqN3JJs9y'] = self.__dict__.pop('_Constant__vHjp3nG4qN3JJs9y')
            def access(self, terp):
                import random, string
                var = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16))
                self.__dict__['_Constant__{}'.format(var)] = self.__dict__.pop('_Constant__vHjp3n4GqN3JJs9y')
                terp.stack.append(eval('self._Constant__{}'.format(var)))
                self.__dict__['_Constant__vHjp3n4GqN3JJs9y'] = self.__dict__.pop('_Constant__{}'.format(var))
        def VAR(terp):
            name = terp.lexer.nextWord()
            if name is None: raise SyntaxError('Invalid Syntax')
            var = Variable()
            terp.define(name, var.access)
        def CONST(terp):
            name = terp.lexer.nextWord()
            val = terp.lexer.nextWord()
            if name is None or val is None: raise SyntaxError('Invalid Syntax')
            const = Constant(val)
            terp.define(name, const.access)
        def STORE(terp):
            if terp.stack.__len__() < 2: raise IndexError('Not enough items on stack')
            val = terp.stack.pop()
            ref = terp.stack.pop()
            ref.value = val
        def FETCH(terp):
            if terp.stack.__len__() < 1: raise IndexError('Not enough items on stack')
            ref = terp.stack.pop()
            terp.stack.append(ref.value)
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
        def STRING(terp):
            collector = ''
            done = False
            while not done:
                nextWord = terp.lexer.nextWord()
                if nextWord is None: raise SyntaxError('Invalid Syntax')
                if nextWord[-1] is '\"': done = True
                collector += nextWord
                if done: collector = collector[0:-1]
                else: collector += ' '
            terp.stack.append(collector)
        return {
            "#":  COMMENT,
            "\"": STRING
            }
