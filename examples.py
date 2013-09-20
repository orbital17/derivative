from function import var, sin, cos, log, create_function

x, y, z = var('x'), var('y'), var('z')

fs = [
    (5 * x ** 2 + 3 * x + 4,
     5 * (2 * x) + 3),
    (x ** 2 * sin(x),
     2 * x * sin(x) + x ** 2 * cos(x)),
    ((x ** 2 + cos(x)) ** 0.5,
     0.5 * (x ** 2 + cos(x)) ** (-0.5) * (2 * x + (-sin(x))))
]

for i in fs:
    print i[0].derivative(x) == i[1]


f = create_function(lambda x, y: x ** 5 + y * sin(x * y) + log(y, 7/x))
print f
print f.derivative()
