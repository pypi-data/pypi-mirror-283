import numpy as np

np.set_printoptions(precision=8)
from tableaux import DormandPrince45


# CashKarp --> CHECKED
# DormandPrince45 --> CHECKED
# DormandPrince78 --> CHECKED
# Fehlberg78 --> CHECKED
# Verner56

###----- Coefficient Checks -----###

m = DormandPrince45()
bt = m.coeff_bt()
bhat = m.coeff_bhat()
c = m.coeff_c()
a = m.coeff_matA()


# = 1
total_b = sum(bt)
total_bhat = sum(bhat)

if round(total_b, 2) == round(1.0, 2):
    print(f"total_b = {round(total_b,2)}")
else:
    print("total_b is NOT 1.0")

if round(total_bhat, 2) == round(1.0, 2):
    print(f"total_bhat = {round(total_bhat,2)}")
else:
    print("total_bhat is NOT 1.0")

comp_b = np.allclose(total_b, total_bhat)
print(f"total_b == total_bhat: {comp_b}")

print()


# = 1/2
mul_bt_c = np.dot(bt, c)
mul_bhat_c = np.dot(bhat, c)

if round(mul_bt_c, 2) == round(1 / 2, 2):
    print(f"b x c = {round(mul_bt_c,2)}")
else:
    print("b x c is NOT 1/2")

if round(mul_bhat_c, 2) == round(1 / 2, 2):
    print(f"bhat x c = {round(mul_bhat_c,2)}")
else:
    print("bhat x c is NOT 1/2")

comp_mul_b_c = np.allclose(mul_bt_c, mul_bhat_c)
print(f"b x c == bhat x c: {comp_mul_b_c}")

print()

# = 1/3
mul_bt_c2 = np.dot(bt, c**2)
mul_bhat_c2 = np.dot(bhat, c**2)

if round(mul_bt_c2, 5) == round(1 / 3, 5):
    print(f"b x c^2 = {round(mul_bt_c2,5)}")
else:
    print("b x c^2 is NOT 1/3")

if round(mul_bhat_c2, 5) == round(1 / 3, 5):
    print(f"bhat x c^2 = {round(mul_bhat_c2,5)}")
else:
    print("bhat x c^2 is NOT 1/3")

comp_mul_b_c2 = np.allclose(mul_bt_c2, mul_bhat_c2)
print(f"b x c^2 == bhat x c^2: {comp_mul_b_c2}")

print()

# = 1/4
mul_bt_c3 = np.dot(bt, c**3)
mul_bhat_c3 = np.dot(bhat, c**3)

if round(mul_bt_c3, 2) == 1 / 4:
    print(f"b x c^3 = {round(mul_bt_c3,2)}")
else:
    print("b x c^3 is NOT 1/4")

if round(mul_bhat_c3, 2) == 1 / 4:
    print(f"bhat x c^3 = {round(mul_bhat_c3,2)}")
else:
    print("bhat x c^3 is NOT 1/4")

comp_mul_b_c3 = np.allclose(mul_bt_c3, mul_bhat_c3)
print(f"b x c^3 == bhat x c^3: {comp_mul_b_c3}")

print()

# = 1/6
bt_a_c = np.linalg.multi_dot([bt, a, c])
bhat_a_c = np.linalg.multi_dot([bhat, a, c])

if round(bt_a_c, 5) == round(1 / 6, 5):
    print(f"b x a x c = {round(bt_a_c,5)}")
else:
    print("b x a x c is NOT 1/6")

if round(bhat_a_c, 5) == round(1 / 6, 5):
    print(f"bhat x a x c = {round(bhat_a_c,5)}")
else:
    print("bhat x a x c is NOT 1/6")

b_a_c = np.allclose(bt_a_c, bhat_a_c)
print(f"b x a x c == bhat x a x c: {b_a_c}")

print()

# = 1/12
bt_a_c2 = np.linalg.multi_dot([bt, a, c**2])
bhat_a_c2 = np.linalg.multi_dot([bhat, a, c**2])

if round(bt_a_c2, 5) == round(1 / 12, 5):
    print(f"b x a x c^2 = {round(bt_a_c2,5)}")
else:
    print("b x a x c^2 is NOT 1/12")

if round(bhat_a_c2, 5) == round(1 / 12, 5):
    print(f"bhat x a x c^2 = {round(bhat_a_c2,5)}")
else:
    print("bhat x a x c^2 is NOT 1/12")

b_a_c2 = np.allclose(bt_a_c2, bhat_a_c2)
print(f"b x a x c^2 == bhat x a x c^2: {b_a_c2}")

print()

# = 1/20
bt_a_c3 = np.linalg.multi_dot([bt, a, c**3])
bhat_a_c3 = np.linalg.multi_dot([bhat, a, c**3])

if round(bt_a_c3, 2) == round(1 / 20, 2):
    print(f"b x a x c^3 = {round(bt_a_c3,2)}")
else:
    print("b x a x c^3 is NOT 1/20")

if round(bhat_a_c3, 2) == round(1 / 20, 2):
    print(f"bhat x a x c^3 = {round(bhat_a_c3,2)}")
else:
    print("bhat x a x c^3 is NOT 1/20")

b_a_c3 = np.allclose(bt_a_c3, bhat_a_c3)
print(f"b x a x c^3 == bhat x a x c^3: {b_a_c3}")

print()

# = 0
mul_bt_a2 = np.dot(bt, a[:, 1])
mul_bhat_a2 = np.dot(bhat, a[:, 1])
bt_a_a2 = np.linalg.multi_dot([bt, a, a[:, 1]])

if round(mul_bt_a2, 8) == round(0.0, 8):
    print(f"b_i x a_i2 = {round(mul_bt_a2,8)}")
else:
    print("b_i x a_i2 is NOT 0")

if round(mul_bhat_a2, 8) == round(0.0, 8):
    print(f"bhat_i x a_i2 = {round(mul_bhat_a2,8)}")
else:
    print("bhat_i x a_i2 is NOT 0")

if round(bt_a_a2, 8) == round(0.0, 8):
    print(f"b_i x a_ij x a_i2 = {round(bt_a_a2,8)}")
else:
    print("b_i x a_ij x a_i2 is NOT 0")

print()

# = 1.5 = 3/2
c3_div_c2 = c[2] / c[1]

if round(c3_div_c2, 2) == round(3 / 2, 2):
    print(f"c3 / c2 = {round(c3_div_c2,2)}")
else:
    print("c3 / c2 is NOT 3/2")


if bt[1] == 0.0:
    print(f"b[1] = {bt[1]}")
else:
    print("b[1] is NOT 0")

if bhat[1] == 0.0:
    print(f"bhat[1] = {bhat[1]}")
else:
    print("bhat[1] is NOT 0")

print()

z = 10
n = len(bt)

for i in range(1, n):
    if round(c[i], z) == round(sum(a[i, :]), z):
        print(
            f"c[{i}] == sum(a[{i},:]): c[{i}] = {round(c[i],z)} -- sum(a[{i},:]) = {round(sum(a[i,:]),z)}"
        )
    else:
        print(f"c[{i}] != sum(a[{i},:])")
