#!/usr/bin/env python
from block import Block


def split_selectors(raw_selector):
    """
    Split a selector with commas and arbitrary whitespaces into a list of
    selector swith single-space whitespaces.
    """
    return [' '.join(s.split()) for s in raw_selector.split(',')]


class StyleSheet(object):
    def __init__(self, css=None):
        # List of encountered blocks
        self.blocks = []

        # Map of property stringification to list of containing blocks
        self.property_locations = {}

        if css:
            self.parse_css(css)

    def parse_css(self, css):
        """
        Parse CSS code one character at a time. This is more efficient than
        simply splitting on brackets, especially for large style sheets. All
        comments are ignored (both inline and multiline).
        """
        stack = char = ''
        prev = block = None
        lineno = 1
        multiline_comment = inline_comment = False

        try:
            for c in css:
                char = c

                if multiline_comment:
                    # Multiline comment end?
                    if c == '/' and prev == '*':
                        multiline_comment = False
                elif inline_comment:
                    # Inline comment end?
                    if c == '\n':
                        inline_comment = False
                elif c == '{':
                    # Block start
                    selectors = split_selectors(stack)
                    stack = ''
                    assert len(selectors)
                    block = Block(*selectors)
                elif c == '}':
                    # Block end
                    assert block is not None
                    block = None
                elif c == ';':
                    # Property definition
                    assert block is not None
                    name, value = map(str.strip, stack.split(':', 1))
                    assert '\n' not in name
                    block.add_property(name, value)
                elif c == '*' and prev == '/':
                    # Multiline comment start
                    multiline_comment = True
                elif c == '/' and prev == '/':
                    # Inline comment start
                    inline_comment = True
                else:
                    if c == '\n':
                        lineno += 1

                    stack += c
                    prev = c
        except AssertionError:
            raise Exception('unexpected \'%c\' on line %d' % (char, lineno))

    def generate_css(self, compress_whitespace=False, compress_color=False,
                     compress_font=False, compress_dimension=False,
                     compress_blocks=False):
        """
        Generate CSS code for the entire stylesheet.

        Options:
        compress_whitespace | Omit unnecessary whitespaces and semicolons.
        compress_color      | Replace color codes/names with shorter synonyms.
        compress_font       | Replace separate font statements with shortcut
                            | font statement where possible.
        compress_dimension  | Replace separate margin/padding statements with
                            | shortcut statements where possible.
        compress_blocks     | Combine or split blocks into blocks with
                            | comma-separated selectors if it results in less
                            | CSS code.
        """
        blocks = self.blocks

        if compress_blocks:
            blocks = self._compress_blocks()

        options = dict(compress_whitespace=compress_whitespace,
                       compress_color=compress_color,
                       compress_font=compress_font,
                       compress_dimension=compress_dimension)
        newline = '' if compress_whitespace else '\n'

        return newline.join(block.generate_css(**options)
                            for block in self.blocks)

    def _compress_blocks(self):
        pass
        #for block in self.blocks

    def compress(self, **kwargs):
        """
        Shortcut for `generate_css`, with all compression options enabled by
        default. Keyword argument names are preceded by 'compress_' before
        being passed to `generate_css`.
        """
        options = dict(whitespace=True, color=True, font=True, dimension=True,
                       blocks=True)
        options.update(kwargs)
        options = dict([('compress_' + k, v) for k, v in options.items()])

        return self.generate_css(**options)

    def __str__(self):
        return self.generate_css()


if __name__ == '__main__':  # pragma: nocover
    # TODO: Command-line options parser
    pass
