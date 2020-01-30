import unittest
import utility

class TestUtility(unittest.TestCase):
    def setUp(self):
        pass

    def test_commalist(self):
        list_none = None
        list_zero = []
        list_one = [ "abc" ]
        list_two = [ "abc", "def"]
        list_multiple = [ "abc", "def", "ghi" ]

        self.assertEqual(utility.commalist(list_none), "")
        self.assertEqual(utility.commalist(list_zero), "")
        self.assertEqual(utility.commalist(list_one), "abc")
        self.assertEqual(utility.commalist(list_two), "abc and def")
        self.assertEqual(utility.commalist(list_multiple), "abc, def and ghi")
