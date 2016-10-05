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
    def __init__(self, terp):
        wordSets = ['display', 'control', 'operations', 'stack']
        for wordSet in wordSets:
            exec('terp.addWords(self.words4{}())'.format(wordSet))
        
    def words4display(self):
        def PRINT(terp):
            if terp.stack.__len__() < 1: raise IndexError('Not enough items on stack')
            print(terp.stack.pop())
        def PSTACK(terp):
            print(" ".join(str(val) for val in terp.stack))
        return {
            "PRINT":  PRINT,
            "PSTACK": PSTACK
            }
    
    def words4control(self):
        def EXIT(terp):
            exit()
        return {
            "EXIT": EXIT
            }
    
    def words4operations(self):
        def CALCGEN(op):
            def CALC(terp):
                if terp.stack.__len__() < 2: raise IndexError('Not enough items on stack')
                exec('terp.stack.append(terp.stack.pop(){}terp.stack.pop())'.format(op))
            return CALC
        ops = ['+', '-', '*', '/', '%', '//', '**', '|', '^', '&', '<<', '>>']
        return dict(zip(ops, [CALCGEN(op) for op in ops]))

    def words4stack(self):
        def DUP(terp):
            ''' Duplicate Top of Stack (ToS). '''
            if terp.stack.__len__() < 1: raise IndexError('Not enough items on stack')
            terp.stack.append(terp.stack[-1])
        def DROP(terp):
            ''' Remove Top of Stack (ToS). '''
            if terp.stack.__len__() < 1: raise IndexError('Not enough items on stack')
            terp.stack.pop()
        def SWAP(terp):
            ''' Exchange positions of TOS and second item on stack (2OS). '''
            if terp.stack.__len__() < 2: raise IndexError('Not enough items on stack')
            tos = terp.stack.pop()
            _2os = terp.stack.pop()
            terp.stack.append(tos)
            terp.stack.append(_2os)
        def OVER(terp):
            ''' Copy 2OS on top of stack. '''
            if terp.stack.__len__() < 2: raise IndexError('Not enough items on stack')
            tos = terp.stack.pop()
            _2os = terp.stack.pop()
            terp.stack.append(_2os)
            terp.stack.append(tos)
            terp.stack.append(_2os)
        def ROT(terp):
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
