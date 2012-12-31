def split_selectors(raw_selector):
    """
    Split a selector with commas and arbitrary whitespaces into a list of
    selector swith single-space whitespaces.
    """
    return [' '.join(s.split()) for s in raw_selector.split(',')]


def parse_groups(css):
    """
    Parse CSS code one character at a time. This is more efficient than
    simply splitting on brackets, especially for large style sheets. All
    comments are ignored (both inline and multiline).
    """
    stack = char = ''
    prev_char = None
    lineno = 1
    properties = []
    current_group = root_group = []
    groups = [(None, root_group)]
    selectors = None
    comment = False

    def parse_property():
        assert selectors is not None

        if stack.strip():
            parts = stack.split(':', 1)
            assert len(parts) == 2
            name, value = map(str.strip, parts)
            assert '\n' not in name
            properties.append((name, value))

    try:
        for c in css:
            char = c

            if char == '\n':
                lineno += 1

            if comment:
                # Comment end?
                if char == '/' and prev_char == '*':
                    comment = False
            elif char == '{':
                # Block start
                if selectors is not None:
                    # Block is nested, save group selector
                    current_group = []
                    groups.append((selectors, current_group))

                selectors = split_selectors(stack)
                #print stack.strip(), '->', selectors
                stack = ''
                assert len(selectors)
            elif char == '}':
                # Last property may not have been closed with a semicolon
                parse_property()

                if selectors is None:
                    # Closing group
                    current_group = root_group
                else:
                    # Closing block
                    current_group.append((selectors, properties))
                    selectors = None
                    properties = []
            elif char == ';':
                # Property definition
                parse_property()
                stack = ''
            elif char == '*' and prev_char == '/':
                # Comment start
                comment = True
                stack = stack[:-1]
            else:
                stack += char

            prev_char = char
    except AssertionError:
        raise Exception('unexpected \'%c\' on line %d' % (char, lineno))

    return groups
