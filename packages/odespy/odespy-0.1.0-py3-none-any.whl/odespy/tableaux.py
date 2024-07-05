import numpy as np


class CashKarp:
    """
    Embedded Runge-Kutta

    Coefficients in this Butcher tableau were developed by Cash and Karp (1990).


    """

    def __init__(self):
        self.a = np.zeros((6, 6), dtype=float)
        self.c = np.zeros((6,), dtype=float)
        self.bt = np.zeros((6,), dtype=float)
        self.bhat = np.zeros((6,), dtype=float)
        self.order = 4

    def coeff_matA(self):
        self.a[1, 0] = 1 / 5
        self.a[2, 0] = 3 / 40
        self.a[2, 1] = 9 / 40
        self.a[3, 0] = 3 / 10
        self.a[3, 1] = -9 / 10
        self.a[3, 2] = 6 / 5
        self.a[4, 0] = -11 / 54
        self.a[4, 1] = 5 / 2
        self.a[4, 2] = -70 / 27
        self.a[4, 3] = 35 / 27
        self.a[5, 0] = 1631 / 55296
        self.a[5, 1] = 175 / 512
        self.a[5, 2] = 575 / 13824
        self.a[5, 3] = 44275 / 110592
        self.a[5, 4] = 253 / 4096
        return self.a

    def coeff_c(self):
        self.c[1] = 1 / 5
        self.c[2] = 3 / 10
        self.c[3] = 3 / 5
        self.c[4] = 1.0
        self.c[5] = 7 / 8
        return self.c

    # -- 4th order weights --#
    def coeff_bt(self):
        self.bt[0] = 37 / 378
        self.bt[1] = 0.0
        self.bt[2] = 250 / 621
        self.bt[3] = 125 / 594
        self.bt[4] = 0.0
        self.bt[5] = 512 / 1771
        return self.bt

    # -- 5th order weights --#
    def coeff_bhat(self):
        self.bhat[0] = 2825 / 27648
        self.bhat[1] = 0.0
        self.bhat[2] = 18575 / 48384
        self.bhat[3] = 13525 / 55296
        self.bhat[4] = 277 / 14336
        self.bhat[5] = 1 / 4
        return self.bhat


class DormandPrince45:
    """
    Coefficients in this Butcher tableau were developed by Dormand and Prince in:

    Title: A Family of Runge-Kutta Formulae
    Author(s): J.R. Dormand and P.J. Prince
    Journal of Computational and Applied Mathematics, Vol 6, No 1, 1980

    RK(4)5, where p = 4 and q = 5

    Book: Numerical Methods for Ordinary Differential Equations (2016)
    Author(s): Butcher
    Chapter: 33 Runge-Kutta Methods with Error Estimate
    Sub-chapter: 336 The Methods of Dormand and Prince
    Pages: 223 - 226

    FSAL = first same as last
    FSAL has the property that vector bT, corresponding to the output approximation,
    has its last component zero and is identical to the last row of A.

    """

    def __init__(self):
        self.a = np.zeros((7, 7), dtype=float)
        self.c = np.zeros((7,), dtype=float)
        self.bt = np.zeros((7,), dtype=float)
        self.bhat = np.zeros((7,), dtype=float)
        self.order = 4

    def coeff_matA(self):
        self.a[1, 0] = 1 / 5

        self.a[2, 0] = 3 / 40
        self.a[2, 1] = 9 / 40

        self.a[3, 0] = 44 / 45
        self.a[3, 1] = -56 / 15
        self.a[3, 2] = 32 / 9

        self.a[4, 0] = 19372 / 6561
        self.a[4, 1] = -25360 / 2187
        self.a[4, 2] = 64448 / 6561
        self.a[4, 3] = -212 / 729

        self.a[5, 0] = 9017 / 3168
        self.a[5, 1] = -355 / 33
        self.a[5, 2] = 46732 / 5247
        self.a[5, 3] = 49 / 176
        self.a[5, 4] = -5103 / 18656

        self.a[6, 0] = 35 / 384
        self.a[6, 1] = 0.0
        self.a[6, 2] = 500 / 1113
        self.a[6, 3] = 125 / 192
        self.a[6, 4] = -2187 / 6784
        self.a[6, 5] = 11 / 84

        return self.a

    def coeff_c(self):
        self.c[1] = 1 / 5
        self.c[2] = 3 / 10
        self.c[3] = 4 / 5
        self.c[4] = 8 / 9
        self.c[5] = 1.0
        self.c[6] = 1.0
        return self.c

    # -- 4th order weights --#
    def coeff_bt(self):
        self.bt[0] = 35 / 384
        self.bt[1] = 0.0
        self.bt[2] = 500 / 1113
        self.bt[3] = 125 / 192
        self.bt[4] = -2187 / 6784
        self.bt[5] = 11 / 84
        self.bt[6] = 0.0
        return self.bt

    # -- 5th order weights --#
    def coeff_bhat(self):
        self.bhat[0] = 5179 / 57600
        self.bhat[1] = 0.0
        self.bhat[2] = 7571 / 16695
        self.bhat[3] = 393 / 640
        self.bhat[4] = -92097 / 339200
        self.bhat[5] = 187 / 2100
        self.bhat[6] = 1 / 40
        return self.bhat


