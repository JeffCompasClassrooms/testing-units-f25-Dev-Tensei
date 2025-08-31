import math
import unittest
from circle import Circle

class TestCircle(unittest.TestCase):
    def test_initial_getRadius(self):
        c = Circle(10)
        self.assertEqual(c.getRadius(), 10)

    def test_setRadius_valid_updates_and_returns_true(self):
        c = Circle(10)
        result = c.setRadius(20)
        self.assertTrue(result)
        self.assertEqual(c.getRadius(), 20)

    def test_setRadius_rejects_negative_and_leaves_value(self):
        c = Circle(5)
        result = c.setRadius(-3)
        self.assertFalse(result)
        self.assertEqual(c.getRadius(), 5)

    def test_getArea_standard(self):
        c = Circle(10)
        self.assertAlmostEqual(c.getArea(), math.pi * 100, places=12)

    def test_getCircumference_standard(self):
        c = Circle(10)
        self.assertAlmostEqual(c.getCircumference(), 2 * math.pi * 10, places=12)

    def test_getArea_zero(self):
        c = Circle(0)
        self.assertAlmostEqual(c.getArea(), 0.0, places=12)

    def test_getCircumference_zero(self):
        c = Circle(0)
        self.assertAlmostEqual(c.getCircumference(), 0.0, places=12)

    def test_getArea_negative_radius_behaves_like_r_squared(self):
        c = Circle(-1)
        self.assertAlmostEqual(c.getArea(), math.pi * 1, places=12)

    def test_getCircumference_negative_radius_is_linear_in_r(self):
        c = Circle(-1)
        self.assertAlmostEqual(c.getCircumference(), -2 * math.pi * 1, places=12)

    def test_area_bug_when_radius_equals_two(self):
        c = Circle(2)
        self.assertAlmostEqual(c.getArea(), 4 * math.pi, places=12)

if __name__ == "__main__":
    unittest.main()