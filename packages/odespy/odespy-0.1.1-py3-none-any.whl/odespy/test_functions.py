import numpy as np


############################################
###---------- Simple Functions ----------###
############################################

def test_func(t, y, p):
    dy = np.zeros((len(y), ))
    dy[0] = p[0] * np.exp(p[1] * t) - p[2] * y[0]
    return dy

def test_params():
    t_range = [0., 2.]
    y_init = [2.]
    params = [4., 0.8, 0.5]
    return t_range, y_init, params


###------------------------------###


def simple_func(t, y, p):
    dy = np.zeros((len(y), ))
    dy[0] = p[0] * np.exp(p[1] * t) - p[2] * y[0]
    return dy

def simple_params():
    t_range = [0., 2.]
    y_init = [2.]
    params = [4., 0.8, 0.5]
    return t_range, y_init, params


#################################################
###---------- Oscillating Functions ----------###
#################################################


def vdp_func(t, y, p):
    dy = np.zeros((len(y), ))
    dy[0] = y[1]
    dy[1] = p[0]*(1 - y[0]**2) * y[1] - y[0]
    return dy

def vdp_params():
    t_range = [0., 20.]
    y_init = [2., 0.]
    params = [1.]
    return t_range, y_init, params


###------------------------------###


def brusselator_func(t, y, p):
    dy = np.zeros((len(y),))
    dy[0] = p[0] + p[1] * y[1] * y[0]**2 - p[2] * y[0]
    dy[1] = p[3] * y[0] - p[4] * y[1] * y[0]**2
    return dy

def brusselator_params():
    t_range = [0, 20]
    y_init = [1.5, 3.]
    params = [1., 1., 4., 3., 1.]
    return t_range, y_init, params


###------------------------------###


def predator_prey(t, y, p):
    dy = np.zeros((len(y),))
    dy[0] = p[0] * y[0] + p[1] * y[0] * y[1] 
    dy[1] = p[2] * y[1] + p[3] * y[0] * y[1] 
    return dy

def predator_prey_params():
    y_init = np.array([2.0, 1.0])
    t_range = np.array([0.0, 20.0])
    params = np.array([1.2, -0.6, -0.8, 0.3])
    return t_range, y_init, params


###------------------------------###


def oscillator_func(t, y, p):
    dy = np.zeros((len(y), ))
    dy[0] = ((p[0] + p[1] * y[0]**2) / (1 + y[0]**2 + p[3]*y[1])) - y[0]
    dy[1] = p[5] * (p[2] * y[0] + p[4] - y[1])
    return dy

def oscillator_params():
    t_range = [1, 100]
    y_init = [1, 1]
    params = [1, 5, 4, 1, 0, 0.1]
    return t_range, y_init, params


################################################
###---------- Functions with Chaos ----------###
################################################


def lorenz_func(t, y, p):
    dy = np.zeros((len(y), ))
    dy[0] = p[0] * (y[1] - y[0])
    dy[1] = y[0] * (p[1] - y[2]) - y[1]
    dy[2] = y[0] * y[1] - p[2] * y[2]
    return dy

def lorenz_params():
    t_range = [0, 10]
    y_init = [0.4, -0.7, 21.]
    params = [10., 28., 8./3.]
    return t_range, y_init, params
    

########################################################
###---------- Functions with Discontinuity ----------###
########################################################

###------------------------------###
# Discontinuous equation
# Book: Solving Ordinary Differential Equations I - Nonstiff Problems (1993)
# Pages: 198, Eqs. (6.28) & (6.27)
def coulomb_func(t, y, p):
    dy = np.zeros((len(y),))
    if y[1] > 0:
        a = 4.
    else:
        a = -4.
        
    dy[0] = p[0] * y[1]
    dy[1] = p[1] * y[1] - p[2] * y[0] + p[3] * np.cos(np.pi * t) - a
    return dy

def coulomb_params():
    t_range = [0, 10.]
    y_init = [3., 4.]
    params = [1., -0.2, 1., 2.]
    return t_range, y_init, params


###------------------------------###

# https://www.engr.mun.ca/~ggeorge/2422/notes/c56ex.html

def discontinuous_func(t, y, p):
    if t >= 2.:
        r = 0.
    elif 0. <= t < 2.:
        r = 12.
        
    dy = np.zeros((len(y), ))
    dy[0] = y[1]
    dy[1] = r - p[0] * y[1] - p[1] * y[0]
    return dy


def discontinuous_params():
    t_range = [0., 5.]
    y_init = [0., 0.]
    params = [5., 6.]
    return t_range, y_init, params

###------------------------------###

def exp_disc_func(t, y, p):
    if t >= 1.:
        r = 0.
    elif 0. <= t < 1.:
        r = np.exp(-t)
        
    dy = np.zeros((len(y), ))
    dy[0] = y[1]
    dy[1] = r - p[0] * y[1] - p[1] * y[0]
    return dy

def exp_disc_params():
    t_range = [0., 5.]
    y_init = [0., 0.]
    params = [2., 2.]
    return t_range, y_init, params

###------------------------------###