class DormandPrince78:
    def __init__(self):
        self.a = np.zeros((13, 13), dtype=float)
        self.c = np.zeros((13,), dtype=float)
        self.bt = np.zeros((13,), dtype=float)
        self.bhat = np.zeros((13,), dtype=float)
        self.order = 7

    def coeff_matA(self):
        self.a[1, 0] = 1 / 18

        self.a[2, 0] = 1 / 48
        self.a[2, 1] = 1 / 16

        self.a[3, 0] = 1 / 32
        self.a[3, 2] = 3 / 32

        self.a[4, 0] = 5 / 16
        self.a[4, 2] = -75 / 64
        self.a[4, 3] = 75 / 64

        self.a[5, 0] = 3 / 80
        self.a[5, 3] = 3 / 16
        self.a[5, 4] = 3 / 20

        self.a[6, 0] = 29443841 / 614563906
        self.a[6, 3] = 77736538 / 692538347
        self.a[6, 4] = -28693883 / 1125000000
        self.a[6, 5] = 23124283 / 1800000000

        self.a[7, 0] = 16016141 / 946692911
        self.a[7, 3] = 61564180 / 158732637
        self.a[7, 4] = 22789713 / 633445777
        self.a[7, 5] = 545815736 / 2771057229
        self.a[7, 6] = -180193667 / 1043307555

        self.a[8, 0] = 39632708 / 573591083
        self.a[8, 3] = -433636366 / 683701615
        self.a[8, 4] = -421739975 / 2616292301
        self.a[8, 5] = 100302831 / 723423059
        self.a[8, 6] = 790204164 / 839813087
        self.a[8, 7] = 800635310 / 3783071287

        self.a[9, 0] = 246121993 / 1340847787
        self.a[9, 3] = -37695042795 / 15268766246
        self.a[9, 4] = -309121744 / 1061227803
        self.a[9, 5] = -12992083 / 490766935
        self.a[9, 6] = 6005943493 / 2108947869
        self.a[9, 7] = 393006217 / 1396673457
        self.a[9, 8] = 123872331 / 1001029789

        self.a[10, 0] = -1028468189 / 846180014
        self.a[10, 3] = 8478235783 / 508512852
        self.a[10, 4] = 1311729495 / 1432422823
        self.a[10, 5] = -10304129995 / 1701304382
        self.a[10, 6] = -48777925059 / 3047939560
        self.a[10, 7] = 15336726248 / 1032824649
        self.a[10, 8] = -45442868181 / 3398467696
        self.a[10, 9] = 3065993473 / 597172653

        self.a[11, 0] = 185892177 / 718116043
        self.a[11, 3] = -3185094517 / 667107341
        self.a[11, 4] = -477755414 / 1098053517
        self.a[11, 5] = -703635378 / 230739211
        self.a[11, 6] = 5731566787 / 1027545527
        self.a[11, 7] = 5232866602 / 850066563
        self.a[11, 8] = -4093664535 / 808688257
        self.a[11, 9] = 3962137247 / 1805957418
        self.a[11, 10] = 65686358 / 487910083

        self.a[12, 0] = 403863854 / 491063109
        self.a[12, 3] = -5068492393 / 434740067
        self.a[12, 4] = -411421997 / 543043805
        self.a[12, 5] = 652783627 / 914296604
        self.a[12, 6] = 11173962825 / 925320556
        self.a[12, 7] = -13158990841 / 6184727034
        self.a[12, 8] = 3936647629 / 1978049680
        self.a[12, 9] = -160528059 / 685178525
        self.a[12, 10] = 248638103 / 1413531060

        return self.a

    def coeff_c(self):
        self.c[1] = 1 / 18
        self.c[2] = 1 / 12
        self.c[3] = 1 / 8
        self.c[4] = 5 / 16
        self.c[5] = 3 / 8
        self.c[6] = 59 / 400
        self.c[7] = 93 / 200
        self.c[8] = 5490023248 / 9719169821
        self.c[9] = 13 / 20
        self.c[10] = 1201146811 / 1299019798
        self.c[11] = 1.0
        self.c[12] = 1.0
        return self.c

    # -- 7th order weights --#
    def coeff_bt(self):
        self.bt[0] = 13451932 / 455176623
        self.bt[5] = -808719846 / 976000145
        self.bt[6] = 1757004468 / 5645159321
        self.bt[7] = 656045339 / 265891186
        self.bt[8] = -3867574721 / 1518517206
        self.bt[9] = 465885868 / 322736535
        self.bt[10] = 53011238 / 667516719
        self.bt[11] = 2 / 45
        return self.bt

    # -- 8th order weights --#
    def coeff_bhat(self):
        self.bhat[0] = 14005451 / 335480064
        self.bhat[5] = -59238493 / 1068277825
        self.bhat[6] = 181606767 / 758867731
        self.bhat[7] = 561292985 / 797845732
        self.bhat[8] = -1041891430 / 1371343529
        self.bhat[9] = 760417239 / 1151165299
        self.bhat[10] = 118820643 / 751138087
        self.bhat[11] = -528747749 / 2220607170
        self.bhat[12] = 1 / 4
        return self.bhat


