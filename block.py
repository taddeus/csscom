import properties as props


class Block(object):
    """
    A Block is a stylesheet block of the following form:

    <selector>,
    ... {
        <property>: <value>;
        ...
    }
    """
    def __init__(self, *args):
        self.selectors = sorted(set(args))
        self.properties = set()

    def add_property(self, name, value):
        self.properties.add((name, value))

    def generate_css(self, compress_whitespace=False, compress_color=False,
                     compress_font=False, compress_dimension=False):
        if compress_whitespace:
            comma = ','
            colon = ':'
            newline = ''
            lbracket = '{'
            rbracket = '}'
        else:
            comma = ',\n'
            colon = ': '
            newline = '\n\t'
            lbracket = ' {'
            rbracket = '\n}'

        properties = self.properties

        if compress_color:
            properties = props.compress_color(properties)

        if compress_font:
            properties = props.compress_font(properties)

        if compress_dimension:
            properties = props.compress_dimension(properties)

        selector = comma.join(self.selectors)
        properties = [newline + name + colon + value
                      for name, value in self.properties]
        inner = ';'.join(properties)

        if len(properties) and not compress_whitespace:
            inner += ';'

        return selector + lbracket + inner + rbracket

    def __repr__(self):  # pragma: nocover
        return '<Block "%s" properties=%d>' \
               % (', '.join(self.selectors), len(self.properties))

    def __str__(self):
        return self.generate_css()
