import numpy as np
from .norms import norm


class StepSize:
    def __init__(self, f, t0, y0, params, method, nord):
        self.f = f
        self.t0 = t0
        self.y0 = y0
        self.params = params
        self.method = method.lower()
        self.nord = nord
        if (
            self.method == "rkf45"
            or self.method == "rkck"
            or self.method == "rk45"
            or self.method == "default"
        ):
            self.p = 4
        elif self.method == "rkv":
            self.p = 5
        elif self.method == "rkf78" or self.method == "rk78":
            self.p = 7

    # def deriv_0(self):
    #     return self.norm(self.y0)

    # def deriv_1(self):
    #     return self.norm(self.f(self.t0, self.y0, self.params))

    def guess_h0(self, a, b):
        if a < 1e-5 or b < 1e-5:
            return 1e-6
        else:
            return 0.01 * (a / b)

    def explicit_Euler(self, x0):
        return self.y0 + x0 * self.f(self.t0, self.y0, self.params)

    def deriv_2(self, x0, k1):
        num = self.f(self.t0 + x0, k1, self.params) - self.f(
            self.t0, self.y0, self.params
        )
        return norm(num, self.nord) / x0

    def guess_h1(self, u, v, x0):
        if max(u, v) <= 1e-15:
            return max(1e-6, x0 * 1e-3)
        else:
            ph1 = 0.01 / max(u, v)
            return ph1 ** (1 / (self.p + 1))

    def init_step_v1(self):
        # d0 = self.deriv_0()
        # d1 = self.deriv_1()

        d0 = norm(self.y0, self.nord)
        d1 = norm(self.f(self.t0, self.y0, self.params), self.nord)

        h0 = self.guess_h0(d0, d1)

        y1 = self.explicit_Euler(h0)
        d2 = self.deriv_2(h0, y1)
        h1 = self.guess_h1(d1, d2, h0)

        return min(100 * h0, h1)

    def init_step_v2(self, abstol, reltol):
        """
        Initial step size based on the following book:
        Title: Solving Ordinary Differential Equations I: Nonstiff Problems
        Chapter: II.4 Practical Error Estimation and Step Size Selection
        Section: Starting Step Size (pp. 169)

        Args:
            abstol (float): absolute tolerance
            reltol (float): relative tolerance

        Returns:
            float: initial step size
        """
        n = len(self.y0)

        # -- Step (a) --#
        sc = abs(abstol) + max(abs(self.y0)) * abs(reltol)
        d0 = ((1 / n) * sum(((self.y0) / sc) ** 2)) ** (1 / 2)
        d1 = ((1 / n) * sum(((self.f(self.t0, self.y0, self.params)) / sc) ** 2)) ** (
            1 / 2
        )

        # -- Step (b): Get a first guess of h --#
        h0 = self.guess_h0(d0, d1)

        # -- Step (c): Perform one explicit Euler step --#
        y1 = self.explicit_Euler(h0)

        # -- Step (d): Estimate the 2nd derivative --#
        yd1 = self.f(self.t0 + h0, y1, self.params)
        yd2 = self.f(self.t0, self.y0, self.params)
        d2 = ((1 / n) * sum(((yd1 - yd2) / sc) ** 2)) ** (1 / 2) / h0

        # -- Step (e): Compute a step size h1 --#
        h1 = self.guess_h1(d1, d2, h0)

        # -- Step (f): Propose a starting step-size --#
        return min(100 * h0, h1)

    # Matlab ODE Suite
    def init_step_v3(self, t_range, threshold, rtol, p):
        dd0 = norm(self.y0, self.nord)  # = d0
        hmax = 1 / 10 * abs(t_range[-1] - t_range[0])
        htspan = abs(t_range[-1] - t_range[0])

        f0 = self.f(self.t0, self.y0, self.params)
        nf0 = norm(f0, self.nord)

        hmin = 16 * np.spacing(self.t0)
        hh = min(hmax, htspan)
        rh = (nf0 / max(dd0, threshold)) / (0.8 * rtol ** (1 / (p + 1)))

        if hh * rh > 1:
            hh = 1 / rh

        hh = max(hh, hmin)
        return hh, hmax