class Fehlberg45:
    """
    https://ntrs.nasa.gov/citations/19690021375
    Table III: Coefficients for RK4(5), Formula 2
    Page(s): 28
    """

    def __init__(self):
        self.a = np.zeros((6, 6), dtype=float)
        self.c = np.zeros((6,), dtype=float)
        self.bt = np.zeros((6,), dtype=float)
        self.bhat = np.zeros((6,), dtype=float)
        self.order = 4

    def coeff_matA(self):
        self.a[1, 0] = 1 / 4

        self.a[2, 0] = 3 / 32
        self.a[2, 1] = 9 / 32

        self.a[3, 0] = 1932 / 2197
        self.a[3, 1] = -7200 / 2197
        self.a[3, 2] = 7296 / 2197

        self.a[4, 0] = 439 / 216
        self.a[4, 1] = -8.0
        self.a[4, 2] = 3680 / 513
        self.a[4, 3] = -845 / 4104

        self.a[5, 0] = -8 / 27
        self.a[5, 1] = 2.0
        self.a[5, 2] = -3544 / 2565
        self.a[5, 3] = 1859 / 4104
        self.a[5, 4] = -11 / 40

        return self.a

    def coeff_c(self):
        self.c[1] = 1 / 4
        self.c[2] = 3 / 8
        self.c[3] = 12 / 13
        self.c[4] = 1.0
        self.c[5] = 1 / 2
        return self.c

    def coeff_bt(self):
        self.bt[0] = 16 / 135
        self.bt[1] = 0.0
        self.bt[2] = 6656 / 12825
        self.bt[3] = 28561 / 56430
        self.bt[4] = -9 / 50
        self.bt[5] = 2 / 55
        return self.bt

    def coeff_bhat(self):
        self.bhat[0] = 25 / 216
        self.bhat[1] = 0.0
        self.bhat[2] = 1408 / 2565
        self.bhat[3] = 2197 / 4104
        self.bhat[4] = -1 / 5
        self.bhat[5] = 0.0
        return self.bhat


