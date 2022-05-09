import math


class Graph:
    def __init__(self, m, c):
        """

        :param m: gradient of the graph
        :param c: constant coefficient
        """
        self.m = m
        self.c = c

    def __call__(self, x=None, lb=None, ub=None, *args, **kwargs):
        """
        Run the graph function or create a period

        :param x: the input for the graph
        :param lb: lower bound
        :param ub: upper bound
        :param args: any additional args for the graph function
        :param kwargs: any additional kwargs for the graph function
        :return: a Period or Number
        """
        if lb or ub:
            return Period(self, lb, ub)
        elif x is not None:
            return self.func(x)

    def __repr__(self):
        return f"Graph(m={self.m}, c={self.c})"

    def func(self, x):
        """
        The function for the graph

        :param x: the input
        :return: a Number (y-value)
        """
        return 0


class Period:
    def __init__(self, graph, lb, ub):
        """

        :param graph: the graph over which the period operates
        :param lb: the lower bound of the domain (defaults to -inf if None)
        :param ub: the upper bound of the domain (defaults to inf if None)
        """
        self.graph = graph

        if not lb: lb = -math.inf
        if not ub: ub = math.inf

        if lb >= ub:
            raise ValueError(f"invalid upper ({ub}) and lower ({lb}) bounds")

        self.lb = lb
        self.ub = ub

    def __call__(self, x, *args, **kwargs):
        """
        Runs the graph function

        :param x: the input for the graph
        :param args: any additional args for the graph function
        :param kwargs: any additional kwargs for the graph function
        :return: a Period or Number
        """
        return self.graph.func(x)

    def __rshift__(self, other):
        """
        Creates a periodic to compose the periods

        :param other: the period to follow
        :return: a Periodic
        """
        if isinstance(other, Period) and self.ub and other.lb:
            if self.ub == other.lb:
                return Periodic(self, other)
            raise ValueError(f"upper ({self.ub}) and lower ({other.lb}) bounds do not match")
        raise TypeError(f"cannot composite {type(self)} with {type(other)}")

    def __repr__(self):
        return f"Period({self.graph} over {self.lb} to {self.ub})"


class Periodic:
    def __init__(self, *periods):
        """

        :param periods: the periods in this Periodic (assumed to be in order)
        """
        self.periods = list(periods)

    def __call__(self, x, *args, **kwargs):
        """
        Run the graph function for the matching period

        :param x: the input for the graph
        :param args: any additional args for the graph function
        :param kwargs: any additional kwargs for the graph function
        :return: a Number
        """
        for p in self.periods:
            if p.lb < x <= p.ub:
                return p(x)

    def __rshift__(self, other):
        """
        Add Period on the right to the Periodic
        :param other: the period to append
        :return: a Periodic (self)
        """
        if isinstance(other, Period) and self.periods[-1].ub and other.lb:
            if self.periods[-1].ub == other.lb:
                self.periods.append(other)
                return self
            raise ValueError(f"upper ({self.periods[-1].ub}) and lower ({other.lb}) bounds do not match")
        raise TypeError(f"cannot composite {type(self)} with {type(other)}")

    def __repr__(self):
        return "\n".join(map(repr, self.periods))
