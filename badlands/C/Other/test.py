import unittest
from main import reverse_json


class ReverseJsonTest(unittest.TestCase):
    def test_all_of_it(self):
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
        self.assertEqual(reverse_json(initial_json), expected_json)


if __name__ == '__main__':
    unittest.main()