class Fehlberg67:
    def __init__(self):
        self.a = np.zeros((10, 10), dtype=float)
        self.c = np.zeros((10,), dtype=float)
        self.bt = np.zeros((10,), dtype=float)
        self.bhat = np.zeros((10,), dtype=float)
        self.order = 6

    def coeff_matA(self):
        self.a[1, 0] = 2 / 33

        self.a[2, 0] = 0.0
        self.a[2, 1] = 4 / 33

        self.a[3, 0] = 1 / 22
        self.a[3, 1] = 0.0
        self.a[3, 2] = 3 / 22

        self.a[4, 0] = 43 / 64
        self.a[4, 1] = 0.0
        self.a[4, 2] = -165 / 64
        self.a[4, 3] = 77 / 32

        self.a[5, 0] = -2383 / 486
        self.a[5, 1] = 0.0
        self.a[5, 2] = 1067 / 54
        self.a[5, 3] = -26312 / 1701
        self.a[5, 4] = 2176 / 1701

        self.a[6, 0] = 10077 / 4802
        self.a[6, 1] = 0.0
        self.a[6, 2] = -5643 / 686
        self.a[6, 3] = 116259 / 16807
        self.a[6, 4] = -6240 / 16807
        self.a[6, 5] = 1053 / 2401

        self.a[7, 0] = -733 / 176
        self.a[7, 1] = 0.0
        self.a[7, 2] = 141 / 8
        self.a[7, 3] = -335763 / 23296
        self.a[7, 4] = 216 / 77
        self.a[7, 5] = -4617 / 2816
        self.a[7, 6] = 7203 / 9152

        self.a[8, 0] = 15 / 352
        self.a[8, 1] = 0.0
        self.a[8, 2] = 0.0
        self.a[8, 3] = -5445 / 46592
        self.a[8, 4] = 18 / 77
        self.a[8, 5] = -1215 / 5632
        self.a[8, 6] = 1029 / 18304
        self.a[8, 7] = 0.0

        self.a[9, 0] = -1833 / 352
        self.a[9, 1] = 0.0
        self.a[9, 2] = 141 / 8
        self.a[9, 3] = -51237 / 3584
        self.a[9, 4] = 18 / 7
        self.a[9, 5] = -729 / 512
        self.a[9, 6] = 1029 / 1408
        self.a[9, 7] = 0.0
        self.a[9, 8] = 1.0

        return self.a

    def coeff_c(self):
        self.c[1] = 2 / 33
        self.c[2] = 4 / 33
        self.c[3] = 2 / 11
        self.c[4] = 1 / 2
        self.c[5] = 2 / 3
        self.c[6] = 6 / 7
        self.c[7] = 1.0
        self.c[8] = 0.0
        self.c[9] = 1.0

        return self.c

    def coeff_bt(self):
        self.bt[0] = 77 / 1440
        self.bt[1] = 0.0
        self.bt[2] = 0.0
        self.bt[3] = 1771561 / 6289920
        self.bt[4] = 32 / 105
        self.bt[5] = 243 / 2560
        self.bt[6] = 16807 / 74880
        self.bt[7] = 11 / 270
        self.bt[8] = 0.0
        self.bt[9] = 0.0

        return self.bt

    def coeff_bhat(self):
        self.bhat[0] = 11 / 864
        self.bhat[1] = 0.0
        self.bhat[2] = 0.0
        self.bhat[3] = 1771561 / 6289920
        self.bhat[4] = 32 / 105
        self.bhat[5] = 243 / 2560
        self.bhat[6] = 16807 / 74880
        self.bhat[7] = 0.0
        self.bhat[8] = 11 / 270
        self.bhat[9] = 11 / 270

        return self.bhat


