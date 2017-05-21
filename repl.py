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

import code
import sys

import struixTerp
import struixPrimitives

sys.ps1 = "sxL> "
sys.ps2 = "    ...> "
banner = "struixLang REPL v1.0.20170521a.\nUse 'exit' to close the prompt."

class Shell(code.InteractiveConsole):
    ''' Provides a REPL for struixLang. '''
    def runsource(self, source, filename="<stdin>"):
        try:
            if '\n' in source:
                terp.run(source.splitlines()[-1])
            else: terp.run(source)
        except:
#            self.showsyntaxerror(filename)
            self.showtraceback()
        if terp.isCompiling(): return True
        return False

terp = struixTerp.Terp()
struixPrimitives.AddWords(terp)
Shell().interact(banner)
