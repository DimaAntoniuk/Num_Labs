import math

def f(x):
    return math.log(x) + math.cos(x/4)

a, b = 0.1, 3.0
e = float(input("E = "))
k = 0
_x = a

while b-a>=2*e:
    x = (a+b)/2
    fa = f(a)
    fx = f(x)
    if fa*fx > 0:
        a = x
    else:
        b = x
    _x = (a + b)/2
    k += 1
print("X = " + str("%.7f" % _x))
print("k = " + str("%.7f" % k))
print("f(X) = " + str("%.7f" % f(_x)))
