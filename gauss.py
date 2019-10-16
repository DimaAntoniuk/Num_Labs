k = 1
p = 21
s = 0.02*k
b = 0.02*p
A = [[8.3, 2.62+s, 4.1, 1.9, -10.65+b],
     [3.92, 8.45, 7.78-s, 2.46, 12.21],
     [3.77, 7.21+s, 8.04, 2.28, 15.45-b],
     [2.21, 3.65-s, 1.69, 6.69, -8.35]]
n = 4
m = 5
X = [0]*n
A_o = [[8.3, 2.62+s, 4.1, 1.9, -10.65+b],
     [3.92, 8.45, 7.78-s, 2.46, 12.21],
     [3.77, 7.21+s, 8.04, 2.28, 15.45-b],
     [2.21, 3.65-s, 1.69, 6.69, -8.35]]

def gauss(A):
    global n
    global m
    global X
    for k in range(n):
        for i in range(k+1, n):
            x = A[i][k]/A[k][k]
            for j in range(0, m):
                A[i][j] = A[i][j] - A[k][j]*x

    for i in range(n):
        a = A[i][i]
        for j in range(m):
            A[i][j] = A[i][j]/a

    X[3] = A[3][4]
    X[2] = A[2][4]- A[2][3]*X[3]
    X[1] = A[1][4] - A[1][2]*X[2] - A[1][3]*X[3]
    X[0] = A[0][4] - A[0][1]*X[1] - A[0][2]*X[2] - A[0][3]*X[3]
    return X

print(str(gauss(A)));
for row in range(n):
    sum = 0
    for col in range(m-1):
        sum = sum + A_o[row][col]*X[col]
    print(sum)
#
# for row in range(n):
#     print(A[row])
