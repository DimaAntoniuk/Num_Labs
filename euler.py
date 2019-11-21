from math import sin, pi
import matplotlib.pylab as plt

U_max = 100
frequency = 50
R1 = 5
R2 = 4
R3 = 7
R4 = 2
L = 0.01
C1 = 300 * 10 ** -6

f = [lambda cur_time, value: ((U_max * sin(2 * pi * frequency * cur_time) - value[0] - value[1]*R1) / ((R1+R2)*C1) + value[1]/C1),
     lambda cur_time, value: (((U_max * sin(2 * pi * frequency * cur_time) - value[0] - value[1]*R1)/(R1 + R2))*(R2/L) - value[1]*(R3+R4)/L)]


def output_voltage(value):
    return value[1] * R4


def get_next_value(cur_time, next_cur_time, value, h):
    next_value = value

    for i in range(len(value)):
        next_value[i] = value[i] + h * f[i](cur_time, value)

    return next_value


def get_results(cur_time, time_end, value, h):
    time_value = dict()

    while cur_time < time_end:
        next_cur_time = cur_time + h
        next_value = get_next_value(cur_time, next_cur_time, value, h)

        cur_time = next_cur_time
        value = next_value

        time_value[cur_time] = output_voltage(value)

    return time_value


def main():
    cur_time = 0
    value = [0, 0]
    time_end = 0.2
    h = 0.00001

    time_value = get_results(cur_time, time_end, value, h)

    cur_times = []
    values = []
    for t, v in time_value.items():
        cur_times.append(t)
        values.append(v)

    plt.plot(cur_times, values)
    plt.show()


if __name__ == '__main__':
    main()