class Fehlberg78:
    def __init__(self):
        self.a = np.zeros((13, 13), dtype=float)
        self.c = np.zeros((13,), dtype=float)
        self.bt = np.zeros((13,), dtype=float)
        self.bhat = np.zeros((13,), dtype=float)
        self.order = 7

    def coeff_matA(self):
        self.a[1, 0] = 2 / 27

        self.a[2, 0] = 1 / 36
        self.a[2, 1] = 1 / 12

        self.a[3, 0] = 1 / 24
        self.a[3, 1] = 0.0
        self.a[3, 2] = 1 / 8

        self.a[4, 0] = 5 / 12
        self.a[4, 1] = 0.0
        self.a[4, 2] = -25 / 16
        self.a[4, 3] = 25 / 16

        self.a[5, 0] = 1 / 20
        self.a[5, 1] = 0.0
        self.a[5, 2] = 0.0
        self.a[5, 3] = 1 / 4
        self.a[5, 4] = 1 / 5

        self.a[6, 0] = -25 / 108
        self.a[6, 1] = 0.0
        self.a[6, 2] = 0.0
        self.a[6, 3] = 125 / 108
        self.a[6, 4] = -65 / 27
        self.a[6, 5] = 125 / 54

        self.a[7, 0] = 31 / 300
        self.a[7, 1] = 0.0
        self.a[7, 2] = 0.0
        self.a[7, 3] = 0.0
        self.a[7, 4] = 61 / 225
        self.a[7, 5] = -2 / 9
        self.a[7, 6] = 13 / 900

        self.a[8, 0] = 2.0
        self.a[8, 1] = 0.0
        self.a[8, 2] = 0.0
        self.a[8, 3] = -53 / 6
        self.a[8, 4] = 704 / 45
        self.a[8, 5] = -107 / 9
        self.a[8, 6] = 67 / 90
        self.a[8, 7] = 3.0

        self.a[9, 0] = -91 / 108
        self.a[9, 1] = 0.0
        self.a[9, 2] = 0.0
        self.a[9, 3] = 23 / 108
        self.a[9, 4] = -976 / 135
        self.a[9, 5] = 311 / 54
        self.a[9, 6] = -19 / 60
        self.a[9, 7] = 17 / 6
        self.a[9, 8] = -1 / 12

        self.a[10, 0] = 2383 / 4100
        self.a[10, 1] = 0.0
        self.a[10, 2] = 0.0
        self.a[10, 3] = -341 / 164
        self.a[10, 4] = 4496 / 1025
        self.a[10, 5] = -301 / 82
        self.a[10, 6] = 2133 / 4100
        self.a[10, 7] = 45 / 82
        self.a[10, 8] = 45 / 164
        self.a[10, 9] = 18 / 41

        self.a[11, 0] = 3 / 205
        self.a[11, 1] = 0.0
        self.a[11, 2] = 0.0
        self.a[11, 3] = 0.0
        self.a[11, 4] = 0.0
        self.a[11, 5] = -6 / 41
        self.a[11, 6] = -3 / 205
        self.a[11, 7] = -3 / 41
        self.a[11, 8] = 3 / 41
        self.a[11, 9] = 6 / 41
        self.a[11, 10] = 0.0

        self.a[12, 0] = -1777 / 4100
        self.a[12, 1] = 0.0
        self.a[12, 2] = 0.0
        self.a[12, 3] = -341 / 164
        self.a[12, 4] = 4496 / 1025
        self.a[12, 5] = -289 / 82
        self.a[12, 6] = 2193 / 4100
        self.a[12, 7] = 51 / 82
        self.a[12, 8] = 33 / 164
        self.a[12, 9] = 12 / 41
        self.a[12, 10] = 0.0
        self.a[12, 11] = 1.0

        return self.a

    def coeff_c(self):
        self.c[1] = 2 / 27
        self.c[2] = 1 / 9
        self.c[3] = 1 / 6
        self.c[4] = 5 / 12
        self.c[5] = 1 / 2
        self.c[6] = 5 / 6
        self.c[7] = 1 / 6
        self.c[8] = 2 / 3
        self.c[9] = 1 / 3
        self.c[10] = 1.0
        self.c[11] = 0.0
        self.c[12] = 1.0
        return self.c

    def coeff_bt(self):
        self.bt[0] = 41 / 840
        self.bt[1] = 0.0
        self.bt[2] = 0.0
        self.bt[3] = 0.0
        self.bt[4] = 0.0
        self.bt[5] = 34 / 105
        self.bt[6] = 9 / 35
        self.bt[7] = 9 / 35
        self.bt[8] = 9 / 280
        self.bt[9] = 9 / 280
        self.bt[10] = 41 / 840
        self.bt[11] = 0.0
        self.bt[12] = 0.0
        return self.bt

    def coeff_bhat(self):
        self.bhat[0] = 0.0
        self.bhat[1] = 0.0
        self.bhat[2] = 0.0
        self.bhat[3] = 0.0
        self.bhat[4] = 0.0
        self.bhat[5] = 34 / 105
        self.bhat[6] = 9 / 35
        self.bhat[7] = 9 / 35
        self.bhat[8] = 9 / 280
        self.bhat[9] = 9 / 280
        self.bhat[10] = 0.0
        self.bhat[11] = 41 / 840
        self.bhat[12] = 41 / 840
        return self.bhat


