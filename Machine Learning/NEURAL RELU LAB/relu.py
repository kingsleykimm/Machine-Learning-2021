import sys; args = sys.argv[1:]

import math, random, time
start_time = time.time()
# t_funct is symbol of transfer functions: 'T1', 'T2', 'T3', or 'T4'
# input is a list of input (summation) values of the current layer
# returns a list of output values of the current layer
def transfer(input_list):
    return [0.01*x if x < 0 else x for x in input_list]
def derv(input):
    if input > 0:
        return 1
    elif input < 0:
        return 0.01
    else:
        return 1/2
# returns a list of dot_product result. the len of the list == stage
# dot_product([x1, x2, x3], [w11, w21, w31, w12, w22, w32], 2) => [x1*w11 + x2*w21 + x3*w31, x1*w12, x2*w22, x3*w32] 
def dot_product(input_list, weights, stage):
   return [sum([input_list[x]*weights[x+s*len(input_list)] for x in range(len(input_list))]) for s in range(stage)]
def initialize_weights(layer_counts):
    return [[round(random.uniform(-1*math.sqrt(2.0 / layer_counts[i]), math.sqrt(2.0 / layer_counts[i])), 2) 
                    for j in range(layer_counts[i]*layer_counts[i+1])] for i in range(len(layer_counts)-1)]

def ff(ts, xv, weights): #xv is a list of lists
    counter = 0
    while counter < len(weights) - 1:
        xv[counter+1] = transfer(dot_product(xv[counter], weights[counter], len(weights[counter])//len(xv[counter])))
        counter += 1 #dot product: first arg is 
    temp_list = []
    for i in range(len(xv[counter])):
        temp_list.append(xv[counter][i]*weights[counter][i])
    # xv[counter+1] = dot_product(xv[counter], weights[counter], len(weights[counter])//len(xv[counter]))
    xv[counter+1] = temp_list
    err = 0
    for i in range(len(ts[-1])):
       err += (ts[-1][i]- xv[-1][i]) ** 2
    err = err / 2
    return xv, err
def bp(ts, xv, weights, ev, negative_grad):   

    counter = len(weights) - 1
    for i in range(len(ts[-1])):
        ev[-1][i] = ts[-1][i]-xv[-1][i]
    temp_list_2 = []
    for i in range(len(ev[counter+1])):
        temp_list_2.append(ev[counter+1][i] * xv[counter][i])
    negative_grad[counter] = temp_list_2
    for i in range(len(ts[-1])):
        ev[counter][i] = ev[counter+1][i] * xv[counter][i] * derv(xv[counter][i]) * weights[counter][i]
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
                                    1)) * derv(xv[counter][i]))
             #error values list construction
            ev[counter] = temp_list_2
        counter -= 1
    return ev, negative_grad
# update all weights and return the new weights
# Challenge: one line solution is possible
def update_weights(weights, negative_grad, alpha, prev, momentum):
      #equation for updating weights: new weight = negative grad * alpha + old weight
    return [[negative_grad[i][j] * alpha + weights[i][j] + momentum * prev[i][j] for j in range(len(weights[i]))]for i in range(len(weights))]

 



def main():
    layer_counts = [2, 4, 2, 1, 1]
    print ('layer counts', layer_counts) # This is the first output. [3, 2, 1, 1] with teh given x_gate.txt


    weights = initialize_weights(layer_counts)

    # build the structure of BP NN: E nodes and negative_gradients 
     # Whenever FF is done once, error will be updated. Start with 10 (a big num)
    # count how many times you trained the network, this can be used for index calc or for decision making of 'restart'
    alpha = 0.3
    momentum = 0
    # calculate the initail error sum. After each forward feeding (# of training sets), calculate the error and store at error list
    prev = []
    err = 10
    x_vals = []
    training_set = []
    E_vals = []
    negative_grad = []
    errors = []
    
    for count in range(1000000):
        alpha = 0.1
      # alpha = alpha_initial * (DROP ** (math.floor(count / DECAY)))
        # if count % 1000 == 0:
        #     for w in weights:
        #         print(w)

        # if (time.time() - start_time) > 95: 
        #     for w in weights: print(w)
        #     return
        # if err < 1: alpha = 3
        # if err < 0.5: alpha = 1
        # if err < 0.1: alpha = 0.5
        # if err < 0.05: alpha = 0.3
        #construct random point 

        training_set = []
        x = round(random.uniform(-1.5, 1.5), 2)

        li = [x]
        temp_list = []
        temp_list.append(li)
        temp_list.append([x**2])
        training_set.append(temp_list)
        x_vals = [temp[0:len(temp)-1] for temp in training_set]
    # x_vals = [temp[0:len(temp)-1] for temp in training_set]
        for i in range(len(training_set)):
            for j in range(len(layer_counts)):
                if j == 0: x_vals[i][j].append(1.0)
                else: x_vals[i].append([0 for temp in range(layer_counts[j])])
        E_vals = [[*i] for i in x_vals]  #copy elements from x_vals, E_vals has the same structures with x_vals
        negative_grad = [[*i] for i in weights]  #copy elements from weights, negative gradients has the same structures with weights
        errors = [10]*len(training_set) 

        for k in range(len(training_set)):
            x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights)
            err = sum(errors)
            if err > 0.3: alpha = 0.5
            E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp

            prev = [[negative_grad[i][j]*alpha for j in range(len(weights[i]))] for i in range(len(weights))]
            weights= update_weights(weights, negative_grad, alpha, prev, momentum)

            



    for w in weights: print(w)
    training_set = []
    x = round(random.uniform(-1.5, 1.5), 2)
    li = [x]
    temp_list = []
    temp_list.append(li)
    temp_list.append([x**2])
    training_set.append(temp_list)
    x_vals = [temp[0:len(temp)-1] for temp in training_set]
# x_vals = [temp[0:len(temp)-1] for temp in training_set]
    for i in range(len(training_set)):
        for j in range(len(layer_counts)):
            if j == 0: x_vals[i][j].append(1.0)
            else: x_vals[i].append([0 for temp in range(layer_counts[j])])
    print(ff(training_set[0], x_vals[0], weights))
if __name__ == '__main__': main()

#Kingsley Kim 3, 22