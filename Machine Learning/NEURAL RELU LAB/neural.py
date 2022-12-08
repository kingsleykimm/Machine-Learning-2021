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
    return [transferFunc(x, val) for x in input_li]
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
    weights =[[-7.8293075277441995, 0.3647667960307226, 7.834873911142444, 0.3585560036142447, 0.009909195465335825, 4.113380568804637, 2.2167529885027473, -2.354275496207227, -2.172695210725063, -2.3273632100258053],
            [16.207315946599063, 16.2522672085926, -9.089853295510135, -6.9557997618177065, -6.980299609189942, -5.623260408174482, -5.615112289239223, 6.092116788512558, 4.784652071035457, 4.853785538939241],
            [-13.212046948717454, 13.021903635304557],
            [3.2346395341361944]]
    x_vals = feedForward(x_vals, weights, input_val)
    print("Input value:", input_val)
    print("Network:")
    for x in x_vals:
        output = []
        for li in x:
            output.append(evaluate(li, input_val))
        print(output)
    print("Final Polynomial:")
    clean_output(x_vals[-1][0])
if __name__ == '__main__':
    main()
#Kingsley Kim, 3
