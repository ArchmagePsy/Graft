import math

from graph import Graph


class Constant(Graph):
    def __init__(self, c):

        Graph.__init__(self, 0, c)

    def __repr__(self):
        return str(self.c)

    def func(self, x):
        return self.c


class Linear(Graph):
    def __repr__(self):
        return f"{self.m}x{signed(self.c, no_zero=True)}"

    def func(self, x):
        return self.m * x + self.c


def signed(number, no_zero=False):
    if number > 0:
        return f"+{number}"
    elif no_zero and number == 0:
        return ""
    else:
        return str(number)


class Polynomial(Graph):
    def __init__(self, m, c):

        for i in filter(lambda x: x[1] == 0, m):
            c += i[0]

        Graph.__init__(self, list(filter(lambda x: x[1] != 0, m)), c)

    def __repr__(self):
        return f"{self.m[0][0]}x^{self.m[0][1]}" + "".join(f"{signed(coefficient)}x^{index}" for coefficient, index in self.m[1:]) + signed(self.c, no_zero=True)

    def func(self, x):
        return sum(coefficient * x ** index for coefficient, index in self.m) + self.c


class Functional(Graph):
    def __init__(self, function, graph, *args, **kwargs):

        Graph.__init__(self, 0, 0)

        self.name = function.__name__

        def func_wrapper(x):
            return function(graph.func(x), *args, **kwargs)

        self.function = func_wrapper
        self.graph = graph

    def __repr__(self):
        return f"{self.name}({self.graph})"

    def func(self, x):
        return self.function(x)


class Absolute(Functional):
    def __init__(self, graph):

        Functional.__init__(self, abs, graph)


class Logarithmic(Functional):
    def __init__(self, graph, base=10):

        Functional.__init__(self, math.log, graph, base=base)