"""
Available norms:
    1-norm, 
    -1-norm
    2-norm (or spectral norm),  
    Frobenius norm, 
    infinity-norm, 
    -infinity-norm
    lp-norm
"""

import numpy as np


def norm(x, nord):
    if type(nord) == str:
        nord = nord.lower()

    if nord == None:  # Frobenius norm
        if x.ndim == 1:
            return (sum(abs(x) ** 2)) ** (1.0 / 2)
        elif x.ndim == 2:
            y = x.flatten()
            return (sum([i**2 for i in y])) ** (1.0 / 2)

    elif nord == "fro":  # Frobenius norm
        if x.ndim == 1:
            return (sum(abs(x) ** 2)) ** (1.0 / 2)
        elif x.ndim == 2:
            y = x.flatten()
            return (sum([i**2 for i in y])) ** (1.0 / 2)

    elif nord == "inf":
        if x.ndim == 1:
            return max(abs(x))
        elif x.ndim == 2:
            return max([j for j in sum(abs(x.T))])
            # m = x.shape[0]
            # res = np.zeros(m, )
            # for i in range(m):
            #     res[i] = sum(abs(x[i,:]))
            # return max(res)

    elif nord == "-inf":
        if x.ndim == 1:
            return min(abs(x))
        elif x.ndim == 2:
            return min([j for j in sum(abs(x.T))])
            # m = x.shape[0]
            # res = np.zeros(m, )
            # for i in range(m):
            #     res[i] = sum(abs(x[i,:]))
            # return min(res)

    elif nord == 0:
        if x.ndim == 1:
            return sum(x != 0)
        elif x.ndim == 2:
            raise Exception("THere is no 0-norm for matrices")

    elif nord == 1:
        if x.ndim == 1:
            return sum(abs(x))
        elif x.ndim == 2:
            return max([j for j in sum(abs(x))])
            # m = x.shape[1]
            # res = np.zeros(m, )
            # for i in range(m):
            #     res[i] = sum(abs(x[:,i]))
            # return max(res)

    elif nord == -1:
        if x.ndim == 1:
            return min(abs(x))
        elif x.ndim == 2:
            return min([j for j in sum(abs(x))])
            # m = x.shape[1]
            # res = np.zeros(m, )
            # for i in range(m):
            #     res[i] = sum(abs(x[:,i]))
            # return min(res)

    elif nord == 2:  # Spectral norm
        if x.ndim == 1:
            return (sum(abs(x) ** 2)) ** (1.0 / 2)
        elif x.ndim == 2:
            xxt = np.matmul(x.T, x)
            eg, ev = np.linalg.eig(xxt)
            return (max(abs(eg))) ** (1.0 / 2)

    else:
        if x.ndim == 1:
            return (sum(abs(x) ** nord)) ** (1.0 / nord)
        elif x.ndim == 2:
            raise Exception("There is no matrix norm for this order")
