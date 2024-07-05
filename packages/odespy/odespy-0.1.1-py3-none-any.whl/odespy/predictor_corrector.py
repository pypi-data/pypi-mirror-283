import numpy as np
from .tableaux import RK41Explicit


class Variables:
    def __init__(self):
        self.coefficients()

    def coefficients(self):
        self.c = RK41Explicit().coeff_c()
        self.a = RK41Explicit().coeff_matA()
        self.b = RK41Explicit().coeff_b()
        self.stages = self.c.shape[0]


class Approximation(Variables):
    def __init__(self, f, t0, y_init, params, h, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.y = y_init.copy()
        self.f = f
        self.t = t0
        self.params = params
        self.h = h
        self.n_odes = len(y_init)
        self.slopes()

    def slopes(self):
        self.k = np.zeros((self.stages, self.n_odes))
        self.k[0, :] = self.f(self.t, self.y, self.params)
        for i in range(1, self.stages):
            matA = 0.0
            for j in range(i):
                matA += self.a[i, j] * self.h * self.k[j, :]
            self.k[i, :] = self.f(
                self.t + self.c[i] * self.h, self.y + matA, self.params
            )

        return self.k

    def y_approx(self):
        tmp = 0.0
        for i in range(self.stages):
            tmp += self.b[i] * self.k[i, :]

        self.y += self.h * tmp
        self.t += self.h
        return self.t, self.y


def approxRK41Class(f, t_range, y, params, h):
    ya = y.copy()

    t = t_range[0]

    ys = np.empty(0)
    ys = np.append(ys, ya)

    ts = np.empty(0)
    ts = np.append(ts, t)

    while t < t_range[-1]:

        yt = Approximation(f, t, ya, params, h)

        tr, yr = yt.y_approx()

        ya = yr
        t += h

        ts = np.append(ts, t)
        ys = np.vstack((ys, yr))

    return ts, ys
