import math
from functools import reduce
import errors


class Function:

    def derivative(self, var='x'):
        if hasattr(var, '__iter__'):
            return reduce(Function.derivative, [self] + var)
        return self._der(self._check_or_create_var(var))

    def antiderivative(self, var='x'):
        var = self._check_or_create_var(var)
        if not self.depends_on(var):
            return self * var
        return self._antider(var)

    def depends_on(self, var):
        return self._depends_on(self._check_or_create_var(var))

    @staticmethod
    def _create_const(num):
        if num < 0:
            return Funminus(Fconst(-num))
        else:
            return Fconst(num)

    @staticmethod
    def _check_or_create_var(var):
        if var.__class__ == Fvar:
            return var
        elif var.__class__ == str:
            return Fvar(var)
        else:
            raise ValueError("var should be Fvar or string")

    def _check_for_num(self, num):
        if isinstance(num, (int, float, long)):
            return self._create_const(num)
        else:
            return num

    def __mul__(self, other):
        other = self._check_for_num(other)

        if self.is_zero() or other.is_zero():
            return Fconst(0)
        if self.is_one():
            return other
        elif other.is_one():
            return self
        else:
            return Fmult(self, other)

    def __rmul__(self, other):
        other = self._check_for_num(other)
        return other.__mul__(self)

    def __add__(self, other):
        other = self._check_for_num(other)

        if self.is_zero():
            return other
        elif other.is_zero():
            return self
        else:
            return Fsum(self, other)

    def __radd__(self, other):
        other = self._check_for_num(other)

        return other.__add__(self)

    def __sub__(self, other):
        other = self._check_for_num(other)

        if self.is_zero():
            return -other
        elif other.is_zero():
            return self
        else:
            return Fsub(self, other)

    def __rsub__(self, other):
        other = self._check_for_num(other)

        return other.__sub__(self)

    def __div__(self, other):
        other = self._check_for_num(other)

        if self.is_zero() or other.is_one():
            return self
        return Fdiv(self, other)

    def __rdiv__(self, other):
        other = self._check_for_num(other)

        return other.__div__(self)

    def __pow__(self, other):
        other = self._check_for_num(other)

        if other.is_zero():
            return Fconst(1)
        if other.is_one():
            return self
        return Fpower(self, other)

    def __rpow__(self, other):
        other = self._check_for_num(other)

        return other.__pow__(self)

    def __neg__(self):
        if self.is_zero():
            return self
        if self.__class__ == Funminus:
            return self.arg
        return Funminus(self)

    def __eq__(self, other):
        raise Exception

    def _priority(self):
        priority = {
            Fsum: 1,
            Fsub: 1,
            Funminus: 1.5,
            Fmult: 2,
            Fdiv: 2,
            Fpower: 3,
            Fvar: 4,
            Fconst: 4,
            Fsin: 5,
            Fcos: 5,
            Fln: 5,
            Flog: 5,
        }
        return priority[self.__class__]

    def brace_repr(self, other):
        if self._priority() < other._priority() or self._priority() == other._priority() and self.__class__ in (Fdiv, Fsin, Fcos, Flog, Fln):
            return '(' + repr(self) + ')'
        else:
            return repr(self)

    def is_zero(self):
        return self.__class__ == Fconst and self.c == 0

    def is_one(self):
        return self.__class__ == Fconst and self.c == 1


class Fconst(Function):

    def __init__(self, c):
        self.c = c

    def __call__(self, val=None, **args):
        return self.c

    def __repr__(self):
        return repr(self.c)

    def __eq__(self, other):
        if isinstance(other, (int, float, long)):
            return self.c == other
        return other.__class__ == Fconst and self.c == other.c

    def _der(self, var):
        return Fconst(0)

    def _antider(self, var):
        return self * var

    def _depends_on(self, var):
        return False


