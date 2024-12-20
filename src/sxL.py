##   Copyright 2017 Sayak Brahmachari
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

import sys

from struixLang import struixTerp, struixPrimitives

f = open(sys.argv[1], 'r')
terp = struixTerp.Terp()
struixPrimitives.AddWords(terp)
terp.run(f.read())
f.close()
