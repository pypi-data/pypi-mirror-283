# SPDX-FileCopyrightText: 2023-present JACS <jacs@zbc.dk>
#
# SPDX-License-Identifier: MIT

from math import pi

from numpy import mean, median, std, var
from spb import plot, plot3d_implicit, plot3d_list, plot_geometry, plot_implicit, plot_list
from sympy import (
    Function,
    Matrix,
    N,
    Piecewise,
    Symbol,
    acos,
    asin,
    atan,
    cos,
    diff,
    dsolve,
    exp,
    expand,
    factor,
    integrate,
    limit,
    ln,
    log,
    nsolve,
    sin,
    solve,
    sqrt,
    symbols,
    tan,
)

from .config import _configure_spb
from .logarithm import log10
from .ode import plot_ode
from .plot_helpers import plot_points
from .regression import regression_exp, regression_poly, regression_power
from .stat_plot import boxplot, plot_bars, plot_hist, plot_sum
from .stats import (
    degroup,
    frekvenstabel,
    group,
    group_mean,
    group_percentile,
    group_std,
    group_var,
    kvartiler,
    percentile,
)
from .trigonometry import Cos, Sin, Tan, aCos, aSin, aTan
from .vector import plot3d_line, plot3d_plane, plot_vector, plot_vector_field

a, b, c, d, e, f, g, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = symbols(
    "a b c d e f g i j k l m n o p q r s t u v w x y z", real=True
)

_configure_spb()

plot.__doc__ = """Afbilder en eller flere funktioner af en variabel.

- Afbildning af en funktion med standardindstillinger:

`plot( f(x) , **kwargs)`

- Flere funktioner med tilpasset x- og y-akse:

`plot( f(x), g(x), (x,0,35), ylim=(0,300)`

- Funktioner med beskrivelser:

`plot( f(x), g(x),
    xlabel="x-værdier", ylabel= "y-værdier",
    label=["f(x)","g(x)"], title="Grafer for f og g")`

- Logaritmisk koordinatsystem:

`plot( f(x) , yscale="log")`

- Dobbeltlogaritmisk koordinatsystem:

`plot( f(x) , (variabel, start, stop), xscale="log", yscale="log")`

Se også
==========
- Parametre linje: [2D line](https://sympy-plot-backends.readthedocs.io/en/latest/modules/graphics/functions_2d.html#spb.graphics.functions_2d.line)
- Parametre figur: [Graphics](https://sympy-plot-backends.readthedocs.io/en/latest/modules/graphics/graphics.html)
- Returværdi: [Plot](https://sympy-plot-backends.readthedocs.io/en/latest/modules/backends/plot.html)
"""
