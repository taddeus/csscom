from unittest import TestCase

from generate import generate_block, generate_group


class TestGenerateBlock(TestCase):
    def setUp(self):
        self.selector = 'div'
        self.properties = [('color', '#000'), ('font-weight', 'bold')]

    def test_nocompress_empty(self):
        self.assertGenerates(['div'], [], 'div {\n}')

    def test_nocompress_single_property(self):
        selectors = ['div']
        properties = [('color', '#000')]
        self.assertGenerates(selectors, properties, '''
div {
    color: #000;
}''')

    def test_nocompress_multiple_properties(self):
        selectors = ['div']
        properties = [('color', '#000'), ('font-weight', 'bold')]
        self.assertGenerates(selectors, properties, '''
div {
    color: #000;
    font-weight: bold;
}''')

    def test_nocompress_multiple_selectors(self):
        selectors = ['div', 'p']
        properties = [('color', '#000')]
        self.assertGenerates(selectors, properties, '''
div,
p {
    color: #000;
}''')

    def test_nocompress_multiple_selectors_sorted(self):
        self.assertMultiLineEqual(generate_block(['div', 'p'], []),
                                  generate_block(['p', 'div'], []))

    def test_compress_whitespace(self):
        selectors = ['div']
        properties = [('color', '#000'), ('font-weight', 'bold')]
        self.assertGenerates(selectors, properties,
                             'div{color:#000;font-weight:bold}',
                             compress_whitespace=True)

    def assertGenerates(self, selectors, props, css, **kwargs):
        self.assertMultiLineEqual(generate_block(selectors, props, **kwargs),
                                  css.strip().replace('    ', '\t'))


class TestGenerateGroup(TestCase):
    pass
