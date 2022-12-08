import sys; args = sys.argv[1:]

import math, random


def transfer(t_funct, input):
   if t_funct == 'T3': return [1 / (1 + math.e**-x) for x in input]
   elif t_funct == 'T4': return [-1+2/(1+math.e**-x) for x in input]
   elif t_funct == 'T2': return [x if x > 0 else 0 for x in input]
   else: return [x for x in input]
def derv(t_funct, input):
   if t_funct == 'T3': return [ x(1-x) for x in input]
   elif t_funct == 'T4': return [(1-y*y)/2 for y in input]
   elif t_funct == 'T2': return [1 if x > 0 else 0 for x in input]
   else: return [1 for x in input]
# returns a list of dot_product result. the len of the list == stage
# dot_product([x1, x2, x3], [w11, w21, w31, w12, w22, w32], 2) => [x1*w11 + x2*w21 + x3*w31, x1*w12, x2*w22, x3*w32] 
def dot_product(input_list, weights, stage):
   return [sum([input_list[x]*weights[x+s*len(input_list)] for x in range(len(input_list))]) for s in range(stage)]

# Complete the whole forward feeding for one input(training) set
# return updated x_vals and error of the one forward feeding
def ff(xv, weights, t_funct): #xv is a list of lists

    ''' ff coding goes here '''
    counter = 0
    while counter < len(weights) - 1:
        xv[counter+1] = transfer(t_funct, dot_product(xv[counter], weights[counter], len(weights[counter])//len(xv[counter])))
        counter += 1 #dot product: first arg is 
    temp_list = []
    for i in range(len(xv[counter])):
        temp_list.append(xv[counter][i]*weights[counter][i])
    # xv[counter+1] = dot_product(xv[counter], weights[counter], len(weights[counter])//len(xv[counter]))
    xv[counter+1] = temp_list
    return xv


# Complete the back propagation with one training set and corresponding x_vals and weights
# update E_vals (ev) and negative_grad, and then return those two lists
def bp(ts, xv, weights, ev, negative_grad):   

    ''' bp coding goes here '''
    counter = len(weights) - 1
    for i in range(len(ts[-1])):
        ev[-1][i] = ts[-1][i]-xv[-1][i]

    temp_list_2 = []
    for i in range(len(ev[counter+1])):
        temp_list_2.append(ev[counter+1][i] * xv[counter][i])

    negative_grad[counter] = temp_list_2
    
    for i in range(len(ts[-1])):
        ev[counter][i] = ev[counter+1][i] * xv[counter][i] * (1 - xv[counter][i]) * weights[counter][i]

    counter -= 1
    while counter > -1:
        temp_list = []
        for e in ev[counter+1]:
            for x in xv[counter]:
                temp_list.append(e*x)
        negative_grad[counter] = temp_list  #negative gradient list construction
        temp_list_2 = []
        if counter != 0: #E = E(layer+1)x(layer)(1-x)weights
            for i in range(len(xv[counter])):
                temp_list_2.append(sum(
                                 dot_product(ev[counter+1], weights[counter][i:len(weights[counter]):len(xv[counter])], 
                                    1)) * xv[counter][i] * (1-xv[counter][i]))
             #error values list construction
            ev[counter] = temp_list_2
        counter -= 1
    return ev, negative_grad

# update all weights and return the new weights
# Challenge: one line solution is possible
def update_weights(weights, negative_grad, alpha, prev, momentum):
      #equation for updating weights: new weight = negative grad * alpha + old weight
    
    return [[negative_grad[i][j] * alpha + weights[i][j] + momentum * prev[i][j] for j in range(len(weights[i]))]for i in range(len(weights))]

 

#one way to help error converging: ditch the neural network
def construct_xvals(layer_counts):
    x_vals = [[] for x in range(len(layer_counts))]
    for i in range(len(layer_counts)):
        x_vals[i] = [0.0 for temp in range(layer_counts[i])]
    x_vals[0][-1] = 1.0
    return x_vals
def main():

    training_set = [[0, 0, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0], [1, 1, 0, 1], [0, 0, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 1, 1]]
    t_funct = 'T3'
   # by using the layer counts, set initial weights [3, 2, 1, 1] => 3*2 + 2*1 + 1*1: Total 6, 2, and 1 weights are needed
    # weights = [[0.29, 0.6, 0.7, -0.06, 0.96, -0.82, 1.34, 1.32], [1.59, -0.81, -0.63, 0.35], [0.39, -2.0]]
    layer_counts = [4, 3, 2, 2]
    x_vals = construct_xvals(layer_counts)
    
    # print final weights of the working NN
    weights = [[-3.971735728445723, -3.9717415178780433, -3.9717349322208952, 1.6119474697056364, -6.245030598028172, -6.244982957903095, -6.244993830250422, 9.06863040743561, -3.0126233318503393, -3.012656831868249, -3.012643536785527, 7.404790494650706], 
                [-2.6355750817540415, -6.946359781924163, 0.35204903968063733, -7.638927128756968, 8.598922060221636, -9.046911097884067], 
                [1.9446663020722612, 5.387053096887867]]
    num1 = args[0]
    num2 = args[1]
    if len(num1) < len(num2):
        while len(num1) < len(num2):
            num1 = '0' + num1
    elif len(num2) < len(num1):
        while len(num2) < len(num1):
            num2 = '0' + num2
    final = ""
    carry = 0
     #[[0.0, 0.0, 0.0, 1.0], [0, 0], [0, 0], [0, 0]]
    for i in range(len(num1)-1, -1, -1):
        x_vals = construct_xvals(layer_counts)
        x_vals[0][1] = int(num1[i])
        x_vals[0][2] = int(num2[i])
        x_vals[0][0] = carry
        li = [x_vals[0][0], x_vals[0][1], x_vals[0][2]]
        out = ff(x_vals, weights, t_funct)
        carry = out[-1][0]
        print(carry)
        if out[-1][1] > 0.5:
            final += '1'
        elif out[-1][1] <= 0.5:
            final += '0'
        
    if carry > 0.5:
        final += '1'
    elif carry <= 0.5:
        final += '0'
    final = final[::-1]
    print(final)
if __name__ == '__main__': main()

#Kingsley Kim 3, 22