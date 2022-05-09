import math


class Graph:
    def __init__(self, m, c):
        self.m = m
        self.c = c

    def __call__(self, x=None, lb=None, ub=None, *args, **kwargs):
        if lb or ub:
            return Period(self, lb, ub)
        elif x is not None:
            return self.func(x)

    def __repr__(self):
        return f"Graph(m={self.m}, c={self.c})"

    def func(self, x):
        return 0


class Period:
    def __init__(self, graph, lb, ub):
        self.graph = graph

        if not lb: lb = -math.inf
        if not ub: ub = math.inf

        if lb >= ub:
            raise ValueError(f"invalid upper ({ub}) and lower ({lb}) bounds")

        self.lb = lb
        self.ub = ub

    def __call__(self, x, *args, **kwargs):
        return self.graph.func(x)

    def __rshift__(self, other):
        if isinstance(other, Period) and self.ub and other.lb:
            if self.ub == other.lb:
                return Periodic(self, other)
            raise ValueError(f"upper ({self.ub}) and lower ({other.lb}) bounds do not match")
        raise TypeError(f"cannot composite {type(self)} with {type(other)}")

    def __repr__(self):
        return f"Period({self.graph} over {self.lb} to {self.ub})"


class Periodic:
    def __init__(self, *periods):
        self.periods = list(periods)

    def __call__(self, x, *args, **kwargs):
        for p in self.periods:
            if p.lb < x <= p.ub:
                return p(x)

    def __rshift__(self, other):
        if isinstance(other, Period) and self.periods[-1].ub and other.lb:
            if self.periods[-1].ub == other.lb:
                self.periods.append(other)
                return self
            raise ValueError(f"upper ({self.periods[-1].ub}) and lower ({other.lb}) bounds do not match")
        raise TypeError(f"cannot composite {type(self)} with {type(other)}")

    def __repr__(self):
        return "\n".join(map(repr, self.periods))
