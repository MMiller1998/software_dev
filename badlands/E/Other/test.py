import unittest
from io import BytesIO
from c import reverse_json
from main import get_port
from tcp_json_reverser import TCPJsonReverser


class ETests(unittest.TestCase):
    def test_get_port_default(self):
        self.assertEqual(45678, get_port(["Other/main.py"]))

    def test_get_port(self):
        self.assertEqual(11111, get_port(["Other/main.py", "11111"]))

    def test_tcp_handler(self):
        mock_reader = BytesIO('{"foo" : "bar" } 123'.encode())
        mock_out = BytesIO()
        TCPJsonReverser._read_and_write_reversed_json(mock_reader, mock_out)
        mock_out.seek(0)

        self.assertEqual('{"foo": "rab"}\n-123\n', mock_out.read().decode())


    def test_reverse_json(self):
        initial_json = {
            "str": "hello",
            "int": 5,
            "negative_int": -5,
            "zero": 0,
            "true": True,
            "false": False,
            "none": None,
            "object": {
                "firstkey": "firstval",
                "secondkey": "secondval",
                "thirdkey": [3, 4, [10, 15]]
            },
            "array": [True, "suh", { "key": "val"}]
        }
        expected_json = {
            "str": "olleh",
            "int": -5,
            "negative_int": 5,
            "zero": 0,
            "true": False,
            "false": True,
            "none": None,
            "object": {
                "firstkey": "lavtsrif",
                "secondkey": "lavdnoces",
                "thirdkey": [[-15, -10], -4, -3]
            },
            "array": [{"key": "lav"}, "hus", False]
        }
        self.assertEqual(expected_json, reverse_json(initial_json))


if __name__ == '__main__':
    unittest.main()
