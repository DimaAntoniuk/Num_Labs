def main():
    partitions = 100
    inner_func = lambda x: (2 + 3 * x) ** (1 / 2)
    f = lambda x: ((2 + 3 * x) ** (3 / 2)) / 3
    lower_limit = 1
    upper_limit = 2

    integral = 0
    middle_point = (upper_limit - lower_limit) / (2 * partitions)
    integral += inner_func(lower_limit) + inner_func(upper_limit)
    for i in range(partitions):
        integral += 4 * inner_func(lower_limit + (2 * i - 1) * middle_point)
    for i in range(partitions - 1):
        integral += 2 * inner_func(lower_limit + 2 * i * middle_point)
    integral *= middle_point / 3
    print("Result: ", integral)
    print("Verification:")
    print("{} ~= {}".format(integral, f(upper_limit) - f(lower_limit)))


main()