class Verner56:
    """
    Verner's method of order 6(5)9b
    A robust RK 56 Pair

    Reference(s):
    Link: https://www.sfu.ca/~jverner/RKV65.IIIXb.Robust.00010102836.081204.RATOnWeb
    """

    def __init__(self):
        self.a = np.zeros((9, 9), dtype=float)
        self.c = np.zeros((9,), dtype=float)
        self.bt = np.zeros((9,), dtype=float)
        self.bhat = np.zeros((9,), dtype=float)
        self.order = 5

    def coeff_matA(self):
        self.a[1, 0] = 9 / 50

        self.a[2, 0] = 29 / 324
        self.a[2, 1] = 25 / 324

        self.a[3, 0] = 1 / 16
        self.a[3, 1] = 0.0
        self.a[3, 2] = 3 / 16

        self.a[4, 0] = 79129 / 250000
        self.a[4, 1] = 0.0
        self.a[4, 2] = -261237 / 250000
        self.a[4, 3] = 19663 / 15625

        self.a[5, 0] = 1336883 / 4909125
        self.a[5, 1] = 0.0
        self.a[5, 2] = -25476 / 30875
        self.a[5, 3] = 194159 / 185250
        self.a[5, 4] = 8225 / 78546

        self.a[6, 0] = -2459386 / 14727375
        self.a[6, 1] = 0.0
        self.a[6, 2] = 19504 / 30875
        self.a[6, 3] = 2377474 / 13615875
        self.a[6, 4] = -6157250 / 5773131
        self.a[6, 5] = 902 / 735

        self.a[7, 0] = 2699 / 7410
        self.a[7, 1] = 0.0
        self.a[7, 2] = -252 / 1235
        self.a[7, 3] = -1393253 / 3993990
        self.a[7, 4] = 236875 / 72618
        self.a[7, 5] = -135 / 49
        self.a[7, 6] = 15 / 22

        self.a[8, 0] = 11 / 144
        self.a[8, 1] = 0.0
        self.a[8, 2] = 0.0
        self.a[8, 3] = 256 / 693
        self.a[8, 4] = 0.0
        self.a[8, 5] = 125 / 504
        self.a[8, 6] = 125 / 528
        self.a[8, 7] = 5 / 72

        return self.a

    def coeff_c(self):
        self.c[1] = 9 / 50
        self.c[2] = 1 / 6
        self.c[3] = 1 / 4
        self.c[4] = 53 / 100
        self.c[5] = 3 / 5
        self.c[6] = 4 / 5
        self.c[7] = 1.0
        self.c[8] = 1.0
        return self.c

    # -- 5th order weights --#
    def coeff_bt(self):
        self.bt[0] = 11 / 144
        self.bt[1] = 0.0
        self.bt[2] = 0.0
        self.bt[3] = 256 / 693
        self.bt[4] = 0.0
        self.bt[5] = 125 / 504
        self.bt[6] = 125 / 528
        self.bt[7] = 5 / 72
        self.bt[8] = 0.0
        return self.bt

    # -- 6th order weights --#
    def coeff_bhat(self):
        self.bhat[0] = 28 / 477
        self.bhat[1] = 0.0
        self.bhat[2] = 0.0
        self.bhat[3] = 212 / 441
        self.bhat[4] = -312500 / 366177
        self.bhat[5] = 2125 / 1764
        self.bhat[6] = 0.0
        self.bhat[7] = -2105 / 35532
        self.bhat[8] = 2995 / 17766
        return self.bhat


class RK41Explicit:
    def __init__(self):
        self.a = np.zeros((4, 4), dtype=float)
        self.c = np.zeros((4,), dtype=float)
        self.b = np.zeros((4,), dtype=float)

    def coeff_matA(self):
        self.a[1, 0] = 1 / 2
        self.a[2, 1] = 1 / 2
        self.a[3, 2] = 1.0
        return self.a

    def coeff_c(self):
        self.c[1] = 1 / 2
        self.c[2] = 1 / 2
        self.c[3] = 1.0
        return self.c

    def coeff_b(self):
        self.b[0] = 1 / 6
        self.b[1] = 1 / 3
        self.b[2] = 1 / 3
        self.b[3] = 1 / 6
        return self.b
