import sys; args = sys.argv[1:]
#Tae Ha Kim
import math

#methods to hard code functions
def func(x_val):
    return 2 * math.pow(x_val, 3) + 3 * math.pow(x_val, 2)
def first_deriv(x_val):
    return 6 * math.pow(x_val, 2) + 6 * x_val
def second_deriv(x_val):
    return 12 * x_val + 6
def main():
    x_0 = float(args[0])
    tracker = set()
    a = 0.0
    count = 0
    while a > 0.01 or count < 10000:
        if second_deriv(x_0) == 0: print("Second derivative is 0, code will not work!"); break
        if abs(first_deriv(x_0)) < 0.01: print("Found minimum/maximum"); break
        a = first_deriv(x_0) / second_deriv(x_0)
        x_0 = x_0 - a
        tracker.add(x_0)
        count += 1
        
        print(x_0)
    
    print("X value: ", x_0); print("In {} iterations".format(count)) 


if __name__ == '__main__':
    main()
