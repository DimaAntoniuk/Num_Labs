from math import ceil
import matplotlib.pylab as plt
import copy
import numpy

C2 = 0.2 * 10 ** -3
L_min = 0.03
L_max = 0.3
i_min = 1
i_max = 2
L2 = 0.5
R1 = 10
R2 = 20
R3 = 50
R4 = 100
half_period = 0.01
period = 2 * half_period


def draw_graph(x_arguments, y_values, title="", x_label="", y_label=""):
    graph = plt.figure().gca()
    graph.plot(x_arguments, y_values)
    graph.set_title(title)
    graph.set_xlabel(x_label)
    graph.set_ylabel(y_label)
    plt.show()


def input_voltage(time_point):
    number_of_half_periods = ceil(time_point / half_period)

    if number_of_half_periods % 2:
        return 10
    else:
        return -10
    return 0


def output_voltage(value):
    return value[0]


def inductance(current_value):
    if abs(current_value) <= i_min:
        return L_max

    if abs(current_value) >= i_max:
        return L_min

    A = numpy.array(
    [
        [1, i_min, i_min**2, i_min**3, L_max],
        [1, i_max, i_max**2, i_max**3, L_min],
        [0, 1, 2 * i_min, 3 * i_min**2, 0],
        [0, 1, 2 * i_max, 3 * i_max**2, 0]
    ])

    a = gaussFunc(A)

    return a[0] + a[1]*abs(current_value) + a[2]*current_value**2 + a[3]*abs(current_value**3)


differential_equations = \
    [lambda time_point, value: (value[2] - value[0]/R4) / C2,
     lambda time_point, value: (input_voltage(time_point) - value[1] * (R1+R3) + value[2]*R3) / inductance(value[1]),
     lambda time_point, value: (value[1] * R3 - value[2] * (R2+R3) - value[0]) / L2]


def get_next_value(time_point, value, step):
    """Runge-Kutta method"""
    next_value = value

    for i in range(len(value)):
        this_value = value[i]
        coefficient1 = step * differential_equations[i](time_point, value)
        value[i] = this_value + 0.5 * coefficient1
        coefficient2 = step * differential_equations[i](time_point + 0.5 * step, value)
        value[i] = this_value + 2 * coefficient2 - coefficient1
        coefficient3 = step * differential_equations[i](time_point + step, value)
        value[i] = this_value

        next_value[i] = value[i] + (coefficient1 + 4 * coefficient2 + coefficient3) / 6

    return next_value


def get_results(time_point, time_interval, value, step):
    time_value_pairs = dict()
    time_value_pairs[time_point] = [value[0], value[1], value[2], input_voltage(time_point), output_voltage(value)]

    while time_point < time_interval:
        value = get_next_value(time_point, value, step)
        time_point += step

        time_value_pairs[time_point] = [value[0], value[1], value[2], input_voltage(time_point), output_voltage(value)]

    return time_value_pairs

def gaussFunc(a):
    eps = 1e-16

    c = numpy.array(a)
    a = numpy.array(a)

    len1 = 4
    len2 = 5
    vectB = copy.deepcopy(a[:, len1])

    for g in range(len1):

        max = abs(a[g][g])
        my = g
        t1 = g
        while t1 < len1:

            if abs(a[t1][g]) > max:
                max = abs(a[t1][g])
                my = t1
            t1 += 1

        if abs(max) < eps:
            print("Check determinant")

        if my != g:
            b = copy.deepcopy(a[g])
            a[g] = copy.deepcopy(a[my])
            a[my] = copy.deepcopy(b)

        amain = float(a[g][g])

        z = g
        while z < len2:
            a[g][z] = a[g][z] / amain
            z += 1

        j = g + 1

        while j < len1:
            b = a[j][g]
            z = g

            while z < len2:
                a[j][z] = a[j][z] - a[g][z] * b
                z += 1
            j += 1

    a = backTrace(a, len1, len2)
    #
    # print("Fallibility:")
    #
    # print(vectorN(c, a, len1, vectB))

    return a


def backTrace(a, len1, len2):
    a = numpy.array(a)
    i = len1 - 1
    while i > 0:
        j = i - 1

        while j >= 0:
            a[j][len1] = a[j][len1] - a[j][i] * a[i][len1]
            j -= 1
        i -= 1
    return a[:, len2 - 1]


def vectorN(c, a, len1, vectB):
    c = numpy.array(c)
    a = numpy.array(a)
    vectB = numpy.array(vectB)

    b = numpy.zeros((len1))

    i = 0

    while i < len1:
        j = 0
        while j < len1:
            b[i] += c[i][j] * a[j]

            j += 1

        i = i + 1

    c = copy.deepcopy(b)

    for i in range(len1):
        c[i] = abs(c[i] - vectB[i])

    return c


def main():
    time_point = 0
    # value[0] = U_C2, value[1] = i1, value[2] = i2
    value = [0, 0, 0]
    time_interval = 5 * period

    step = period / 400

    time_value_pairs = get_results(time_point, time_interval, value, step)

    time_points = []
    values_u_c2 = []
    values_i1 = []
    values_i2 = []
    values_u1 = []
    values_u2 = []
    values_of_inductance = []

    i_interval = []
    i = 0
    while i <= i_max + 1:
        i_interval.append(i)
        values_of_inductance.append(inductance(i))
        i += step

    for t, v in time_value_pairs.items():
        time_points.append(t)
        values_u_c2.append(v[0])
        values_i1.append(v[1])
        values_i2.append(v[2])
        values_u1.append(v[3])
        values_u2.append(v[4])

    draw_graph(i_interval, values_of_inductance, "L1", "i, amp", "L, henry")
    draw_graph(time_points, values_u1, "U1", "t, sec", "u, volt")
    draw_graph(time_points, values_i1, "i1", "t, sec", "i, amp")
    draw_graph(time_points, values_u_c2, "U_C2", "t, sec", "u, volt")
    draw_graph(time_points, values_i2, "i2", "t, sec", "i, amp")
    draw_graph(time_points, values_u2, "U2", "t, sec", "u, volt")


if __name__ == '__main__':
    main()
