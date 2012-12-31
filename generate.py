from operator import itemgetter

import compress


def _indent(text, tab='\t'):
    indented = ''

    for i, line in enumerate(text.split('\n')):
        if i:
            indented += '\n'

        if len(line):
            indented += tab

        indented += line

    return indented


def _indented_block(selectors, inner, compress_whitespace=False, tab='\t'):
    if compress_whitespace:
        comma = ','
        lbracket = '{'
        rbracket = '}'
    else:
        # TODO: use this?: comma = ',\n'
        comma = ', '
        lbracket = ' {'
        rbracket = '\n}'
        inner = _indent(inner, tab=tab)

    selector = comma.join(sorted(set(selectors)))
    return selector + lbracket + inner + rbracket


def generate_block(selectors, properties, compress_whitespace=False,
                   sort_properties=False, tab='\t'):
    """
    Generate CSS code for a single block.
    """
    if sort_properties:
        properties.sort(key=itemgetter(0))

    if compress_whitespace:
        newline = ''
        colon = ':'
    else:
        newline = '\n'
        colon = ': '

    properties = [newline + name + colon + value
                  for name, value in properties]
    inner = ';'.join(properties)

    if not compress_whitespace:
        inner += ';'

    return _indented_block(selectors, inner,
                           compress_whitespace=compress_whitespace, tab=tab)


def generate_group(selectors, blocks, compress_blocks=True,
                   compress_whitespace=True, compress_color=True,
                   compress_font=True, compress_dimension=True,
                   sort_properties=True, tab='\t'):
    compressed_blocks = []

    if compress_blocks:
        blocks = compress.compress_blocks(blocks)

    for block_selectors, properties in blocks:
        if compress_color:
            properties = compress.compress_color(properties)

        if compress_font:
            properties = compress.compress_font(properties)

        if compress_dimension:
            properties = compress.compress_dimension(properties)

        compressed_blocks.append(generate_block(block_selectors, properties,
            compress_whitespace=compress_whitespace,
            sort_properties=sort_properties, tab=tab))

    newline = '' if compress_whitespace else '\n'
    inner = newline.join(compressed_blocks)

    if selectors is None:
        # Root-level group
        return inner

    return _indented_block(selectors, newline + inner,
                           compress_whitespace=compress_whitespace, tab=tab)
