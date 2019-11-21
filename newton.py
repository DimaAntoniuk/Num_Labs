import copy
import math


def main():
    roots_number = 2
    starting_x1 = -0.1
    starting_x2 = 0.1
    epsilon = 10 ** -6
    elementary_matrix = [[1, 0],[0, 1]]
    f1 = lambda x1, x2: (math.e ** x1) * math.cos(x2) - 1 - x1
    f2 = lambda x1, x2: (math.e ** x1) * math.sin(x2) + 1 - x2
    jacobian = copy.deepcopy(elementary_matrix)
    x_older = [starting_x1, starting_x2]
    x_old = [starting_x1 + 0.01, starting_x2 + 0.01]
    x = [starting_x1, starting_x2]
    epsilon_is_reached = [False, False]

    while not all(condition for condition in epsilon_is_reached):

        f = [f1(x[0], x[1]), f2(x[0], x[1])]
        jacobian[0][0] = (math.e ** x[0]) * math.cos(x[1]) - 1
        jacobian[0][1] = (math.e ** x[0]) * (-math.sin(x[1]))
        jacobian[1][0] = (math.e ** x[0]) * math.sin(x[1])
        jacobian[1][1] = (math.e ** x[0]) * math.cos(x[1]) - 1
        invers = copy.deepcopy(jacobian)
        for b in range(roots_number):
            v_array = copy.deepcopy(jacobian)
            c_array = copy.deepcopy(jacobian)
            p_array = [elementary_matrix[i][b] for i in range(roots_number)]
            y_array = copy.deepcopy(p_array)
            for k in range(roots_number):
                # column sort begin
                max_value = abs(v_array[k][k])
                w = k
                for l in range(k + 1, roots_number):
                    if max_value < abs(v_array[l][k]):
                        max_value = abs(v_array[l][k])
                        w = l
                for d in range(roots_number):
                    value = v_array[k][d]
                    v_array[k][d] = v_array[w][d]
                    v_array[w][d] = value
                # column sort end
                y_array[k] = p_array[k] / v_array[k][k]
                for i in range(k + 1, roots_number):
                    p_array[i] -= v_array[i][k] * y_array[k]
                    for j in range(k + 1, roots_number):
                        c_array[k][j] = v_array[k][j] / v_array[k][k]
                        v_array[i][j] -= v_array[i][k] * c_array[k][j]
            x_y_array = copy.deepcopy(y_array)
            for i in range(roots_number - 1, -1, -1):
                cx_sum = 0
                for j in range(i + 1, roots_number):
                    cx_sum += c_array[i][j] * x_y_array[j]
                x_y_array[i] = y_array[i] - cx_sum
            for i in range(roots_number):
                invers[i][b] = x_y_array[i]

        f = [f1(x[0], x[1]), f2(x[0], x[1])]
        for i in range(roots_number):
            invers_f_sum = 0
            for j in range(roots_number):
                invers_f_sum += invers[i][j] * f[j]
            x[i] = x_old[i] - invers_f_sum

        for i in range(roots_number):
            if (((x[i] - x_old[i]) / x[i]) * 100) < epsilon:
                epsilon_is_reached[i] = True
            else:
                epsilon_is_reached[i] = False
            x_older[i] = x_old[i]
            x_old[i] = x[i]
    print("Results:")
    print("\tx =", x[0])
    print("\ty =", x[1])
    print("Verification:")
    print("\te^x*cos(y) - 1 - x ~=", f1(x[0], x[1]))
    print("\te^x*sin(y) + 1 - y ~=", f2(x[0], x[1]))


main()
