import unittest

tests = unittest.defaultTestLoader.discover('tests', 'test_*.py')
run_options = dict(failfast=True)

if __name__ == '__main__':
    unittest.TextTestRunner(**run_options).run(tests)
    print