class Fvar(Function):

    def __init__(self, var='x'):
        self.var = var

    def __call__(self, val=None, **args):
        if len(args) == 0 and val is None:
            raise Exception
        if val is not None:
            if len(args) != 0:
                raise Exception
            return val
        return args[self.var]

    def __repr__(self):
        return self.var

    def __eq__(self, other):
        return other.__class__ == Fvar and self.var == other.var

    def _der(self, var):
        if var == self.var or self == var:
            return Fconst(1)
        else:
            return Fconst(0)

    def _antider(self, var):
        if self == var:
            return self ** 2 / 2
        else:
            return self * var

    def _depends_on(self, var):
        return self == var


class Fsum(Function):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, val=None, **args):
        return self.left(val, **args) + self.right(val, **args)

    def __repr__(self):
        return self.left.brace_repr(self) + ' + ' + self.right.brace_repr(self)

    def __eq__(self, other):
        return other.__class__ == Fsum and self.left == other.left and self.right == other.right

    def _der(self, var):
        return self.left.derivative(var) + self.right.derivative(var)

    def _antider(self, var):
        return self.left._antider(var) + self.right._antider(var)

    def _depends_on(self, var):
        return self.left.depends_on(var) or self.right.depends_on(var)


class Fsub(Function):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, val=None, **args):
        return self.left(val, **args) - self.right(val, **args)

    def __repr__(self):
        return self.left.brace_repr(self) + ' - ' + self.right.brace_repr(self)

    def __eq__(self, other):
        return other.__class__ == Fsub and self.left == other.left and self.right == other.right

    def _der(self, var):
        return self.left.derivative(var) - self.right.derivative(var)

    def _antider(self, var):
        return self.left._antider(var) - self.right._antider(var)

    def _depends_on(self, var):
        return self.left.depends_on(var) or self.right.depends_on(var)


class Fmult(Function):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, val=None, **args):
        return self.left(val, **args) * self.right(val, **args)

    def __repr__(self):
        return self.left.brace_repr(self) + ' * ' + self.right.brace_repr(self)

    def __eq__(self, other):
        return other.__class__ == Fmult and self.left == other.left and self.right == other.right

    def _der(self, var):
        return self.left.derivative(var) * self.right + self.left * self.right.derivative(var)

    def _antider(self, var):
        if not self.left.depends_on(var):
            return self.left * self.right.antiderivative(var)
        elif not self.right.depends_on(var):
            return self.left.antiderivative(var) * self.right
        else:
            raise errors.CantFindAntiDerivativeException()

    def _depends_on(self, var):
        return self.left.depends_on(var) or self.right.depends_on(var)


class Fdiv(Function):

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __call__(self, val=None, **args):
        return self.numerator(val, **args) * 1.0 / self.denominator(val, **args)

    def __repr__(self):
        return self.numerator.brace_repr(self) + ' / ' + self.denominator.brace_repr(self)

    def __eq__(self, other):
        return other.__class__ == Fdiv and self.numerator == other.numerator and self.denominator == other.denominator

    def _der(self, var):
        return ((self.numerator.derivative(var) * self.denominator - self.numerator * self.denominator.derivative(var))
                / self.denominator ** 2)

    def _antider(self, var):
        if not self.denominator.depends_on(var):
            return self.numerator.antiderivative(var) * self.denominator
        else:
            raise errors.CantFindAntiDerivativeException()

    def _depends_on(self, var):
        return self.numerator.depends_on(var) or self.denominator.depends_on(var)


class Fpower(Function):

    def __init__(self, f, power):
        self.f = f
        self.power = power

    def __call__(self, val=None, **args):
        return self.f(val, **args) ** self.power(val, **args)

    def __repr__(self):
        return self.f.brace_repr(self) + ' ** ' + self.power.brace_repr(self)

    def __eq__(self, other):
        return other.__class__ == Fpower and self.f == other.f and self.power == other.power

    def _der(self, var):
        if self.power.__class__ == Fconst:
            return self.power * self.f ** (self.power.c - 1) * self.f.derivative(var)
        elif self.f.__class__ == Fconst:
            return self * Fln(self.f) * self.power.derivative(var)
        else:
            return self * (Fln(self.f) * self.power.derivative(var) + (self.power * self.f.derivative(var)) / self.f)

    def _depends_on(self, var):
        return self.f.depends_on(var) or self.power.depends_on(var)

    def _antider(self, var):
        if self.f == var and self.power.__class__ == Fconst:
            c = Fconst(self.power.c + 1)
            return self.f ** c / c
        elif self.f.__class__ == Fconst and self.power == var:
            return self / math.ln(self.f.c)
        else:
            raise errors.CantFindAntiDerivativeException()


