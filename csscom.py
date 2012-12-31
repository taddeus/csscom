#!/usr/bin/env python
from argparse import ArgumentParser

from parse import parse_groups
from generate import generate_group


def compress_css(css, combine_blocks=True, compress_whitespace=True,
                 compress_color=True, compress_font=True,
                 compress_dimension=True, sort_properties=True):
    groups = parse_groups(css)
    options = dict(combine_blocks=combine_blocks,
                   compress_whitespace=compress_whitespace,
                   compress_color=compress_color,
                   compress_font=compress_font,
                   compress_dimension=compress_dimension,
                   sort_properties=sort_properties)
    compressed_groups = [generate_group(selectors, blocks, **options)
                         for selectors, blocks in groups]
    newlines = '' if compress_whitespace else '\n\n'
    return newlines.join(compressed_groups)


def parse_options():
    parser = ArgumentParser(description='Just another CSS compressor.')
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='list of CSS files to compress')
    parser.add_argument('-cw', '--compress-whitespace', action='store_true',
                        help='omit unnecessary whitespaces and semicolons')
    parser.add_argument('-cc', '--compress-color', action='store_true',
                        help='replace color codes/names with shorter synonyms')
    parser.add_argument('-cf', '--compress-font', action='store_true',
                        help='replace separate font statements with shortcut '
                             'font statement where possible')
    parser.add_argument('-cd', '--compress-dimension', action='store_true',
                        help='replace separate margin/padding statements with '
                             'shortcut statements where possible')
    parser.add_argument('-cb', '--combine-blocks', action='store_true',
                        help='combine or split blocks into blocks with '
                             'comma-separated selectors if it results in less '
                             'css code')
    parser.add_argument('-nc', '--no-compression', action='store_true',
                        help='don\'t apply any compression, just generate CSS')
    parser.add_argument('-ns', '--no-sort', action='store_false',
                        dest='sort_properties', help='sort property names')
    parser.add_argument('-o', '--output', help='filename for compressed '
                                               'output (default is stdout)')
    args = parser.parse_args()

    # Enable all compression options if none are explicitely enabled
    if not any([args.compress_whitespace, args.compress_color,
                args.compress_font, args.compress_dimension,
                args.combine_blocks]) and not args.no_compression:
        args.compress_whitespace = args.compress_color = args.compress_font = \
                args.compress_dimension = args.combine_blocks = True

    return args


def _content(filename):
    handle = open(filename, 'r')
    content = '\n' + handle.read()
    handle.close()
    return content


if __name__ == '__main__':  # pragma: nocover
    args = parse_options()
    options = dict(args._get_kwargs())
    files = options.pop('files')
    output_file = options.pop('output')
    del options['no_compression']

    try:
        css = '\n'.join(_content(filename) for filename in files)
        compressed = compress_css(css, **options)

        if output_file:
            open(output_file, 'w').write(compressed)
        else:
            print compressed,
    except IOError as e:
        print e
