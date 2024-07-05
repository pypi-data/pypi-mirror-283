# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from odespy import rkexplicit, abm4
import test_functions as tf
from test_functions import lorenz_func


# The default of relative error tolerance is 1e-3 and absolute error tolerance is 1e-6.
# methods: default, rk45, rk78, rkf45, rkf78, rkv, rkck
# oscillating functions: vdp_func, brusselator_func, predator_prey, oscillator_func
# functions with discontinuity: coulomb_func, discontinuous_func, exp_disc_func
# functions with chaos: lorenz_func

f = lorenz_func

t_range, yinit, params = tf.lorenz_params()


ts, ys, yshat, stats = rkexplicit(
    f, t_range, yinit, params, method="rk78", reltol=1e-7, abstol=1e-8, nord="inf"
)

print(stats)

n = ys.shape[1]

for i in range(n):
    plt.plot(ts, ys[:, i])
    # plt.plot(ts, abs(ys[:,i]-yshat[:,i])) # error

plt.show()

# ------------#

# h = 0.001
# tr, yr, err = abm4(f, t_range, yinit, params, h, nord=2, k=2)

# fig, axs = plt.subplots(1, 2, figsize=(8, 3))
# axs[0].plot(tr, yr)
# axs[1].plot(tr, err)
# plt.show()
