"""Custom exception for classes inheriting SourceString or Matcher."""
__author__ = 'Taylor "Nekroze" Lawson'
__email__ = 'nekroze@eturnilnetwork.com'


class PartpyError(Exception):
    """Takes a SourceString or Matcher derived object and an optional message.

    When converted to a string will display the previous and current line
    with line numbers and a '^' under the current position of the object with
    the optional message on the following line.
    """
    def __init__(self, obj, msg=None):  # pylint: disable=W0231
        self.partpymsg = msg
        self.partpyobj = obj  # pylint: enable=W0231

    def pretty_print(self, carrot=True):
        """Print the previous and current line with line numbers and
        a carret under the current character position.

        Will also print a message if one is given to this exception.
        """
        output = ['\n']
        output.extend([line.pretty_print() for line in
                       self.partpyobj.get_surrounding_lines(1, 0)])

        if carrot:
            output.append('\n' +
                          (' ' * (self.partpyobj.col + 5)) + '^' + '\n')
        if self.partpymsg:
            output.append(self.partpymsg)

        return ''.join(output)

    def __repr__(self):
        return self.pretty_print()

    def __str__(self):
        return self.pretty_print()
