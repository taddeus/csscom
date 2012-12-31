def split_selectors(raw_selector):
    """
    Split a selector with commas and arbitrary whitespaces into a list of
    selector swith single-space whitespaces.
    """
    return filter(None, (' '.join(s.split()) for s in raw_selector.split(',')))


def parse_groups(css):
    """
    Parse CSS code one character at a time. This is more efficient than
    simply splitting on brackets, especially for large style sheets. All
    comments are ignored.
    """
    stack = char = ''
    prev_char = None
    lineno = 1
    properties = []
    current_group = (None, [])
    groups = []
    selectors = None
    comment = False
    nesting_level = 0
    property_name = None

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
                nesting_level += 1

                # Block start
                if selectors is not None:
                    # Block is nested, push current root group and continue
                    # with this group
                    if len(current_group[1]):
                        groups.append(current_group)

                    current_group = (selectors, [])

                selectors = split_selectors(stack)
                stack = ''
                assert len(selectors)
            elif char == '}':
                assert nesting_level > 0
                nesting_level -= 1

                if selectors is None:
                    # Closing group
                    groups.append(current_group)
                    current_group = (None, [])
                else:
                    # Closing block
                    # Last property may not have been closed with a semicolon
                    property_value = stack.strip()

                    if len(property_value):
                        assert property_name is not None
                        properties.append((property_name, property_value))
                        property_name = None
                        stack = ''

                    current_group[1].append((selectors, properties))
                    selectors = None
                    properties = []
            elif char == ':' and nesting_level > 0:
                assert selectors is not None
                # Property name
                property_name = stack.strip()
                assert '\n' not in property_name
                stack = ''
            elif char == ';':
                # Property value
                property_value = stack.strip()

                if len(property_value):
                    assert property_name is not None
                    properties.append((property_name, property_value))
                    property_name = None
                    stack = ''
                else:
                    assert property_name is None
            elif char == '*' and prev_char == '/':
                # Comment start
                comment = True
                stack = stack[:-1]
            else:
                stack += char

            prev_char = char

        if len(current_group[1]):
            groups.append(current_group)

        if stack.split() or nesting_level > 0:
            char = '<EOF>'
            raise AssertionError()
    except AssertionError:
        if len(char) < 2:
            char = "'" + char + "'"

        raise Exception('unexpected %s on line %d' % (char, lineno))

    return groups
