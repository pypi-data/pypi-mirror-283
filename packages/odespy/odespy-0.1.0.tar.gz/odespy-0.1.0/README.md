# Odespy

Odespy is a Python library for solving various types of ordinary differential equations (ODEs). The first release (version 0.1.0) offers solutions to initial value problems (IVPs) of non-stiff type.

## (1) Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install odespy:

```
pip install odespy
```

## (2) Prerequisites

Numpy version 1.25 or higher must be installed prior to using odespy.

## (3) Functions and methods

Currently available functions in odespy:

- `rkexplicit()` for solving non-stiff IVPs. The function applies explicit embedded Runge-Kutta (RK) methods with adaptive time-stepping (variable step sizes). In particular, the following methods are available:

  - `method='rk45'` or `method='default'` of Dormand-Prince is based on the RK5(4) formula<sup>[1]</sup>
  - `method='rk78'` of Dormand-Prince is based on the RK8(7)13M formula<sup>[2]</sup>
  - `method='rkf45'` of Fehlberg is based on a 4*th*-order RK 4(5) formula<sup>[3]</sup>
  - `method='rkf78'` of Fehlberg is based on a 7*th*-order RK 7(8) formula<sup>[4]</sup>
  - `method='rkck'` of Cash-Karp is based on the RK 5(4) formula<sup>[5]</sup>
  - `method='rkv'` of Verner is based on the RK 6(5) formula<sup>[6]</sup>

- `abm4()` for solving non-stiff IVPs with jumps or discontinuity applies the 4th-order Adams-Bashforth method as a predictor and 3rd-order Adams-Moulton method as a corrector; also called the predictor-corrector method. Currently, this function only works with fixed step sizes and uses the predictor-evalute-corrector or PEC mode, with $k$ fixed point iterations per step or $\text{P(EC)}^k$.

How would we know if the equations we want to solve are stiff or non-stiff? Well, the rule of thumb is:

> Stiff equations are problems for which explicit methods don't work<sup>[7]</sup>

## (4) Usage

### `rkexplicit()` function

The required input arguments for `rkexplicit()` are as follows:

- function
- `trange` [list or ndarray]: tunction time span
- `yinit` [list or ndarray]: function initial values
- `params` [list of ndarray]: function parameters

and the following are optional input arguments:

- `method` [str]: Runge-Kutta method, defaults to Runge-Kutta Dormand-Prince of order 4(5) or inputed as `method='rk45'`. See section (3) above.
- `reltol` [float]: relative error tolerance, defaults to $10^{-3}$ or inputed as `reltol=1e-3`.
- `abstol` [float]: absolute error tolerance, defaults to $10^{-6}$ or inputed as `abstol=1e-6`.
- `nord` [int or str]: vector norm for formulas used in the solver (see Reference [7]), defaults to 2-norm or inputed as `nord=2`. Other available norms are: `nord=1`, `nord=-1`, `nord='inf'`, `nord='-inf'`, `nord='None'`, and `l-p` norms (`nord=p` where $p$ is any integer but zero).

The function has the following output:

- `t` [ndarray or float]: time solution that contains different values of time step.
- `y` [ndarray or float]: approximation of order $p$
- `yhat` [ndarray or float]: embedded approximation of order $q$
- `stats` [dict]: statistics (number of total steps, number of failed steps, relative error, and absolute error)

Parameters of equations should be put in a list or NumPy array, like the following system of van der Pol oscillator with scalar parameter $\mu=1.0$,

```
def vdp_func(t, y, p):
    dy = np.zeros((len(y), ))
    dy[0] = y[1]
    dy[1] = p[0]*(1 - y[0]**2) * y[1] - y[0]
    return dy
```

where the list `p` here contains only one parameter $\mu$, hence `p[0]`. To solve and visualize the system of ODEs above using `rkexplicit()` with 7th-order Runge-Kutta method (`method='rk78'`), and `inf`-norm,

```
from odespy import rkexplicit
import matplotlib.pyplot as plt

trange = [0, 20]
yinit = [2, 0]
params = [1]

ts, ys, yhat, stats = rkexplicit(vdp_func, trange, yinit, params, method='rk78', nord='inf')

print(stats)

n = ys.shape[1]

for i in range(n):
    plt.plot(ts, ys[:, i], '.')

plt.show()
```

Local truncation errors of the approximations can also be visualized:

```
n = ys.shape[1]

for i in range(n):
    plt.plot(ts, abs(ys[:,i]-yshat[:,i]))

plt.show()
```

### `abm4()` function

The required input arguments for `abm4()` are as follows:

- function
- `trange` [list or ndarray]: tunction time span
- `yinit` [list or ndarray]: function initial values
- `params` [list of ndarray]: function parameters
- `h` [float]: time step

and the following are optional input arguments:

- `nord` [int or str]: vector norm, used to calculate the difference between corrector and predictor for local truncation error (lte), defaults to 2-norm or inputed as `nord=2`. Other available norms are: `nord=1`, `nord=-1`, `nord='inf'`, `nord='-inf'`, `nord='None'`, and `l-p` norms (`nord=p` where $p$ is any integer but zero).
- `k` [int]: number of iterations for $\text{P(EC)}^k$, defaults to `k=4`.

The function has the following output:

- `t` [ndarray or float]: time solution that contains fixed time steps.
- `y` [ndarray or float]: approximation result
- `lte`: [ndarray or float]: differences between corrector and predictor

The predictor-corrector method can be used to solve discontinuous functions (functions with switches or jumps) with little numerical costs. For example, to solve Coulomb's law of friction that has been reformulated in to a system of ODEs:

$$
\dfrac{dy}{dt} = v
$$

$$
\dfrac{dv}{dt} = -0.2v - y + 2 \cos(\pi t) -
\begin{cases}
4 & \quad \text{if $v>0$}\\
-4 & \quad \text{otherwise}
\end{cases}
$$

we write in Python

```
def coulomb_func(t, y, p):
    dy = np.zeros((len(y),))
    if y[1] > 0:
        a = p[2]
    else:
        a = p[3]

    dy[0] = y[1]
    dy[1] = p[0] * y[1] - y[0] + p[1] * np.cos(np.pi * t) - a
    return dy
```

and to solve and visualize both the result and error with 1-norm and 3 iterations,

```
from odespy import abm4
import matplotlib.pyplot as plt

trange = [0, 10]
yinit = [3, 4]
params = [-0.2, 2, 4, -4]
h = 0.001

ts, ys, lte = abm4(coulomb_func, trange, yinit, params, h, nord=1, k=3)

fig, axs = plt.subplots(1, 2, figsize=(8, 3))
axs[0].plot(ts, ys)
axs[1].plot(ts, lte)

plt.show()
```

## (5) Contributing

Interested in contributing? Please contact me directly.

## References

[1] https://doi.org/10.1016/0771-050X(80)90013-3 <br>
[2] https://doi.org/10.1016/0771-050X(81)90010-3 <br>
[3] https://ntrs.nasa.gov/api/citations/19690021375/downloads/19690021375.pdf <br>
[4] https://ntrs.nasa.gov/api/citations/19680027281/downloads/19680027281.pdf <br>
[5] https://doi.org/10.1145/79505.79507 <br>
[6] https://www.sfu.ca/~jverner/RKV65.IIIXb.Robust.00010102836.081204.RATOnWeb <br>
[7] https://doi.org/10.1007/978-3-642-05221-7
