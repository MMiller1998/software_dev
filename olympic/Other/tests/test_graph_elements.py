from unittest import TestCase

import tests.examples.milestone2 as example


class TestTrainPlace(TestCase):

    def test_get_connections_between(self):
        self.assertSetEqual(
            example.bwi2.get_connections_between(example.bos),
            {example.c_bwi_bos1, example.c_bwi_bos2}
        )
        self.assertSetEqual(
            example.bos.get_connections_between(example.bwi2),
            {example.c_bwi_bos1, example.c_bwi_bos2}
        )
        self.assertSetEqual(example.bwi2.get_connections_between(example.lax), {example.c_bwi_lax})
        self.assertSetEqual(example.iad.get_connections_between(example.bos), set())
