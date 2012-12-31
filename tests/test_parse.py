from unittest import TestCase

from parse import split_selectors, parse_groups


class TestHelpers(TestCase):
    def test_split_selectors(self):
        self.assertEqual(split_selectors(''), [])
        self.assertEqual(split_selectors('a, b'), ['a', 'b'])
        self.assertEqual(split_selectors('a ,b'), ['a', 'b'])
        self.assertEqual(split_selectors('\na ,b '), ['a', 'b'])
        self.assertEqual(split_selectors('a, b\nc'), ['a', 'b c'])
        self.assertEqual(split_selectors('a,\nb c ,d\n'), ['a', 'b c', 'd'])


class TestParseGroups(TestCase):
    def test_empty_stylesheet(self):
        self.assertParse('', [])
        self.assertParse(' \n ', [])

    def test_empty_block(self):
        self.assertParse('div {}', [(None, [(['div'], [])])])

    def test_single_property(self):
        self.assertParse('div {color:black;}',
                         [(None, [(['div'], [('color', 'black')])])])
        self.assertParse('div {color:black}',
                         [(None, [(['div'], [('color', 'black')])])])

        self.assertParse('''
        div {
            color: black;
        }
        ''', [(None, [(['div'], [('color', 'black')])])])

        self.assertParse('''
        div {
            color: black
        }
        ''', [(None, [(['div'], [('color', 'black')])])])

    def test_multiple_properties(self):
        self.assertParse('''
        div {
            color: black;
            border: none;
        }
        ''', [(None, [(['div'], [('color', 'black'), ('border', 'none')])])])

        self.assertParse('''
        div {
            color: black;
            border: none
        }
        ''', [(None, [(['div'], [('color', 'black'), ('border', 'none')])])])

    def test_multiple_selectors(self):
        self.assertParse('div,p {color: black}',
                         [(None, [(['div', 'p'], [('color', 'black')])])])
        self.assertParse('div, p {color: black}',
                         [(None, [(['div', 'p'], [('color', 'black')])])])
        self.assertParse('p,\n\tdiv {color: black}',
                         [(None, [(['p', 'div'], [('color', 'black')])])])

    def test_single_group(self):
        self.assertParse('''
        @media (min-width: 970px) {
            div {color: black}
        }
        ''', [(['@media (min-width: 970px)'],
               [(['div'], [('color', 'black')])])])

    def test_single_group_multiple_blocks(self):
        self.assertParse('''
        @media (min-width: 970px) {
            div {color: black}
            p {margin: 0}
        }
        ''', [(['@media (min-width: 970px)'],
               [(['div'], [('color', 'black')]), (['p'], [('margin', '0')])])])

    def test_multiple_groups(self):
        self.assertParse('''
        @media (min-width: 970px) {
            div {color: black}
        }
        @media (max-width: 969px) {
            div {color: red}
        }
        ''', [
            (['@media (min-width: 970px)'], [(['div'], [('color', 'black')])]),
            (['@media (max-width: 969px)'], [(['div'], [('color', 'red')])])
        ])

    def test_group_with_root(self):
        self.assertParse('''
        div {
            color: black
        }
        @media (max-width: 969px) {
            div {color: red}
        }
        ''', [
            (None, [(['div'], [('color', 'black')])]),
            (['@media (max-width: 969px)'], [(['div'], [('color', 'red')])])
        ])

        self.assertParse('''
        @media (max-width: 969px) {
            div {color: red}
        }
        div {
            color: black
        }
        ''', [
            (['@media (max-width: 969px)'], [(['div'], [('color', 'red')])]),
            (None, [(['div'], [('color', 'black')])])
        ])

    def test_group_with_multiple_roots(self):
        self.assertParse('''
        div {
            color: black
        }
        @media (max-width: 969px) {
            div {color: red}
        }
        p {
            margin: 0
        }
        ''', [
            (None, [(['div'], [('color', 'black')])]),
            (['@media (max-width: 969px)'], [(['div'], [('color', 'red')])]),
            (None, [(['p'], [('margin', '0')])])
        ])

    def test_multiple_groups_multiple_roots(self):
        self.assertParse('''
        @media (min-width: 970px) {
            div {color: black}
        }
        div {
            color: black
        }
        @media (max-width: 969px) {
            div {color: red}
        }
        p {
            margin: 0
        }
        ''', [
            (['@media (min-width: 970px)'], [(['div'], [('color', 'black')])]),
            (None, [(['div'], [('color', 'black')])]),
            (['@media (max-width: 969px)'], [(['div'], [('color', 'red')])]),
            (None, [(['p'], [('margin', '0')])])
        ])

        self.assertParse('''
        p {
            margin: 0
        }
        @media (min-width: 970px) {
            div {color: black}
        }
        div {
            color: black
        }
        @media (max-width: 969px) {
            div {color: red}
        }
        ''', [
            (None, [(['p'], [('margin', '0')])]),
            (['@media (min-width: 970px)'], [(['div'], [('color', 'black')])]),
            (None, [(['div'], [('color', 'black')])]),
            (['@media (max-width: 969px)'], [(['div'], [('color', 'red')])]),
        ])

    def test_comment(self):
        self.assertParse('''
        /* this is a comment */
        div {color: black}
        ''', [(None, [(['div'], [('color', 'black')])])])

        self.assertParse('''
        /*
         * this is a multiline comment
         */

        div {color: black}
        ''', [(None, [(['div'], [('color', 'black')])])])

        self.assertParse('''
        div {color: /*inline comment*/ black}
        ''', [(None, [(['div'], [('color', 'black')])])])

    def test_error_brackets(self):
        self.assertRaisesRegexp(Exception, 'unexpected \'{\' on line 1',
                parse_groups, '{')
        self.assertRaisesRegexp(Exception, 'unexpected \'{\' on line 2',
                parse_groups, 'div {\n{}')

        self.assertRaisesRegexp(Exception, 'unexpected \'}\' on line 1',
                parse_groups, '}')
        self.assertRaisesRegexp(Exception, 'unexpected \'}\' on line 2',
                parse_groups, 'div\n}')

    def test_error_EOF(self):
        self.assertRaisesRegexp(Exception, 'unexpected <EOF> on line 3',
                parse_groups, '\ndiv\n')
        self.assertRaisesRegexp(Exception, 'unexpected <EOF> on line 2',
                parse_groups, '\ndiv {')

    def test_error_property_name(self):
        self.assertRaisesRegexp(Exception, 'unexpected \':\' on line 2',
                parse_groups, 'div{margin\nleft: 0}')

    def test_error_property_value(self):
        self.assertRaisesRegexp(Exception, 'unexpected \';\' on line 1',
                parse_groups, 'div{margin:;}')
        self.assertRaisesRegexp(Exception, 'unexpected \';\' on line 1',
                parse_groups, 'div{foo;}')
        self.assertParse('div {;}', [(None, [(['div'], [])])])

    def assertParse(self, css, result):
        self.assertEqual(parse_groups(css), result)
