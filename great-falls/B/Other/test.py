import unittest
from main import parse_args


class MyTestCase(unittest.TestCase):
    def test_parse_args_returns_lines(self):
        self.assertEqual(parse_args(['Other/main.py', '-10']), 10)

    def test_no_dash(self):
        self.assertRaises(ValueError, parse_args, ['Other/main.py', '10'])

    def test_not_numeric(self):
        self.assertRaises(ValueError, parse_args, ['Other/main.py', '-a'])

    def test_not_natural(self):
        self.assertRaises(ValueError, parse_args, ['Other/main.py', '--10'])

    def test_only_digit(self):
        self.assertRaises(ValueError, parse_args, ['Other/main.py', '-+10'])

    def test_no_lines(self):
        self.assertRaises(IndexError, parse_args, ['Other/main.py'])


if __name__ == '__main__':
    unittest.main()
