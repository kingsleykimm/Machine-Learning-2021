#NOTE: WEIGHTS NEED TO BE MANUALLY CHANGED IN FILE
import sys; args = sys.argv[1:]
myVar = open(args[0], 'r').read().splitlines()
import math

def power(A, pow_val): #method to raise a list to a power pow_val
    temp_li = [1]
    for i in range(pow_val):
        temp_li = polynomialMulti(A, temp_li, len(A), len(temp_li), False)
    return temp_li
def evaluate(input_list, x): #method to evaluate a polynomial a list at x
    sum = 0
    for i in range(len(input_list)):
        sum += input_list[i]*math.pow(x, i)
    return sum
def clean_output(input_list): #prints a coefficient list as a polynomial
    s = ""
    for i in range(len(input_list)):
        if i == 0:
            s += str(input_list[i])
        else:
            if 'e' in str(input_list[i]):
                index = str(input_list[i]).index('e')
                power = str(input_list[i])[index+1:index+4]
                s+= (str(input_list[i])[0:-4] + "*10^{" + power + "}" + "x^{" + str(i) + "}")
            else:
                s += (str(input_list[i])) + "x^{" + str(i) + "}"
        if i == len(input_list)-1: continue
        s += " + "
    return s
def polynomialMulti(A, B, a_size, b_size, logis): #Polynomial multiplication method
    new_li = []
    for j in range(a_size + b_size-1):
        new_li.append(0)
    for a in range(a_size):
        for b in range(b_size):
            prod = A[a] * B[b]
            new_li[a+b] += prod
    return new_li
def polynomialAdd(A, B): #Polynomial addition method
    a_size = len(A); b_size = len(B)
    if a_size>= b_size:
        for i in range(b_size):
            A[i] += B[i]
        return A
    else:
        for i in range(a_size):
            B[i] += A[i]
        return B
def polynomialSubtract(A, B): #Polynomial subtraction method
    a_size = len(A); b_size = len(B)
    if a_size >= b_size:
        for i in range(b_size):
            A[i] -= B[i]
        return A
    else:
        for i in range(a_size):
            B[i] -= A[i]
        return B
def logistic_deriv(n): #returns the nth derivative of the transfer function
    if n == 0:
        return [0, 1]
    elif n == 1:
        return [0, 1, -1]
    else:
        li = logistic_deriv(n-1)
        new_li = []
        for i in range(1, len(li)):
            new_li.append(li[i] * i)
        return polynomialMulti(new_li, [0, 1, -1], len(new_li), 3, True)
    # [0, 1, -3, 2] => [1, -6, 6]
def evaluate_logistic(x): #returns a coefficient list of the Taylor polynomial at x
    f = 1 / (1 + math.exp(-x))
    ret = []
    for i in range(4):
        sum = 0
        poly = logistic_deriv(i)
        for j in range(len(poly)):
            sum += poly[j] * math.pow(f, j)
        ret.append(sum)
    for i in range(4):
        ret[i] = ret[i] / math.factorial(i)
    return ret
def transferFunc(input_list, val): #Transfer function that takes in an input_list and generates a Taylor series 
    center = round(evaluate(input_list, val))
    polyList = []
    polyList = evaluate_logistic(center)
    initial = []
    input_list[0] = input_list[0] - center
    for count, value in enumerate(polyList):
        power_li = power(input_list, count)
        initial = polynomialAdd([x * value for x in power_li], initial)
    return initial
def transfer(input_li, val): #does the transfer function on each node in the layer
    temp_li = []
    for x in input_li:
        center = evaluate(x, val)
        if center > 0:
            temp_li.append(x)
        elif center < 0:
            temp_li.append([0.01*y for y in x])
    return temp_li
def dot_product(xvals, weights, nextcount): #dot product function
    ret = []
    for i in range(nextcount):
        curr = [0]
        for j in range(len(xvals)):
            curr = polynomialAdd([weights[len(xvals)*i + j]*x for x in xvals[j]], curr)
        ret.append(curr)
    return ret
def feedForward(input_matrix, weights, val): #feed forward function
    counter = 0
    while counter < len(weights) - 1:
        input_matrix[counter+1] = transfer(dot_product(input_matrix[counter], weights[counter], len(weights[counter])//len(input_matrix[counter])), val)
        counter+=1
    input_matrix[counter+1] = dot_product(input_matrix[counter], weights[counter], len(weights[counter])//len(input_matrix[counter]))
    return input_matrix

def initialize_weights():
    weights = []
    layerCts = [2]
    for line in myVar:
        temp_li = []
        line_split = line.split(", ")
        for num in line_split:
            temp_li.append(float(num))
        weights.append(temp_li)
    for i in range(len(weights)):
        layerCts.append(int(len(weights[i])/layerCts[i]))
    return weights, layerCts


def findIntersect(line1, line2):
    return (line2[0] - line1[0]) / (line1[1] - line2[1])
def main():
    weights, layerCts = initialize_weights()
    print(layerCts)
    training_set = [[[1], [1]]]
    x_vals = [[[] for z in range(layerCts[i])] for i in range(len(layerCts))]

    x_vals[0][-1] = [1,0]

    for i in range(len(training_set)):
        inputs = training_set[i][0]
        for j in range(len(inputs)):
            x_vals[0][j] = [0, inputs[j]]

    
    # li = dot_product(x_vals[0], weights[0], layerCts[1])
    # points = []
    # for x in li:
    #     points.append((-1)*x[0] / x[1])
    # for y in points:
    #     clean_output(feedForward(x_vals, weights, y)[-1][0])
    # print(points)
    start = -1.5
    initial_poly = feedForward(x_vals, weights, start)[-1][0]

    start += 0.0001
    check = False
    poly = []
    poly_list = [initial_poly]
    point_list = [-1.5]

    while start < 1.5:
        poly = feedForward(x_vals, weights, start)[-1][0]
        # print(start)
        for i in range(len(poly)):
            if round(poly[i], 5) != round(initial_poly[i], 5):
                check = True
        if check:
            point = findIntersect(poly, initial_poly)
            poly_list.append(poly)
            initial_poly = poly.copy()
            point_list.append(point)
        check = False
        start += 0.0001
    print("Break Points:")
    for i in range(len(point_list)-1):
        print("(" + str(point_list[i]) + ", " + str(point_list[i+1]) + ") --> " + clean_output(poly_list[i]))
    print("(" + str(point_list[len(point_list)-1]) + ", " + str(1.5) + ") --> " + clean_output(poly_list[len(poly_list)-1]))
if __name__ == '__main__':
    main()

#Good weights:
# 1.6487164607022147, -0.33005663911000077, -3.4801134046594355, -2.2980634887810165, 0.36140779049461563, -1.0902587031923574, -1.863287178012149, -0.3602413641357084, 3.2929920716106755, -2.182287736923245
# 2.1481464835138735, -2.1550593225080688, 0.1262538380510728, 1.8539039866325449, -2.334080685863305, 0.5273692049135263, 2.8956079322031214, 0.8371687588154973, 0.48420948307048084, 3.099223137100227
# -3.6340475066207696, -4.173724146963986
# -5.661868574488944




#Kingsley Kim, 3
