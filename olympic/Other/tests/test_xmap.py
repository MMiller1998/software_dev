from unittest import TestCase
from trains.xmap.xmap import StatefulSpacedJSONParser


class TestStatefulSpacedJSONParser(TestCase):
    def test_input_parser_basic(self):
        parser = StatefulSpacedJSONParser('"a""b"{"c": "d"}')
        self.assertEqual(
            parser.read_string(), 'a'
        )
        self.assertEqual(
            parser.read_string(), 'b'
        )
        self.assertDictEqual(
            parser.read_object(),
            {'c': 'd'}
        )

    def test_input_parser_test(self):
        parser = StatefulSpacedJSONParser('\t"\\n\\ta"\t\t"b"\n  \t{"c":\t"d"}')
        self.assertEqual(
            parser.read_string(), '\n\ta'
        )
        self.assertEqual(
            parser.read_string(), 'b'
        )
        self.assertDictEqual(
            parser.read_object(),
            {'c': 'd'}
        )
