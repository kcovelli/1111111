from typing import List, Callable, Union


class Token:
    left: Union['Token', None]
    right: Union['Token', None]
    func: Callable[['Token', 'Token'], int]

    def __init__(self, func):
        # noinspection PyTypeChecker
        self.left, self.right = None, None
        self.func = func
        print(self.getsymbol())

    def eval(self) -> int:
        return self.func(self.left, self.right)

    def getsymbol(self):
        return SYMBOL_DICT[self.func]

    def __str__(self):
        return '(' + str(self.left) + self.getsymbol() + str(self.right) + ')'


def check(var):
    return var if isinstance(var, int) else 0 if var is None else var.eval()


def add(left: 'Token', right: 'Token') -> int:
    """ adds result of all childrens func calls """
    return check(left) + check(right)


def sub(left: 'Token', right: 'Token') -> int:
    """ subtracts resulf of all childrens func calls """
    return check(left) - check(right)


def mul(left: 'Token', right: 'Token') -> int:
    """ multiplies result of all childrens func calls """
    return check(left) * check(right)


def concat(left: 'Token', right: 'Token') -> int:
    """ concatinates all childrens func calls """
    return int(str(check(left)) + str(check(right)))


def mod(left: 'Token', right: 'Token') -> int:
    return check(left) % check(right)


SYMBOL_DICT = {add: '+', sub: '-', mul: '*', concat: '|', mod: '%', None: ''}

# (1+1)*(1|((1+(1+1))*(1+1)-1)
leaf = [1] * 9
a0 = Token(add)
a0.left, a0.right = leaf[0:2]
a1 = Token(add)
a1.left, a1.right = leaf[2], a0
a2 = Token(add)
a2.left, a2.right = leaf[3:5]
m0 = Token(mul)
m0.left, m0.right = a1, a2

s = Token(sub)
s.left, s.right = [m0, leaf[7]]

c = Token(concat)
c.left, c.right = [leaf[1], s]

TEST_TOKEN = Token(mul)
TEST_TOKEN.left, TEST_TOKEN.right = a0, c

SMOL_TOKEN = Token(mul)
SMOL_TOKEN.left, SMOL_TOKEN.right = a0, a2
