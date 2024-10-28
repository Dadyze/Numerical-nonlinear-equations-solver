import re
from typing import Callable

from sympy.abc import x


class Graphable:
    def __init__(self, id: str, starter_vals: int, x_arr: list[float], y_arr: list[float], additional: dict=None, annotation_func: Callable=None):
        '''
        :param id: Name of the algorithm used to create this graph.
        :param starter_vals: Number of initial x/y value pairs provided upfront.
        :param x_arr: All x values, including initially provided values to perform calcuations.
        :param y_arr: All f(x) (y) values, including calculation on initial x values.
        :param additional: Meta-calculations required to get the final result, has intermediate values of each iteration.
        :param annotation_function: Callable to instrument a generated plot with visual aids.
        '''
        self.id = id
        self.starter_vals = starter_vals
        self.x_arr = x_arr
        self.y_arr = y_arr
        self.additional_cols = additional if additional != None else {}
        self.annotation_func = annotation_func


    def deltas(self):
        '''
        Get distance from 0 (to solve) for each iteration. Excludes initially
        provided values as these should always be 0.

        :returns: List of deltas for each iteration.
        '''
        return list(map(lambda y: abs(y), self.y_arr[self.starter_vals:]))


    def annotate(self, plot):
        '''
        Instruments the given plot with visual aids specific to the data
        represented by this graphable object.

        :param plot: Matplotlib plot to instrument.
        '''
        if self.annotation_func != None:
            self.annotation_func(plot, self.x_arr, self.y_arr)


def bisection(f, x0: float, x1: float, tolerance: float, max_iter=500) -> Graphable:
    '''
    :throws RuntimeError: When init_start and init_end are both positive or both negative.
    '''
    x_arr = [x0, x1]
    y_arr = [f.subs(x, x0).doit(), f.subs(x, x1).doit()]
    additional = {
        'Donja_granica': [],
        'Gornja_granica': []
    }

    for i in range(max_iter):
        midpoint = (x0 + x1) / 2
        f_midpoint = f.subs(x, midpoint).doit()

        x_arr.append(midpoint)
        y_arr.append(f_midpoint)
        additional['Donja_granica'].append(x0)
        additional['Gornja_granica'].append(x1)

        if abs(f_midpoint) <= tolerance or i == max_iter:
            break

        if f.subs(x, x0).doit() * f_midpoint > 0:
            x0 = midpoint
        else:
            x1 = midpoint

    return Graphable('bisection', 2, x_arr, y_arr, additional)


def secant(f, x0: float, x1: float, tolerance: float, max_iter=500) -> Graphable:
    '''
    :throws ZeroDivisionError: When f(x1) - f(x0) == 0.
    '''
    x_arr = [x0, x1]
    y_arr = [f.subs(x, x0).doit(), f.subs(x, x1).doit()]
    additional = {
        'Prva_tacka': [],
        'Druga_tacka': []
    }

    def annotation_function(plot, x_arr: list[float], y_arr: list[float]):
        plot.plot(x_arr, y_arr, 'g', linestyle = ':', zorder=3)

    for i in range(max_iter):
        f_x0, f_x1 = f.subs(x, x0).doit(), f.subs(x, x1).doit()
        x2 = x0 - (x1 - x0) * f_x0 / (f_x1 - f_x0)
        f_x2 = f.subs(x, x2).doit()

        x_arr.append(x2)
        y_arr.append(f_x2)
        additional['Prva_tacka'].append(x0)
        additional['Druga_tacka'].append(x1)

        x0, x1 = x1, x2

        if abs(f_x2) <= tolerance or i == max_iter:
            break

    return Graphable('secant', 2, x_arr, y_arr, additional, annotation_function)


def regula_falsi(f, x0: float, x1: float, tolerance: float, max_iter=500):
    x_arr = [x0, x1]
    y_arr = [f.subs(x, x0).doit(), f.subs(x, x1).doit()]
    additional = {
        'Tacka_a': [],
        'Tacka_b': []
    }

    for i in range(max_iter):
        f_x0, f_x1 = f.subs(x, x0).doit(), f.subs(x, x1).doit()
        x2 = (x0 * f_x1 - x1 * f_x0) / (f_x1 - f_x0)
        f_x2 = f.subs(x, x2).doit()

        x_arr.append(x2)
        y_arr.append(f_x2)
        additional['Tacka_a'].append(x0)
        additional['Tacka_b'].append(x1)

        if (x2 > 0):
            x1 = x2
        else:
            x0 = x2

        if abs(f_x2) <= tolerance or i == max_iter:
            break

    return Graphable('regula_falsi', 2, x_arr, y_arr, additional)


def newtons(f, df, x0: float, tolerance: float, max_iter=500):
    x_arr = [x0]
    y_arr = [f.subs(x, x0).doit()]

    for i in range(max_iter):
        f_x = f.subs(x, x0).doit()
        df_x = df.subs(x, x0).doit()
        x0 = x0 - (f_x / df_x)

        x_arr.append(x0)
        y_arr.append(f.subs(x, x0).doit())

        if abs(f_x) <= tolerance or i == max_iter:
            break

    return Graphable('newtons', 1, x_arr, y_arr)


def modified_newtons(f, df, x0: float, tolerance: float, max_iter=500):
    x_arr = [x0]
    y_arr = [f.subs(x, x0).doit()]
    x_i = x0

    for i in range(max_iter):
        f_x = f.subs(x, x_i).doit()
        df_x = df.subs(x, x0).doit()
        x_i = x_i - (f_x / df_x)

        x_arr.append(x_i)
        y_arr.append(f.subs(x, x_i).doit())

        if abs(f_x) <= tolerance or i == max_iter:
            break

    return Graphable('modified_newtons', 1, x_arr, y_arr)


def normalize_equation(equation: str) -> str:
    '''
    Sympify can't parse certian syntax which we should probably support. To
    work around this, we'll define some regexes to rearrange parts of the
    equation.

    For example, Sympy doesn't support coefficients such as "4x", so we convert
    these to "4 * x".

    :param equation: Equation to rearrange.
    :returns: Equation with identical meaning, but rearranges.
    '''
    patterns = [
        (r'(\d+)([A-Za-zπ])', lambda match: f'{match[1]} * {match[2]}', equation),
        (r'π', '3.1415'),
        (r'e', '2.718')
    ]

    for pattern in patterns:
        equation = re.sub(pattern[0], pattern[1], equation)

    return equation