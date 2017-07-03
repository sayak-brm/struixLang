__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'

cimport cython as cy


cdef class SourceString(object):
    cdef public str string
    cdef public long length, pos, row
    cdef public long col, eos

    cpdef load_file(self, str filename)

    cpdef set_string(self, str string)

    cpdef add_string(self, str string)

    cpdef reset_position(self)

    cpdef int has_space(self, long length = *, long offset = *)

    @cy.locals(distance = cy.long)
    cpdef long eol_distance_next(self, long offset = *)
    
    @cy.locals(distance = cy.long)
    cpdef long eol_distance_last(self, long offset = *)

    @cy.locals(pos = cy.long, col = cy.long, row = cy.long, char = str)
    cpdef eat_length(self, long length)

    @cy.locals(pos = cy.long, col = cy.long, row = cy.long, char = str)
    cpdef eat_string(self, str string)

    cpdef eat_line(self)

    cpdef str get_char(self, long offset = *)

    cpdef str get_length(self, long length, long trim = *, long offset = *)

    @cy.locals(string = str, pos = cy.long)
    cpdef str get_string(self, long offset = *)

    cpdef str rest_of_string(self, long offset = *)

    @cy.locals(line = cy.long, output = list, char = str)
    cpdef SourceLine get_line(self, long lineno)

    @cy.locals(pos = cy.long, string = str, end = cy.long, output = list)
    cpdef SourceLine get_current_line(self)

    @cy.locals(linestring = list, linestrings = list, output = list, char = str,
        line = cy.long)
    cpdef list get_lines(self, first, last)

    @cy.locals(string = str, pos = cy.long, end = cy.long, row = cy.long,
        linesback = cy.long, output = list, linestring = list, lines = cy.long)
    cpdef list get_surrounding_lines(self, long past = *, long future = *)

    @cy.locals(output = list, line = list, lineno = cy.long, char = str)
    cpdef list get_all_lines(self)

    cpdef int match_string(self, str string, int word = *, long offset = *)

    @cy.locals(length = cy.long, currentlength = cy.long, current = str,
    string = str)
    cpdef str match_any_string(self, list strings, int word = *, long offset = *)

    @cy.locals(current = str)
    cpdef str match_any_char(self, str chars, long offset = *)

    @cy.locals(pattern = str, output = list, firstchar = str, char = str)
    cpdef str match_string_pattern(self, str first, str rest = ?, long least = *, long offset = *)

    @cy.locals(output = list, firstchar = str, char = str)
    cpdef str match_function_pattern(self, first, rest = ?, int least = *, long offset = *)

    @cy.locals(indents = cy.long, spaces = cy.long, char = str)
    cpdef long count_indents(self, long spacecount, int tabs = *, long offset = *)

    @cy.locals(indents = cy.long, spaces = cy.long, charlen = cy.long, char = str)
    cpdef tuple count_indents_length(self, long spacecount, int tabs = *, long offset = *)

    @cy.locals(lines = list, line = SourceLine)
    cpdef count_indents_last_line(self, long spacecount, int tabs = *, long back = *)

    @cy.locals(lines = list, line = SourceLine)
    cpdef count_indents_length_last_line(self, long spacecount, int tabs = *,  long back = *)

    @cy.locals(char = str)
    cpdef skip_whitespace(self, int newlines = *)


cdef class SourceLine(SourceString):
    cdef public long lineno

    cpdef strip_trailing_ws(self)

    @cy.locals(char = str)
    cpdef str get_first_char(self)

    @cy.locals(char = str)
    cpdef str get_last_char(self)
