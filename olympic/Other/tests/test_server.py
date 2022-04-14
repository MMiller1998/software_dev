import unittest
import asyncio
import json

from unittest.mock import MagicMock, patch

from trains.remote.server import TrainsServer, MAX_NUM_PLAYERS, CLIENT_NAME_WAIT_SEC
from tests.helpers.mock_streams import MockStreamReader, MockTimeoutStreamReader


class TestServer(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_receive_and_validate_client_name_go_right(self):
        mock_reader = MockStreamReader(b'"some dummy data"')
        self.assertEqual(
            self.loop.run_until_complete(TrainsServer.receive_and_validate_client_name(mock_reader)),
            'some dummy data'
        )

    def test_receive_and_validate_client_name_too_long(self):
        mock_reader = MockStreamReader(b'"more than fifty characters worth of content blahblahblah"')
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(TrainsServer.receive_and_validate_client_name(mock_reader))

    def test_receive_and_validate_client_name_non_ascii(self):
        mock_reader = MockStreamReader('©'.encode('utf-8'))
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(TrainsServer.receive_and_validate_client_name(mock_reader))

    def test_receive_and_validate_client_name_timeout(self):
        mock_reader = MockTimeoutStreamReader(CLIENT_NAME_WAIT_SEC + 1)
        with self.assertRaises(asyncio.exceptions.TimeoutError):
            self.loop.run_until_complete(TrainsServer.receive_and_validate_client_name(mock_reader))

    def test_receive_and_validate_client_name_bad_json(self):
        mock_reader = MockStreamReader(b"this isn't json")
        with self.assertRaises(json.decoder.JSONDecodeError):
            self.loop.run_until_complete(TrainsServer.receive_and_validate_client_name(mock_reader))


    @patch('trains.remote.server.asyncio.streams.StreamWriter')
    def test_handle_client_connect_signups_full(self, mock_stream_writer_class):
        mock_stream_writer = mock_stream_writer_class.return_value

        server = TrainsServer()
        server.clients = ['fake client' for _ in range(MAX_NUM_PLAYERS)]

        self.loop.run_until_complete(server.handle_client_connect('fake reader', mock_stream_writer))
        mock_stream_writer.close.assert_called_once()

    def test_handle_client_connect_go_right(self):
        mock_stream_reader = MockStreamReader(b'"player"')

        server = TrainsServer()
        self.assertEqual(len(server.clients), 0)

        self.loop.run_until_complete(server.handle_client_connect(mock_stream_reader, 'fake writer'))
        self.assertEqual(len(server.clients), 1)

    def test_handle_client_connect_final_signup(self):
        mock_stream_reader = MockStreamReader(b'"player"')

        server = TrainsServer()
        server.clients = ['fake client' for _ in range(MAX_NUM_PLAYERS - 1)]
        server.got_enough_signups = self.loop.create_future()

        self.loop.run_until_complete(server.handle_client_connect(mock_stream_reader, 'fake writer'))
        self.assertTrue(server.got_enough_signups.done())
        self.assertTrue(server.got_enough_signups.result())

    def test_check_signups_not_enough(self):
        server = TrainsServer()
        server.got_enough_signups = self.loop.create_future()
        mock_on_failure = MagicMock()

        server.check_signups(5, mock_on_failure)

        self.assertFalse(server.got_enough_signups.done())
        mock_on_failure.assert_called_once()

    def test_check_signups_enough(self):
        min_num_signups = 5

        server = TrainsServer()
        server.clients = ['fake client' for _ in range(min_num_signups)]
        server.got_enough_signups = self.loop.create_future()
        mock_on_failure = MagicMock()

        server.check_signups(min_num_signups, mock_on_failure)

        self.assertTrue(server.got_enough_signups.done())
        self.assertTrue(server.got_enough_signups.result())
        mock_on_failure.assert_not_called()
