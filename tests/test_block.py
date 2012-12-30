from unittest import TestCase

from block import Block


class TestBlock(TestCase):
    def test_constructor(self):
        s = '#foo div'
        b = Block(s)
        self.assertEqual(b.selectors, [s])
        self.assertEqual(b.properties, set())


class TestBlockAddProperty(TestCase):
    def setUp(self):
        self.b = Block('foo')

    def test_single_value(self):
        self.b.add_property('foo', 'bar')
        self.assertEqual(self.b.properties, set([('foo', 'bar')]))

    def test_double_value(self):
        self.b.add_property('foo', 'bar')
        self.b.add_property('foo', 'bar')
        self.assertEqual(self.b.properties, set([('foo', 'bar')]))

    def test_multiple_values(self):
        self.b.add_property('foo', 'bar')
        self.b.add_property('foo', 'baz')
        self.assertEqual(self.b.properties, set([('foo', 'bar'),
                                                 ('foo', 'baz')]))


class TestBlockGenerateCss(TestCase):
    def setUp(self):
        self.div = Block('div')
        self.div.add_property('color', '#000')
        self.div.add_property('font-weight', 'bold')

    def test_nocompress_empty(self):
        div = Block('div')
        self.assertEqual(div.generate_css(), 'div {\n}')

    def test_nocompress_single_property(self):
        div = Block('div')
        div.add_property('color', '#000')
        self.assertEqualCss(div.generate_css(), '''
div {
    color: #000;
}''')

    def test_nocompress_multiple_properties(self):
        self.assertEqualCss(self.div.generate_css(), '''
div {
    color: #000;
    font-weight: bold;
}''')

    def test_nocompress_multiple_selectors(self):
        div = Block('div', 'p')
        div.add_property('color', '#000')
        self.assertEqualCss(div.generate_css(), '''
div,
p {
    color: #000;
}''')

    def test_nocompress_multiple_selectors_sorted(self):
        self.assertMultiLineEqual(Block('div', 'p').generate_css(),
                                  Block('p', 'div').generate_css())

    def test_compress_whitespace(self):
        self.assertEqual(self.div.generate_css(compress_whitespace=True),
                         'div{color:#000;font-weight:bold}')

    def test___str__(self):
        self.assertEqual(str(self.div), self.div.generate_css())

    def assertEqualCss(self, a, b):
        self.assertMultiLineEqual(a, b.strip().replace('    ', '\t'))
