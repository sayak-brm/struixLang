<img src="https://github.com/sayak-brm/struixLang/blob/master/logo/struixLANG.PNG?raw=true" alt="struixLang" height="60"/>

##### A stack-based programming language implemented in Python3.

###### Copyright 2016 [Sayak Brahmachari](https://sayak-brm.github.io/) @ [MicroControlled](http://mctrl.ml/). Licenced under [Apache v2.0](https://opensource.org/licenses/Apache-2.0). 

[![Test Coverage](https://codeclimate.com/github/sayak-brm/struixLang/badges/coverage.svg)](https://codeclimate.com/github/sayak-brm/struixLang/coverage) [![Code Climate](https://codeclimate.com/github/sayak-brm/struixLang/badges/gpa.svg)](https://codeclimate.com/github/sayak-brm/struixLang) [![Issue Count](https://codeclimate.com/github/sayak-brm/struixLang/badges/issue_count.svg)](https://codeclimate.com/github/sayak-brm/struixLang) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/5830dba3f80f44359b3e60807b0e591b/badge.svg)](https://www.quantifiedcode.com/app/project/5830dba3f80f44359b3e60807b0e591b)

----

## Intro:

**struixLang** implements a **stack**, which is a list of objects which the program operates on.

Also, a **dictionary** is present, containing **words** *(functions/subroutines)* which may be executed in a program.*

Several primitive *(read:built-in)* words are pre-defined and mechanisms to define new *user-defined* words within struixLang itself are in place.

----

## Data Model:

### Supported Types:

struixLang supports the following data types:

* Integers,
* Floats,
* Strings,
* Boolean,
* Lists, and
* Words.

However, the current implementation can utilize words which put or use values of any type supported in Python 3.

Also note that as struixLang is a *Homoiconic Language*, it can treat code as data and data as code, hence **words** are included in the list above.