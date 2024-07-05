import numpy as np

np.set_printoptions(precision=8)
from tableaux import DormandPrince78


# CashKarp --> CHECKED
# DormandPrince45 --> CHECKED
# DormandPrince78 --> CHECKED
# Fehlberg45 --> CHECKED
# Fehlberg67
# Fehlberg78 --> CHECKED
# Verner56

###----- Coefficient Checks -----###

m = DormandPrince78()
bt = m.coeff_bt()
bhat = m.coeff_bhat()
c = m.coeff_c()
a = m.coeff_matA()


def test_one(bt, bhat):
    # = 1
    total_b = sum(bt)
    total_bhat = sum(bhat)

    if np.allclose(total_b, total_bhat) == True:
        print(f"Passed test 1: total_b = total_bhat = {total_b:.2f} == {np.allclose(total_b, total_bhat)}")
        return 1
    else:
        print(f"Not passed test 1: total_b = total_bhat == {np.allclose(total_b, total_bhat)}")
        return 0


def test_two(bt, bhat, c):
    # = 1/2
    mul_bt_c = np.dot(bt, c)
    mul_bhat_c = np.dot(bhat, c)

    if np.allclose(mul_bt_c, mul_bhat_c) == True:
        print(f"Passed test 2: b x c = bhat x c = {mul_bt_c:.2f} == {np.allclose(mul_bt_c, mul_bhat_c)}")
        return 1
    else:
        print(f"Not passed test 2: b x c = bhat x c == {np.allclose(mul_bt_c, mul_bhat_c)}")
        return 0


def test_three(bt, bhat, c):
    # = 1/3
    mul_bt_c2 = np.dot(bt, c**2)
    mul_bhat_c2 = np.dot(bhat, c**2)

    if np.allclose(mul_bt_c2, mul_bhat_c2) == True:
        print(f"Passed test 3: b x c^2 = bhat x c^2 = {mul_bt_c2:.2f} == {np.allclose(mul_bt_c2, mul_bhat_c2)}")
        return 1
    else:
        print(f"Not passed test 3: b x c^2 = bhat x c^2 == {np.allclose(mul_bt_c2, mul_bhat_c2)}")
        return 0


def test_four(bt, bhat, c):
    # = 1/4
    mul_bt_c3 = np.dot(bt, c**3)
    mul_bhat_c3 = np.dot(bhat, c**3)

    if np.allclose(mul_bt_c3, mul_bhat_c3) == True:
        print(f"Passed test 4: b x c^3 = bhat x c^3 = {mul_bhat_c3:.2f} == {np.allclose(mul_bt_c3, mul_bhat_c3)}")
        return 1
    else:
        print(f"Not passed test 4: b x c^3 = bhat x c^3 == {np.allclose(mul_bt_c3, mul_bhat_c3)}")
        return 0


def test_five(bt, bhat, a, c):
    # = 1/6
    bt_a_c = np.linalg.multi_dot([bt, a, c])
    bhat_a_c = np.linalg.multi_dot([bhat, a, c])

    if np.allclose(bt_a_c, bhat_a_c) == True:
        print(f"Passed test 5: b x a x c = bhat x a x c = {bt_a_c:.3f} == {np.allclose(bt_a_c, bhat_a_c)}")
        return 1
    else:
        print(f"Not passed test 5: b x a x c = bhat x a x c == {np.allclose(bt_a_c, bhat_a_c)}")
        return 0


def test_six(bt, bhat, a, c):
    # = 1/12
    bt_a_c2 = np.linalg.multi_dot([bt, a, c**2])
    bhat_a_c2 = np.linalg.multi_dot([bhat, a, c**2])

    if round(bt_a_c2, 5) == round(1 / 12, 5) and round(bhat_a_c2, 5) == round(
        1 / 12, 5
    ):
        print(f"Passed test 6: b x a x c^2 = bhat x a x c^2 = {bt_a_c2:.3f} == {round(bt_a_c2, 5) == round(bhat_a_c2, 5)}")
        return 1
    else:
        print(f"Not passed test 6: b x a x c^2 = bhat x a x c^2 == {round(bt_a_c2, 5) == round(bhat_a_c2, 5)}")
        return 0


def test_seven(bt, bhat, a, c):
    # = 1/20
    bt_a_c3 = np.linalg.multi_dot([bt, a, c**3])
    bhat_a_c3 = np.linalg.multi_dot([bhat, a, c**3])

    if round(bt_a_c3, 2) == round(1 / 20, 2) and round(bhat_a_c3, 2) == round(
        1 / 20, 2
    ):
        print(f"Passed test 7: b x a x c^3 = bhat x a x c^3 = {bt_a_c3:.2f} == {round(bt_a_c3, 2) == round(bhat_a_c3, 2)}")
        return 1
    else:
        print(f"Not passed test 7: b x a x c^3 = bhat x a x c^3 == {round(bt_a_c3, 2) == round(bhat_a_c3, 2)}")
        return 0


def test_eight(bt, bhat, a):
    # = 0
    mul_bt_a2 = np.dot(bt, a[:, 1])
    mul_bhat_a2 = np.dot(bhat, a[:, 1])
    bt_a_a2 = np.linalg.multi_dot([bt, a, a[:, 1]])

    if (
        round(mul_bt_a2, 8) == round(0.0, 8)
        and round(mul_bhat_a2, 8) == round(0.0, 8)
        and round(bt_a_a2, 8) == round(0.0, 8)
    ):
        print("Passed test 8")
        return 1
    else:
        print("Not passed test 8")
        return 0


def test_nine(c):
    # = 1.5 = 3/2
    c3_div_c2 = c[2] / c[1]

    if round(c3_div_c2, 2) == round(3 / 2, 2):
        print(f"Passed test 9: c[2] / c[1] = 1.5 == {round(c3_div_c2, 2) == round(3 / 2, 2)}")
        return 1
    else:
        print("Not passed test 9")
        return 0


def test_ten(bt):
    if bt[1] == 0.0:
        print(f"Passed test 10: b[1] = 0 == {bt[1]==0.0}")
        return 1
    else:
        print("Not passed test 10")
        return 0


def test_eleven(bhat):
    if bhat[1] == 0.0:
        print(f"Passed test 11: bhat[1] = 0 == {bhat[1]==0.0}")
        return 1
    else:
        print("Not passed test 11")
        return 0


def test_twelve(bt, a, c):
    z = 10
    n = len(bt)

    for i in range(1, n):
        if round(c[i], z) == round(sum(a[i, :]), z):
            print("Passed test 12")
            return 1
        else:
            print("Not passed test 12")
            return 0


if (
    test_one(bt, bhat) == 1
    and test_two(bt, bhat, c) == 1
    and test_three(bt, bhat, c) == 1
    and test_four(bt, bhat, c) == 1
    and test_five(bt, bhat, a, c) == 1
    and test_six(bt, bhat, a, c) == 1
    and test_seven(bt, bhat, a, c) == 1
    and test_eight(bt, bhat, a) == 1
    and test_nine(c) == 1
    and test_ten(bt) == 1
    and test_eleven(bhat) == 1
    and test_twelve(bt, a, c) == 1
):
    print("-- Passed all 12 tests --")
else:
    print("Not passed.")
