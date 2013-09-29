import unittest
from function import *
import errors


class TestDer(unittest.TestCase):

    def setUp(self):
        self.x, self.y, self.z = var('x'), var('y'), var('z')
        x = self.x
        self.fs = [
            (5 * x ** 2 + 3 * x + 4,
             5 * (2 * x) + 3),
            (x ** 2 * sin(x),
             2 * x * sin(x) + x ** 2 * cos(x)),
            ((x ** 2 + cos(x)) ** 0.5,
             0.5 * (x ** 2 + cos(x)) ** (-0.5) * (2 * x + (-sin(x))))
        ]

    def test_derivatives(self):
        for i in self.fs:
            self.assertEqual(i[0].derivative(self.x), i[1])

    def test_create_function(self):
        f = create_function(
            lambda x, y: (x ** 5 + y * sin(x * y)) + log(y, 7 / x))
        x = self.x
        y = self.y
        self.assertEqual(f, (x ** 5 + (y * sin(x * y)) + log(y, 7 / x)))

    def test_mult_var_der(self):
        f = create_function(
            lambda x, y: x ** 5 + y * sin(x * y) + log(y, 7 / x))
        g = f.derivative('y')

    def test_antider_const(self):
        const = 3
        fconst = create_const(const)
        self.assertEqual(fconst.antiderivative(self.x), fconst * self.x)

    def test_antider_mult(self):
        x = self.x
        f = x ** 2 - 2 * x + 5
        self.assertEqual(
            x ** 3 / 3 - 2 * (x ** 2 / 2) + 5 * x, f.antiderivative())

    def test_get_multipliers(self):
        x = self.x
        y = self.y
        f = 2 * x ** 3 * (x + y) ** 5 / (x / y)
        g = {'down': {x: 1}, 'up': {y: 1, x: 3, create_const(2): 1, x + y: 5}}
        self.assertEqual(f.get_multipliers(), g)

    def test_simplify_mult(self):
        x = self.x
        f = x ** 3 / x / x
        self.assertEqual(f.simplify_mult(), x)
        f = x / x
        self.assertEqual(f.simplify_mult(), create_const(1))
        f = 2 * (x ** 2 / 2)
        self.assertEqual(f.simplify_mult(), x ** 2)

    def test_simplify_sum(self):
        x = self.x
        y = self.y
        self.assertEqual((x + 6 * 9 * y - 5 + x).simplify_sum(), 54 * y + 2 * x - 5)


if __name__ == '__main__':
    unittest.main()
