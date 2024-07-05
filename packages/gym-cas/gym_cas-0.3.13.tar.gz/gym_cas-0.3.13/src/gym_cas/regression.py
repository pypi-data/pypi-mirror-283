from typing import Callable

from numpy import corrcoef
from numpy.polynomial import Polynomial
from spb import plot, plot_list
from spb.defaults import TWO_D_B  # type: ignore
from sympy import Lambda, N, exp, latex, ln, simplify
from sympy.abc import t, x


def reg_poly(x_points, y_points, deg):
    p = Polynomial.fit(x_points, y_points, deg)
    ps = simplify(p(x))

    yp = [float(N(p(x))) for x in x_points]
    r2 = float(corrcoef(yp, y_points)[0][1] ** 2)
    return Lambda(t, ps.subs(x, t)), r2


def reg_pow(x_points, y_points, _):
    x_log = [float(N(ln(x))) for x in x_points]
    y_log = [float(N(ln(y))) for y in y_points]

    p = Polynomial.fit(x_log, y_log, 1)
    ps = exp(p.convert().coef[0]) * x ** p.convert().coef[1]

    yp = [float(N(p(x))) for x in x_log]
    r2 = float(corrcoef(yp, y_log)[0][1] ** 2)
    return Lambda(t, ps.subs(x, t)), r2


def reg_exp(x_points, y_points, _):
    y_log = [float(N(ln(y))) for y in y_points]

    p = Polynomial.fit(x_points, y_log, 1)
    ps = exp(p.convert().coef[0]) * exp(p.convert().coef[1]) ** x

    yp = [float(N(p(x))) for x in x_points]
    r2 = float(corrcoef(yp, y_log)[0][1] ** 2)
    return Lambda(t, ps.subs(x, t)), r2


class RegressionFun:
    """
    Funktion dannet ud fra regression.

    Attributer
    ---
    f : funktionen
    r2 : forklaringsgrad
    plot : grafisk afbildning
    """

    def __init__(self, f: Lambda, r2: float, plot: TWO_D_B):
        self.f = f
        self.r2 = r2
        self.plot = plot

    def __call__(self, *args):
        return self.f(*args)

    def __str__(self):
        return self.f.__str__()

    def _repr_latex_(self):
        return self.f._repr_latex_()


def regression(
    x_points: list[float],
    y_points: list[float],
    deg: int,
    method: Callable[[list[float], list[float], int], tuple[Lambda, float]],
    *,
    show=True,
):
    fun, r2 = method(x_points, y_points, deg)

    p1 = plot_list(x_points, y_points, is_point=True, show=False, title=f"Forklaringsgrad $R^2 = {r2:.3}$")
    p2 = plot(fun(x), (x, min(x_points), max(x_points)), show=False, use_latex=True)
    plt = p1 + p2
    plt.series[1]._latex_label = latex(plt.series[1].expr)
    if show:
        plt.show()

    return RegressionFun(fun, r2, plt)


def regression_poly(x_points: list[float], y_points: list[float], deg: int, *, show=True):
    """
    Polynomial regression.

    Parameters
    ---

    x_points, y_points : list
        Datapoints

    deg : int
        Degree of polynomial. Use deg = 1 for linear interpolation

    show : bool, default = True
        Whether to show plot
    """
    return regression(x_points, y_points, deg, reg_poly, show=show)


def regression_power(x_points: list[float], y_points: list[float], *, show=True):
    """
    Power regression.

    Parameters
    ---

    x_points, y_points : list
        Datapoints

    show : bool, default = True
        Whether to show plot
    """
    return regression(x_points, y_points, 1, reg_pow, show=show)


def regression_exp(x_points: list[float], y_points: list[float], *, show=True):
    """
    Exponential regression.

    Parameters
    ---

    x_points, y_points : list
        Datapoints

    show : bool, default = True
        Whether to show plot
    """
    return regression(x_points, y_points, 1, reg_exp, show=show)


if __name__ == "__main__":
    f = regression_poly([1, 2, 3], [3, 6, 12], 1, show=False)
    print(f(x))
    print(f(2.0))

    p = regression_poly([1, 2, 3, 4], [3, 6, 12, 4], 2, show=False)
    print(p(x))
    print(p(2.0))

    f2 = regression_power([1, 2, 3], [3, 6, 12], show=False)
    print(f2(x))
    print(f2(2.0))

    f3 = regression_exp([1, 2, 3], [3, 6, 12], show=False)
    print(f3(x))
    print(f3(2.0))
    print(f3.r2)

    p = f.plot + p.plot + f2.plot + f3.plot
    p.xlim = (0, 5)
    p.title = "Regression bonanza"
    p.show()
