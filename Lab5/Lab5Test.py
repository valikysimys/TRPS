import unittest

from Lab5TRPS import Point


class TestPoint(unittest.TestCase):

    def setUp(self):
        self.point_1 = Point(4, 5)
        self.point_2 = Point(1, -2)
        self.point_3 = Point(4, 6)
        self.point_4 = Point(5, 5)
        self.point_5 = Point(4, -5)
        self.point_6 = Point(4, 5)

    def test_add(self):
        test_point = self.point_1 + self.point_2
        self.assertEqual(test_point.x, 5)
        self.assertEqual(test_point.y, 3)

    def test_sub(self):
        test_point = self.point_1 - self.point_2
        self.assertEqual(test_point.x, 3)
        self.assertEqual(test_point.y, 7)

    def test_str(self):
        self.assertEqual(str(self.point_1), "(4,5)")

    def test_cmp(self):
        try:
            self.assertTrue(self.point_1 <= self.point_1)
        except NotImplementedError:
            None
        try:
            self.assertFalse(self.point_1 < self.point_1)
            self.assertFalse(self.point_1 < self.point_2)
            self.assertTrue(self.point_1 < self.point_3)
            self.assertTrue(self.point_1 < self.point_4)
        except NotImplementedError:
            None

        try:
            self.assertTrue(self.point_1 >= self.point_1)
        except NotImplementedError:
            None

        try:
            self.assertFalse(self.point_1 > self.point_1)
            self.assertFalse(self.point_2 > self.point_1)
            self.assertTrue(self.point_3 > self.point_1)
            self.assertTrue(self.point_4 > self.point_1)
        except NotImplementedError:
            None

        try:
            self.assertFalse(self.point_1 == self.point_2)
            self.assertFalse(self.point_1 == self.point_5)
            self.assertTrue(self.point_1 == self.point_6)
        except NotImplementedError:
            None


if __name__ == '__main__':
    unittest.main()