import numpy as np
import copy
from tableaux import (
    CashKarp,
    DormandPrince45,
    DormandPrince78,
    Verner56,
    Fehlberg45,
    Fehlberg78,
)


###------------------------------###


class Variables:
    def __init__(self, method):
        self.method = method
        self.coefficients()

    def coefficients(self):
        if self.method == "rkck":
            self.c = CashKarp().coeff_c()
            self.a = CashKarp().coeff_matA()
            self.bt = CashKarp().coeff_bt()
            self.bhat = CashKarp().coeff_bhat()
            self.p = CashKarp().order
        elif self.method == "rkv":
            self.c = Verner56().coeff_c()
            self.a = Verner56().coeff_matA()
            self.bt = Verner56().coeff_bt()
            self.bhat = Verner56().coeff_bhat()
            self.p = Verner56().order
        elif self.method == "default" or self.method == "rk45":
            self.c = DormandPrince45().coeff_c()
            self.a = DormandPrince45().coeff_matA()
            self.bt = DormandPrince45().coeff_bt()
            self.bhat = DormandPrince45().coeff_bhat()
            self.p = DormandPrince45().order
        elif self.method == "rk78":
            self.c = DormandPrince78().coeff_c()
            self.a = DormandPrince78().coeff_matA()
            self.bt = DormandPrince78().coeff_bt()
            self.bhat = DormandPrince78().coeff_bhat()
            self.p = DormandPrince78().order
        elif self.method == "rkf45":
            self.c = Fehlberg45().coeff_c()
            self.a = Fehlberg45().coeff_matA()
            self.bt = Fehlberg45().coeff_bt()
            self.bhat = Fehlberg45().coeff_bhat()
            self.p = Fehlberg45().order
        elif self.method == "rkf78":
            self.c = Fehlberg78().coeff_c()
            self.a = Fehlberg78().coeff_matA()
            self.bt = Fehlberg78().coeff_bt()
            self.bhat = Fehlberg78().coeff_bhat()
            self.p = Fehlberg78().order
        else:
            raise ValueError(
                "Method is unknown. Available methods are: 'rkck', 'rkv','rkf45', 'rkf78', 'rk78', 'rk45' (or 'Default')."
            )
        self.stages = self.c.shape[0]


class Approximation(Variables):
    def __init__(self, f, t0, y_init, params, h, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.y = copy.deepcopy(y_init)
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

    def y_approx(self, weights):
        tmp = 0.0
        for i in range(self.stages):
            tmp += weights[i] * self.k[i, :]

        self.y += self.h * tmp
        self.t += self.h
        return self.t, self.y

