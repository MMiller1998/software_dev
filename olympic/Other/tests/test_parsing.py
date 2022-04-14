import unittest
import asyncio

from asyncio.streams import StreamReader

from trains.parsing import JSONStreamParser


class TestJSONStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_decode_next_value_basic(self):
        reader = StreamReader()
        reader.feed_data(b'["hello", "world"]')
        parser = JSONStreamParser(reader)

        self.assertEqual(self.loop.run_until_complete(parser.decode_next_value()), ["hello", "world"])

    def test_decode_next_value_multiple(self):
        reader = StreamReader()
        reader.feed_data(b'["hello", "world"] \t\n\r "next value"')
        parser = JSONStreamParser(reader)

        self.assertEqual(self.loop.run_until_complete(parser.decode_next_value()), ["hello", "world"])
        self.assertEqual(self.loop.run_until_complete(parser.decode_next_value()), "next value")

    def test_decode_next_value_eof(self):
        reader = StreamReader()
        reader.feed_data(b'["hello", "world"] \t\n\r "next value"')
        reader.feed_eof()
        parser = JSONStreamParser(reader)

        self.assertEqual(self.loop.run_until_complete(parser.decode_next_value()), ["hello", "world"])
        self.assertEqual(self.loop.run_until_complete(parser.decode_next_value()), "next value")
        self.assertEqual(self.loop.run_until_complete(parser.decode_next_value()), None)
        self.assertEqual(self.loop.run_until_complete(parser.decode_next_value()), None)
