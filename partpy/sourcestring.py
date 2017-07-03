"""SourceString stores the entire string to be parsed in memory and provides
some simple methods for retrieving and moving current position aswell as
methods for matching strings and patterns.
"""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'


class SourceString(object):
    """Stores the parse string and its length followed by current position
    in the string and if the end of the string has been reached.

    It also stores the current row and column position as manually counted.

    Provides multiple methods for matching strings and patterns and working
    with the source string.
    """
    def __init__(self, string=None):
        """Accepts a string or None by default. If a string is given then
        self.set_string(string) is run automatically. If you wish to load a
        file then create a SourceString object with no arguments and then use
        load_file or overload this function when inheriting from SourceString.
        """
        self.string = ''
        self.length = 0
        self.pos = 0
        self.col = 0
        self.row = 1
        self.eos = 0
        if string is not None:
            self.set_string(string)

    def load_file(self, filename):
        """Read in file contents and set the current string."""
        with open(filename, 'r') as sourcefile:
            self.set_string(sourcefile.read())

    def set_string(self, string):
        """Set the working string and its length then reset positions."""
        self.string = string
        self.length = len(string)
        self.reset_position()

    def add_string(self, string):
        """Add to the working string and its length and reset eos."""
        self.string += string
        self.length += len(string)
        self.eos = 0

    def reset_position(self):
        """Reset all current positions."""
        self.pos = 0
        self.col = 0
        self.row = 1
        self.eos = 0

    def has_space(self, length=1, offset=0):
        """Returns boolean if self.pos + length < working string length."""
        return self.pos + (length + offset) - 1 < self.length

    def eol_distance_next(self, offset=0):
        """Return the amount of characters until the next newline."""
        distance = 0
        for char in self.string[self.pos + offset:]:
            if char == '\n':
                break
            else:
                distance += 1
        return distance

    def eol_distance_last(self, offset=0):
        """Return the ammount of characters until the last newline."""
        distance = 0
        for char in reversed(self.string[:self.pos + offset]):
            if char == '\n':
                break
            else:
                distance += 1
        return distance

    def spew_length(self, length):
        """Move current position backwards by length."""
        pos = self.pos
        if not pos or length > pos:
            return None

        row = self.row
        for char in reversed(self.string[pos - length:pos]):
            pos -= 1
            if char == '\n':  # handle a newline char
                row -= 1

        self.pos = pos
        self.col = self.eol_distance_last()
        self.row = row

        if self.has_space():  # Set eos if there is no more space left.
            self.eos = 0

    def eat_length(self, length):
        """Move current position forward by length and sets eos if needed."""
        pos = self.pos
        if self.eos or pos + length > self.length:
            return None

        col = self.col
        row = self.row
        for char in self.string[pos:pos + length]:
            col += 1
            pos += 1
            if char == '\n':  # handle a newline char
                col = 0
                row += 1

        self.pos = pos
        self.col = col
        self.row = row

        if not self.has_space():  # Set eos if there is no more space left.
            self.eos = 1

    def eat_string(self, string):
        """Move current position by length of string and count lines by \n."""
        pos = self.pos
        if self.eos or pos + len(string) > self.length:
            return None

        col = self.col
        row = self.row
        for char in string:
            col += 1
            pos += 1
            if char == '\n':  # handle a newline char
                col = 0
                row += 1

        self.pos = pos
        self.col = col
        self.row = row

        if not self.has_space():  # Set eos if there is no more space left.
            self.eos = 1

    def eat_line(self):
        """Move current position forward until the next line."""
        if self.eos:
            return None
        eat_length = self.eat_length
        get_char = self.get_char
        has_space = self.has_space
        while has_space() and get_char() != '\n':
            eat_length(1)
        eat_length(1)

    def get_char(self, offset=0):
        """Return the current character in the working string."""
        if not self.has_space(offset=offset):
            return ''

        return self.string[self.pos + offset]

    def get_length(self, length, trim=0, offset=0):
        """Return string at current position + length.
        If trim == true then get as much as possible before eos.
        """
        if trim and not self.has_space(offset + length):
            return self.string[self.pos + offset:]
        elif self.has_space(offset + length):
            return self.string[self.pos + offset:self.pos + offset + length]
        else:
            return ''

    def get_string(self, offset=0):
        """Return non space chars from current position until a whitespace."""
        if not self.has_space(offset=offset):
            return ''

        # Get a char for each char in the current string from pos onward
        #  solong as the char is not whitespace.
        string = self.string
        pos = self.pos + offset
        for i, char in enumerate(string[pos:]):
            if char.isspace():
                return string[pos:pos + i]
        else:
            return string[pos:]

    def rest_of_string(self, offset=0):
        """A copy of the current position till the end of the source string."""
        if self.has_space(offset=offset):
            return self.string[self.pos + offset:]
        else:
            return ''

    def get_line(self, lineno):
        """Return any line as a SourceLine and None if lineno doesnt exist."""
        line = 0
        output = []
        for char in self.string:
            if line == lineno:
                output.append(char)
            elif line > lineno:
                break

            if char == '\n':
                line += 1
        if not output:
            return None

        return SourceLine(''.join(output), lineno)

    def get_current_line(self):
        """Return a SourceLine of the current line."""
        if not self.has_space():
            return None

        pos = self.pos - self.col
        string = self.string
        end = self.length

        output = []
        while pos < len(string) and string[pos] != '\n':
            output.append(string[pos])
            pos += 1
            if pos == end:
                break
        else:
            output.append(string[pos])

        if not output:
            return None

        return SourceLine(''.join(output), self.row)

    def get_lines(self, first, last):
        """Return SourceLines for lines between and including first & last."""
        line = 1
        linestring = []
        linestrings = []
        for char in self.string:
            if line >= first and line <= last:
                linestring.append(char)
                if char == '\n':
                    linestrings.append((''.join(linestring), line))
                    linestring = []
            elif line > last:
                break

            if char == '\n':
                line += 1
        if linestring:
            linestrings.append((''.join(linestring), line))
        elif not linestrings:
            return None

        return [SourceLine(string, lineno) for string, lineno in linestrings]

    def get_surrounding_lines(self, past=1, future=1):
        """Return the current line and x,y previous and future lines.
        Returns a list of SourceLine's.
        """
        string = self.string
        pos = self.pos - self.col
        end = self.length
        row = self.row

        linesback = 0
        while linesback > -past:
            if pos <= 0:
                break
            elif string[pos - 2] == '\n':
                linesback -= 1
            pos -= 1

        output = []
        linestring = []
        lines = future + 1
        while linesback < lines:
            if pos >= end:
                linestring.append(string[pos - 1])
                output.append(
                    SourceLine(''.join(linestring[:-1]), row + linesback))
                break
            elif string[pos] == '\n':
                linestring.append(string[pos])
                pos += 1
                output.append(
                    SourceLine(''.join(linestring), row + linesback))
                linesback += 1
                linestring = []
            linestring.append(string[pos])
            pos += 1

        return output

    def get_all_lines(self):
        """Return all lines of the SourceString as a list of SourceLine's."""
        output = []
        line = []
        lineno = 1
        for char in self.string:
            line.append(char)
            if char == '\n':
                output.append(SourceLine(''.join(line), lineno))
                line = []
                lineno += 1
        if line:
            output.append(SourceLine(''.join(line), lineno))

        return output

    def match_string(self, string, word=0, offset=0):
        """Returns 1 if string can be matches against SourceString's
        current position.

        If word is >= 1 then it will only match string followed by whitepsace.
        """
        if word:
            return self.get_string(offset) == string
        return self.get_length(len(string), offset) == string

    def match_any_string(self, strings, word=0, offset=0):
        """Attempts to match each string in strings in order.
        Will return the string that matches or an empty string if no match.

        If word arg >= 1 then only match if string is followed by a whitespace
        which is much higher performance.

        If word is 0 then you should sort the strings argument yourself by
        length.
        """
        if word:
            current = self.get_string(offset)
            return current if current in strings else ''
        current = ''

        currentlength = 0
        length = 0
        for string in strings:
            length = len(string)
            if length != currentlength:
                current = self.get_length(length, offset)
            if string == current:
                return string
        return ''

    def match_any_char(self, chars, offset=0):
        """Match and return the current SourceString char if its in chars."""
        if not self.has_space(offset=offset):
            return ''
        current = self.string[self.pos + offset]
        return current if current in chars else ''

    def match_string_pattern(self, first, rest=None, least=1, offset=0):
        """Match each char sequentially from current SourceString position
        until the pattern doesnt match and return all maches.

        Integer argument least defines and minimum amount of chars that can
        be matched.

        If rest is defined then first is used only to match the first arg
        and the rest of the chars are matched against rest.
        """
        if not self.has_space(offset=offset):
            return ''
        firstchar = self.string[self.pos + offset]
        if not firstchar in first:
            return ''

        output = [firstchar]
        pattern = first if rest is None else rest

        for char in self.string[self.pos + offset + 1:]:
            if char in pattern:
                output.append(char)
            else:
                break

        if len(output) < least:
            return ''

        return ''.join(output)

    def match_function_pattern(self, first, rest=None, least=1, offset=0):
        """Match each char sequentially from current SourceString position
        until the pattern doesnt match and return all maches.

        Integer argument least defines and minimum amount of chars that can
        be matched.

        This version takes functions instead of string patterns.
        Each function must take one argument, a string, and return a
        value that can be evauluated as True or False.

        If rest is defined then first is used only to match the first arg
        and the rest of the chars are matched against rest.
        """
        if not self.has_space(offset=offset):
            return ''
        firstchar = self.string[self.pos + offset]
        if not first(firstchar):
            return ''

        output = [firstchar]
        pattern = first if rest is None else rest

        for char in self.string[self.pos + offset + 1:]:
            if pattern(char):
                output.append(char)
            else:
                break

        if len(output) < least:
            return ''

        return ''.join(output)

    def count_indents(self, spacecount, tabs=0, offset=0):
        """Counts the number of indents that can be tabs or spacecount
        number of spaces in a row from the current line.
        """
        if not self.has_space(offset=offset):
            return 0
        spaces = 0
        indents = 0
        for char in self.string[self.pos + offset - self.col:]:
            if char == ' ':
                spaces += 1
            elif tabs and char == '\t':
                indents += 1
                spaces = 0
            else:
                break
            if spaces == spacecount:
                indents += 1
                spaces = 0
        return indents

    def count_indents_length(self, spacecount, tabs=0, offset=0):
        """Counts the number of indents that can be tabs or spacecount
        number of spaces in a row from the current line.

        Also returns the character length of the indents.
        """
        if not self.has_space(offset=offset):
            return 0
        spaces = 0
        indents = 0
        charlen = 0
        for char in self.string[self.pos + offset - self.col:]:
            if char == ' ':
                spaces += 1
            elif tabs and char == '\t':
                indents += 1
                spaces = 0
            else:
                break
            charlen += 1
            if spaces == spacecount:
                indents += 1
                spaces = 0
        return (indents, charlen)

    def count_indents_last_line(self, spacecount, tabs=0, back=5):
        """Finds the last meaningful line and returns its indent level.
        Back specifies the amount of lines to look back for a none whitespace
        line.
        """
        if not self.has_space():
            return 0
        lines = self.get_surrounding_lines(back, 0)

        for line in reversed(lines):
            if not line.string.isspace():
                return line.count_indents(spacecount, tabs)
        return 0

    def count_indents_length_last_line(self, spacecount, tabs=0, back=5):
        """Finds the last meaningful line and returns its indent level and
        character length.
        Back specifies the amount of lines to look back for a none whitespace
        line.
        """
        if not self.has_space():
            return 0
        lines = self.get_surrounding_lines(back, 0)

        for line in reversed(lines):
            if not line.string.isspace():
                return line.count_indents_length(spacecount, tabs)
        return (0, 0)

    def skip_whitespace(self, newlines=0):
        """Moves the position forwards to the next non newline space character.
        If newlines >= 1 include newlines as spaces.
        """
        if newlines:
            while not self.eos:
                if self.get_char().isspace():
                    self.eat_length(1)
                else:
                    break
        else:
            char = ''
            while not self.eos:
                char = self.get_char()
                if char.isspace() and char != '\n':
                    self.eat_length(1)
                else:
                    break

    def __repr__(self):
        """Returns the entire base string. Called from the repr() builtin."""
        return self.string

    def __getitem__(self, index):
        """Returns the character at the given index.
        Called by SourceString[index] where index is an integer.
        """
        return self.string[index]

    def __delitem__(self, index):
        del self.string[index]

    def __setitem__(self, index, value):
        self.string[index] = value

    def __len__(self):
        """Returns the length of base string. Called by len(SourceString)."""
        return len(self.string)

    def __contains__(self, string):
        """Returns a boolean if the given string is within the base string.
        Called by 'word' in SourceString.
        """
        return string in self.string

    def __iter__(self):
        """Yields the current char and moves the position onwards until eos."""
        string = self.string
        while not self.eos:
            yield string[self.pos]
            self.eat_length(1)


class SourceLine(SourceString):
    """Contains an entire line of a source with handy line specific methods."""

    def __init__(self, string, lineno):  # pylint: disable=W0231
        self.string = ''
        self.length = 0
        self.set_string(string)
        self.lineno = lineno  # pylint: enable=W0231

    def strip_trailing_ws(self):
        """Remove trailing whitespace from internal string."""
        self.string = self.string.rstrip()

    def get_first_char(self):
        """Return the first non-whitespace character of the line."""
        for char in self.string:
            if not char.isspace():
                return char

    def get_last_char(self):
        """Return the last non-whitespace character of the line."""
        for char in reversed(self.string):
            if not char.isspace():
                return char

    def pretty_print(self, carrot=False):
        """Return a string of this line including linenumber.
        If carrot is True then a line is added under the string with a carrot
        under the current character position.
        """
        lineno = self.lineno
        padding = 0
        if lineno < 1000:
            padding = 1
        if lineno < 100:
            padding = 2
        if lineno < 10:
            padding = 3

        string = str(lineno) + (' ' * padding) + '|' + self.string
        if carrot:
            string += '\n' + (' ' * (self.col + 5))
        return string

    def __str__(self):
        return self.pretty_print()
