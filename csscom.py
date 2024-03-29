#!/usr/bin/env python
from argparse import ArgumentParser
import logging
import sys

from parse import parse_groups
from generate import generate_group


def compress_css(css, combine_blocks=True, compress_whitespace=True,
                 compress_color=True, compress_font=True,
                 compress_dimension=True, sort_properties=True, tab='\t'):
    groups = parse_groups(css)
    options = dict(combine_blocks=combine_blocks,
                   compress_whitespace=compress_whitespace,
                   compress_color=compress_color,
                   compress_font=compress_font,
                   compress_dimension=compress_dimension,
                   sort_properties=sort_properties,
                   tab=tab)
    compressed_groups = [generate_group(selectors, blocks, **options)
                         for selectors, blocks in groups]
    newlines = '' if compress_whitespace else '\n\n'
    return newlines.join(compressed_groups)


def parse_options():
    parser = ArgumentParser(description='Just another CSS compressor. '
            'If none of the compression options below (those starting with '
            '"-c") are specified, all are enabled by default. If any are '
            'specified, the others are not enabled.')
    parser.add_argument('files', metavar='FILE', nargs='*',
                        help='CSS files to compress (CSS is read from stdin '
                             'if no files are specified)')
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
    parser.add_argument('-s', '--spaces', type=int, metavar='NUMBER=4',
                        nargs='?', const=4,
                        help='number of spaces to use for indenting (indent '
                             'defaults to a single tab [\\t])')
    parser.add_argument('-o', '--output', metavar='FILE',
                        help='filename for compressed output (default is '
                             'stdout)')
    parser.add_argument('-ow', '--overwrite', action='store_true',
                        help='use the first CSS file as output file')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show which compressions are performed')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='show debug statements')
    parser.add_argument('--logfile', metavar='FILE',
                        help='file to write verbose/debug statements to '
                             '(defaults to stderr)')
    args = parser.parse_args()

    # Enable all compression options if none are explicitely enabled
    if not any([args.compress_whitespace, args.compress_color,
                args.compress_font, args.compress_dimension,
                args.combine_blocks]) and not args.no_compression:
        args.compress_whitespace = args.compress_color = args.compress_font \
                = args.compress_dimension = args.combine_blocks = True

    return args


def _content(filename):
    handle = open(filename, 'r')
    content = handle.read()
    handle.close()
    return content


if __name__ == '__main__':
    args = parse_options()
    options = dict(args._get_kwargs())

    files = options.pop('files')

    del options['no_compression']

    spaces = options.pop('spaces')
    options['tab'] = '\t' if spaces is None else spaces * ' '

    outfile = options.pop('output')

    if options.pop('overwrite'):
        if not files:
            print 'error: cannot use --overwrite option wihthout filenames'
            sys.exit(1)

        outfile = files[0]

    log_level = logging.WARNING

    if options.pop('verbose'):
        log_level = logging.INFO

    if options.pop('debug'):
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level, filename=options.pop('logfile'),
                        #format='%(levelname)s: %(message)s')
            format='%(filename)s, line %(lineno)s: %(levelname)s: %(message)s')

    try:
        if files:
            css = '\n'.join(_content(filename) for filename in files)
        else:
            css = sys.stdin.read()

        compressed = compress_css(css, **options)

        if outfile:
            open(outfile, 'w').write(compressed)
        else:
            print compressed,
    except IOError as e:
        print e
