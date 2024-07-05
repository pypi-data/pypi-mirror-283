import copy
import numpy as np

np.seterr(divide="ignore", invalid="ignore")
from step_size import StepSize
from initialization import ArrayInitialization
from estimation import Variables, Approximation
from norms import norm
from predictor_corrector import approxRK41Class

###-------------------------###


def calculateStepSize(rejectStep, hh, hmin, err, p):
    opt = np.sign(1.0 / err) * (np.abs(1.0 / err)) ** (1 / (p + 1))
    if rejectStep == True:
        r = min(0.5, max(0.1, 0.8 * opt))
        hh = max(hmin, hh * r)
    return hh


def rkexplicit(
    func, t_range, yinit, params, method="Default", abstol=1e-6, reltol=1e-3, nord=2
):
    """
    Main function for explicit/non-stiff ODEs.

    Args:
        func (None): Function that consists of ODEs to solve
        t_range (ndarray): Time range
        yinit (ndarray): Initial conditions
        params (list): Parameters
        method (str, optional): Runge-Kutta method of choice. Defaults to "rk45" or "Default".
        abstol (float, optional): Absolute error tolerance. Defaults to 1e-6.
        reltol (float, optional): Relative error tolerance. Defaults to 1e-3.
        nord (int/str, optional): Norm order. Defaults to 2-norm.

    Raises:
        Exception: _description_
        ValueError: _description_

    Returns:
        tuple: _description_
    """
    method = method.lower()

    if reltol == 0.0:
        raise Exception("RelTol cannot be zero")

    atol = abs(abstol)
    rtol = abs(reltol)
    threshold = atol / rtol

    init = ArrayInitialization()

    yinit = init.array_check(yinit)
    t_range = init.array_check(t_range)
    params = init.array_check(params)

    if t_range.shape[0] != 2:
        raise ValueError(
            "Time span must containt only two values: [time_start, time_end]"
        )

    t = t_range[0]
    n = yinit.shape[0]

    tsol, ysol, yhatsol = init.gen_init_arrays(t, yinit)

    # -- Get Butcher tableau coefficients --#
    vals = Variables(method)
    vals.coefficients()
    b = vals.bt
    bhat = vals.bhat
    p = vals.p

    ya = yinit.copy()
    tspan = t_range[0]

    # For direction of time span
    tdir = np.sign(t_range[-1] - t_range[0])

    # -- Generate initial step size (page 169: Starting Step Size) --#
    ss = StepSize(func, t, yinit, params, method, nord)
    hh, hmax = ss.init_step_v3(t_range, threshold, rtol, p)

    nsteps = 1
    nfailed = 0
    rejectStep = False
    done = False

    while done == False:
        # Step size is bounded by lower (hmin) and upper (hmax)
        hmin = 16.0 * np.spacing(t)
        hh = min(hmax, max(hmin, hh))
        h = tdir * hh

        # Check if it's the last step size and reduce h if the length exeeds the grid (time range)
        if 1.1 * hh >= abs(t_range[-1] - t):
            h = t_range[-1] - t
            hh = abs(h)
            done = True

        noFailed = True  # no failed attempts

        # Loop for moving 1 step forward
        while True:

            yt1 = Approximation(func, t, ya, params, h, method)
            t1, y = yt1.y_approx(b)

            yt2 = Approximation(func, t, ya, params, h, method)
            _, yhat = yt2.y_approx(bhat)

            # Estimate error
            ydiff = y - yhat
            sc = atol + rtol * max(norm(ya, nord), norm(y, nord))  # Eq. (4.10)
            err = ((1 / n) * (norm(ydiff, nord) / sc) ** 2) ** (
                1 / 2
            )  # norm following Eq (4.11)

            ###--------------------------###

            if err > rtol:
                nfailed += 1

                if hh < hmin:
                    msg = f"Unable to meet integration tolerances: hmin ({hmin}) exceeded!"
                    raise ValueError(msg)

                if noFailed == True:
                    noFailed = False

                rejectStep = True

                hh = calculateStepSize(rejectStep, hh, hmin, err, p)
                h = tdir * hh
                continue
            else:
                break

            ###--------------------------###

        # If there were no failures in computing a new step:
        # The safety factor 1.25 is to increase the probability that the next sep will be accepted.
        # The constants 5 and 0.2 serve to prevent an abrupt change in the stepsize.
        if noFailed == True and rejectStep == False:
            temp = 1.25 * (err / rtol) ** (1 / (p + 1))
            if temp > 0.2:
                hh = hh / temp
            else:
                hh = 5.0 * hh

        nsteps += 1

        ysol = np.vstack((ysol, y))
        yhatsol = np.vstack((yhatsol, yhat))

        tspan += h
        tsol = np.append(tsol, tspan)

        ya = y
        t = t1
        rejectStep = False

    return (
        tsol,
        ysol,
        yhatsol,
        {
            "total steps": nsteps,
            "failed steps": nfailed,
            "absolute error": atol,
            "relative error": rtol,
        },
    )


