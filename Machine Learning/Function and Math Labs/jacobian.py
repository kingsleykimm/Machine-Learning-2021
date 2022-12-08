import sys; args = sys.argv[1:]
#Tae Ha Kim
import numpy as np
import math

def main():
    x = float(args[0])
    y = float(args[1])
    count = 0
    s = np.array([1.0, 1.0])
    vec = np.array([x, y])
    jac = generate_jacobian(x, y)
    tracker = set()
    while count < 1000:
        # if np.linalg.norm(s) < 0.05: break
        inv = np.linalg.inv(jac)
        s = np.dot(inv, generate_func(vec[0], vec[1]))
        vec = np.subtract(vec, s)
        jac = generate_jacobian(vec[0], vec[1])
        tracker.add(vec[0])
        print(vec)
        count += 1
     
    if vec[0] in tracker:
        print("Curves do not intersect, no answer")
    else:        
        print(vec, count)

#have to hardcode the functions and partials
def generate_func(x_0, y_0):
    return np.array([func1(x_0, y_0), func2(x_0, y_0)])
def func1(x_0, y_0):
    return 4*math.pow(x_0, 2) + math.pow(y_0, 3)
def func2(x_0, y_0):
    return 2*x_0 + 3*y_0 + 2

def generate_jacobian(x_0, y_0):
    return np.array([[xpartial_f1(x_0, y_0), ypartial_f1(x_0, y_0)],
                     [xpartial_f2(x_0, y_0), ypartial_f2(x_0, y_0)]])                                            
def xpartial_f1(x_0, y_0):
    return 8*x_0
def ypartial_f1(x_0, y_0):
    return 3 * y_0 * y_0
def xpartial_f2(x_0, y_0):
    return 2 
def ypartial_f2(x_0, y_0):
    return 3
if __name__ == '__main__':
    main()