class Fsin(Function):

    def __init__(self, arg):
        self.arg = arg

    def __call__(self, val=None, **args):
        return math.sin(self.arg(val, **args))

    def __repr__(self):
        return 'sin' + self.arg.brace_repr(self)

    def __eq__(self, other):
        return other.__class__ == Fsin and self.arg == other.arg

    def _der(self, var):
        return Fcos(self.arg) * self.arg.derivative(var)

    def _depends_on(self, var):
        return self.arg.depends_on(var)

    def _antider(self, var):
        if self.arg == var:
            return -Fcos(var)
        else:
            raise errors.CantFindAntiDerivativeException()


class Fcos(Function):

    def __init__(self, arg):
        self.arg = arg

    def __call__(self, val=None, **args):
        return math.cos(self.arg(val, **args))

    def __repr__(self):
        return 'cos' + self.arg.brace_repr(self)

    def __eq__(self, other):
        return other.__class__ == Fcos and self.arg == other.arg

    def _der(self, var):
        return -Fsin(self.arg) * self.arg.derivative(var)

    def _depends_on(self, var):
        return self.arg.depends_on(var)

    def _antider(self, var):
        if self.arg == var:
            return Fsin(var)
        else:
            raise errors.CantFindAntiDerivativeException()


class Funminus(Function):

    def __init__(self, arg):
        self.arg = arg

    def __call__(self, val=None, **args):
        return -(self.arg(val, **args))

    def __repr__(self):
        return '-' + self.arg.brace_repr(self)

    def __eq__(self, other):
        return other.__class__ == Funminus and self.arg == other.arg

    def _der(self, var):
        return -self.arg.derivative(var)

    def _depends_on(self, var):
        return self.arg.depends_on(var)

    def _antider(self, var):
        return -self.arg.antiderivative()


class Fln(Function):

    def __init__(self, arg):
        self.arg = arg

    def __call__(self, val=None, **args):
        return math.log(self.arg(val, **args))

    def __repr__(self):
        return 'ln' + self.arg.brace_repr(self)

    def __eq__(self, other):
        return other.__class__ == Fln and self.arg == other.arg

    def _der(self, var):
        return self.arg.derivative(var) / self.arg

    def _depends_on(self, var):
        return self.arg.depends_on(var)

    def _antider(self, var):
        if self.arg == var:
            return var * self - var
        else:
            raise errors.CantFindAntiDerivativeException()


class Flog(Function):

    def __init__(self, base, arg):
        self.base = base
        self.arg = arg

    def __call__(self, val=None, **args):
        return math.log(self.base(val, **args), self.arg(val, **args))

    def __repr__(self):
        return 'log[' + repr(self.base) + ']' + self.arg.brace_repr(self)

    def __eq__(self, other):
        return (other.__class__ == Flog and self.arg == other.arg and self.base == other.base or
                other._class__ == Fln and self.base == math.e and self.arg == other.arg)

    def _der(self, var):
        return (Fln(self.arg).derivative(var) - Fln(self.base).derivative(var) * self) / Fln(self.base)

    def _depends_on(self, var):
        return self.arg.depends_on(var) or self.base.depends_on(var)

    def _antider(self, var):
        if self.arg == var and self.base.__class__ == Fconst:
            return var * self - math.log(math.e, self.base.c) * var
        else:
            raise errors.CantFindAntiDerivativeException()


var, sin, cos, ln, log = Fvar, Fsin, Fcos, Fln, Flog


def create_function(function):
    varnames = function.func_code.co_varnames
    return function(*(Fvar(i) for i in varnames))
