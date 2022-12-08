import sys; args = sys.argv[1:]
#Tae Ha Kim
import numpy as np


def main():
    x = float(args[0])
    y = float(args[1])
    count = 0
    s = np.array([])
    vec = np.array([x, y])
    hes = generate_Hessian(x, y)
    while count < 10000:
        det = np.linalg.det(hes)
        if abs(x_partial(vec[0], vec[1])) < 0.01 and abs(y_partial(vec[0], vec[1])) < 0.01: 
            if det < 0: print("Point is a saddle point, not a min/max"); break
            elif det == 0: print("Inconclusive, Hessian det is 0"); break
            print("Min/max found"); break
        inv = np.linalg.inv(hes)
        s = np.dot(inv, generate_gradient(vec[0], vec[1]))
        vec = np.subtract(vec, s)
        hes = generate_Hessian(vec[0], vec[1])
        print(vec)
        count += 1
    print(vec); print("In {} iterations".format(count)) 
#generate Hessian matrix 
def generate_Hessian(x_0, y_0):
    return np.array([[x_double(x_0, y_0), xy_partial(x_0, y_0)],
                     [xy_partial(x_0, y_0), y_double(x_0, y_0)] ])
#methods to hard code the derivatives into 
def xy_partial(x_0, y_0):
    return -3
def x_double(x_0, y_0):
    return 90 * x_0
def y_double(x_0, y_0):
    return 90 * y_0
def x_partial(x_0, y_0):
    return 45 * x_0 * x_0 - 3 * y_0
def y_partial(x_0, y_0):
    return (-3) * x_0 + 45 * y_0 * y_0
def generate_gradient(x_0, y_0):
    return np.array([x_partial(x_0, y_0), y_partial(x_0, y_0)])
if __name__ == '__main__':
    main()