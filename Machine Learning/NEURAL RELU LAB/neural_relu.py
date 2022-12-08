import math






    #we know the inputs are x and y -- make two separate matrices defining those --- the bias will be added on later
    #one option -- make a modified x vals which is a 3d numpy array, that way you can have 2d numpy arrays in each one 


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
    print(s)
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
            temp_li.append([0.001*y for y in x])
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



def main():
    layerCts = [2, 5, 3, 1, 1]
    training_set = [[[1], [1]]]
    x_vals = [[[] for z in range(layerCts[i])] for i in range(len(layerCts))]

    x_vals[0][-1] = [1,0]

    for i in range(len(training_set)):
        inputs = training_set[i][0]
        for j in range(len(inputs)):
            x_vals[0][j] = [0, inputs[j]]
    input_val = float(input("What is the x value?"))
    weights =[[0.32819225623183373, -0.5534748602761296, -2.591866387973633, 0.11474385963363083, -4.888539225048593, -2.6053149350855933, 5.319595826747164, -1.9602285786552929],
                [1.0196026260792015, 1.9619140114981921, 5.480984600691452, 5.178765682367408, -0.7223953462498519, -1.0008794981904023, 0.14708809782715448, -0.6044324487016332],
                [-7.742775501927343, -0.1883837395006959],
                [-7.726372145804084]]

    x_vals = feedForward(x_vals, weights, input_val)
    print("Input value:", input_val)
    for x in x_vals:
        print(x)
    print("Network:")
    # for x in x_vals:
    #     output = []
    #     for li in x:
    #         output.append(evaluate(li, input_val))
    #     print(output)
    print("Final Polynomial:")
    clean_output(x_vals[-1][0])
if __name__ == '__main__':
    main()
#Looks like number of intervals is related to the 2nd layer
#For Weights: lyrCounts: [2, 5, 3, 1, 1]
# [[1.2062159010410753, -0.6620634006984781, -1.499757319038771, -0.4926178871864039, 0.9507095585087965, -0.7173073553087935, -0.901184144315221, -0.9293390256716465, 0.5009140839470628, -0.08290999662253094],
# [0.5038174876415445, 0.665485892627089, 0.41577471005679084, 1.0196818769013973, 0.8426062491618853, -0.2938998760515775, -0.43058617861516063, -0.526234997630081, -0.5776080328308502, 0.7652283166682888, 0.7038643286477225, 0.2722583478243556, 0.8460955698282739, 0.33984111611055273, -1.0451873530537654],
# [1.0452356099852342, 0.5667452184766932, 0.5253753812905689],
# [1.1582324656844731]]
#7/8 intervals
#(-1.5, -1.0): -1.8188587500072884 + -2.752405054832252x^{1}
#(-1.0, -0.4): -0.4811413735012004 + -1.4552146259562149x^{1}
#(-0.3, 0.2): 0.0008221943419850736 + 0.00045575034334788126x^{1}
#(0.2, 0.5): -0.12761175437972422 + 0.7613686189216023x^{1}
#(0.6, 0.8): -0.4037072679078048 + 1.2643881156530696x^{1}
#At 0.8: -0.5172365210756081 + 1.4148582667789158x^{1}
#(0.9, 1.0): -1.1170539562290152 + 2.101260477391223x^{1}
#(1, 1.5): -1.4510727235121383 + 2.409682707330537x^{1}

#For weights: Layer count [2, 4, 2, 1, 1]
# [0.32819225623183373, -0.5534748602761296, -2.591866387973633, 0.11474385963363083, -4.888539225048593, -2.6053149350855933, 5.319595826747164, -1.9602285786552929]
# [1.0196026260792015, 1.9619140114981921, 5.480984600691452, 5.178765682367408, -0.7223953462498519, -1.0008794981904023, 0.14708809782715448, -0.6044324487016332]
# [-7.742775501927343, -0.1883837395006959]
# [-7.726372145804084]
#(-1.5, -0.5): -0.841436473395255 + -1.9054462360023026x^{1}
#(-0.5, 0): 0.011971846416999206 + -0.3041350124714866x^{1}
#(0, 0.3): 9.971063332876483e-05 + -0.0025348493822844307x^{1}
#(0.4, 1.5): -0.6081756081600123 + 1.6461840444034221x^{1}
#Kingsley Kim, 3
