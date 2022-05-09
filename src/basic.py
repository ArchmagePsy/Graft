import math

from src.graph import Graph


class Constant(Graph):
    def __init__(self, c):
        """

        :param c: the constant output of the graph
        """

        Graph.__init__(self, 0, c)

    def __repr__(self):
        return str(self.c)

    def func(self, x):
        """
        Given any input returns the constant

        :param x: input for the graph function
        :return: the constant (self.c)
        """
        return self.c


class Linear(Graph):
    def __repr__(self):
        return f"{self.m}x{signed(self.c, no_zero=True)}"

    def func(self, x):
        """
        Computes a linear graph in the form mx+c

        :param x: input for the graph function
        :return: a Number
        """
        return self.m * x + self.c


def signed(number, no_zero=False):
    """
    Formats a number to remove a sign for outputting

    :param number: the number to convert to a signed string
    :param no_zero: if True zero returns an empty string
    :return: signed string of the number
    """
    if number > 0:
        return f"+{number}"
    elif no_zero and number == 0:
        return ""
    else:
        return str(number)


class Polynomial(Graph):
    def __init__(self, m, c):
        """

        :param m: list of coefficients and indexes in the form [(coefficient, index), ... ]
        :param c: constant coefficient
        """

        for i in filter(lambda x: x[1] == 0, m):
            c += i[0]

        Graph.__init__(self, list(filter(lambda x: x[1] != 0, m)), c)

    def __repr__(self):
        return f"{self.m[0][0]}x^{self.m[0][1]}" + "".join(f"{signed(coefficient)}x^{index}" for coefficient, index in self.m[1:]) + signed(self.c, no_zero=True)

    def func(self, x):
        """
        Computes a polynomial graph in the form mnx^in+ ... +c (where n is the number of elements in m)
        :param x: the input for the graph function
        :return: a Number
        """
        return sum(coefficient * x ** index for coefficient, index in self.m) + self.c


class Functional(Graph):
    def __init__(self, function, graph, *args, **kwargs):
        """

        :param function: a function to wrap around the result of the graph function
        :param graph: the graph to wrap
        :param args: any additional args for the graph function
        :param kwargs: any additional kwargs for the graph function
        """

        Graph.__init__(self, 0, 0)

        self.name = function.__name__

        def func_wrapper(x):
            return function(graph.func(x), *args, **kwargs)

        self.function = func_wrapper
        self.graph = graph

    def __repr__(self):
        return f"{self.name}({self.graph})"

    def func(self, x):
        """
        Computes a graph function wrapped with a mathematical function such that g(f(x))
        :param x: the input for the graph function
        :return: a Number
        """
        return self.function(x)


class Absolute(Functional):
    def __init__(self, graph):

        Functional.__init__(self, abs, graph)


class Logarithmic(Functional):
    def __init__(self, graph, base=10):
        """

        :param graph: the graph to wrap
        :param base: the base of log to use (default is base=10)
        """

        Functional.__init__(self, math.log, graph, base=base)