from unittest import TestCase

from parse import split_selectors, parse_groups


class TestParse(TestCase):
    def test_split_selectors(self):
        self.assertEqual(split_selectors('a, b'), ['a', 'b'])
        self.assertEqual(split_selectors('a ,b'), ['a', 'b'])
        self.assertEqual(split_selectors('\na ,b '), ['a', 'b'])
        self.assertEqual(split_selectors('a, b\nc'), ['a', 'b c'])
        self.assertEqual(split_selectors('a,\nb c ,d\n'), ['a', 'b c', 'd'])
