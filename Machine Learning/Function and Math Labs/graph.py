import sys
import os 
import math
import re

#Kingsley Kim 
#

def main():

    x_0 = 2.91
    # f0 = convert(args[0]); f1 = convert(args[1]); x_0 = args[2]
    y_val = 100000000.0
    count = 0
    der = 0

    while abs(func(x_0)) > 0.01 or count < 10000: #while y value is not zero, or iteration count is reached
        # y_val = float(input("What is the y-value?"))
        # der = float(input("Derivative?"))
        # if der == 0.0: print("Reached max/min, code is stuck!"); break
        # y_inter = y_val - der * x_0
        # x_inter = (-1)*y_inter / der

        # x_0 = x_inter
        # print(x_0)
        # count+=1
        print(x_0, count)
        if deriv(x_0) == 0: ("Reached max/min"); break
        res = func(x_0) / deriv(x_0) 
        x_0 = x_0 - res
        
        count+=1 
    print(x_0, count)


def func(x_val):
    return math.sin(x_val)

def deriv(x_val):
    return math.cos(x_val)




if __name__ == "__main__":
    main()