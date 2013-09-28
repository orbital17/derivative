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
        fconst = Fconst(const)
        self.assertEqual(fconst.antiderivative(self.x), fconst * self.x)

    def test_antider_mult(self):
        x = self.x
        f = x ** 2 - 2 * x + 5
        self.assertEqual(
            x ** 3 / 3 - 2 * (x ** 2 / 2) + 5 * x, f.antiderivative())

if __name__ == '__main__':
    unittest.main()
