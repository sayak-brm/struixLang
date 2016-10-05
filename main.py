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

import primitives

class Lexer:
    def __init__(self, text):
        self.words = text.split()
        self.n = 0
        
    def nextWord(self):
        if self.n >= self.words.__len__(): return
        self.n += 1
        return self.words[self.n-1]
    
    def peekWord(self):
        if self.n >= self.words.__len__(): return
        return self.words[self.n]

class Terp:
    def __init__(self):
        self.dictionary = {}
        self.stack = []
        
    def addWords(self, newWords):
        self.dictionary.update(newWords)
        
    def run(self, text):
        lexer = Lexer(text) #TODO: Make lexer an obj property for read aheads.
        word = None
        num = None
        while lexer.peekWord():
            word = lexer.nextWord().upper()
            try: num = int(word)
            except ValueError:
                try: num = float(word)
                except ValueError: num = None
            if word in self.dictionary.keys():
                self.dictionary[word](self)
            elif num is not None:
                self.stack.append(num)
            else:
                raise ValueError('Unknown Word: {}'.format(word))

terp = Terp()
primitives.AddWords(terp)
while True:
    terp.run(input('>>> '))