###-------------------------###


def abm4(f, t_range, yinit, p, h, nord=2, k=4):

    init = ArrayInitialization()

    yinit = init.array_check(yinit)
    t_range = init.array_check(t_range)
    p = init.array_check(p)

    if t_range.shape[0] != 2:
        raise ValueError(
            "Time span must containt only two values: [time_start, time_end]"
        )

    t0 = t_range[0]

    trk4 = np.array([t0, t0 + h, t0 + 2 * h, t0 + 3 * h])

    y0 = yinit.copy()

    dt = round((t_range[-1] - t_range[0]) / h)

    ts, ys = approxRK41Class(f, trk4, y0, p, h)

    tt = ts.copy()
    tsol = np.empty(0)
    tsol = np.append(tsol, tt)

    yy = copy.deepcopy(ys)
    ysol = copy.deepcopy(ys)

    s = ts.shape[0]
    i = s - 1

    k = int(k)

    if k < 1:
        raise ValueError(
            "In predictor-corrector mode P(EC)^k, the value of k cannot be less than 1!"
        )

    lte = np.array([0.0, 0.0, 0.0, 0.0])

    for i in range(s - 1, dt):

        t00 = tt[i]
        t11 = tt[i - 1]
        t22 = tt[i - 2]
        t33 = tt[i - 3]
        tpp = tt[i] + h

        y00 = yy[i, :]  # y_n+3
        y11 = yy[i - 1, :]  # y_n+2
        y22 = yy[i - 2, :]  # y_n+1
        y33 = yy[i - 3, :]  # y_n

        y0prime = f(t00, y00, p)
        y1prime = f(t11, y11, p)
        y2prime = f(t22, y22, p)
        y3prime = f(t33, y33, p)

        ##-- Predictor (P) --##
        # Compute the predictor, Eq (1.5') pp. 358
        ypredictor = y00 + (h / 24) * (
            55 * y0prime - 59 * y1prime + 37 * y2prime - 9 * y3prime
        )

        ytemp = ypredictor.copy()

        for _ in range(k):

            ##-- Evaluate (E) --##
            # Evaluate the function using the predictor
            fp = f(tpp, ytemp, p)

            ##-- Corrector (C) --#
            # Apply the corrector, Eq. (1.9"), pp. 360
            ycorrector = y00 + (h / 24) * (
                9 * fp + 19 * y0prime - 5 * y1prime + y2prime
            )

            ytemp = ycorrector

        # Calculate the norm of the difference between predictor and corrector
        sigma = norm((ycorrector - ypredictor), nord)

        # Save it in the array of local truncation error
        lte = np.append(lte, sigma)

        ysol = np.vstack((ysol, ycorrector))

        tm = tt[i] + h
        tsol = np.append(tsol, tm)

        tt = tsol

        yy = ysol

    return tsol, ysol, lte
