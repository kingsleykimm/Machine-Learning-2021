import sys; args = sys.argv[1:]

import math, random, time
start_time = time.time()
# t_funct is symbol of transfer functions: 'T1', 'T2', 'T3', or 'T4'
# input is a list of input (summation) values of the current layer
# returns a list of output values of the current layer
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


def ff(ts, xv, weights, t_funct): #xv is a list of lists
    counter = 0
    while counter < len(weights) - 1:

        xv[counter+1] = transfer(t_funct, dot_product(xv[counter], weights[counter], len(weights[counter])//len(xv[counter])))
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

 



def main():

    input_string = args[0] 
    t_funct = 'T3' # we default the transfer(activation) function as 1 / (1 + math.e**(-x))
    if input_string[8] == '=': operator = input_string[7:9]
    else: operator = input_string[7:8]
    radius = float(input_string[9:len(input_string)])

    # training_set = []
    # for i in range(5000):
        
    #     x = round(random.uniform(-1.5, 1.5), 2)
    #     y = round(random.uniform(-1.5, 1.5), 2)
    #     if operator == ">=" or operator == ">":
    #         while (x*x+y*y) == radius ** 2:
    #             x = round(random.uniform(-1.5, 1.5), 2)
    #             y = round(random.uniform(-1.5, 1.5), 2)
    #     elif operator == "<=" or operator == "<":
    #         while (x*x+y*y) == radius ** 2:
    #             x = round(random.uniform(-1.5, 1.5), 2)
    #             y = round(random.uniform(-1.5, 1.5), 2)
    #     li = [x, y]
    #     if operator == ">=":
    #         if x*x+y*y >= radius ** 2: li.append(0.5)
    #         else: li.append(0)
    #     elif operator == "<=":
    #         if x*x+y*y <= radius**2: li.append(0.5)
    #         else: li.append(0)
    #     elif operator == "<":
    #         if x*x+y*y < radius**2: li.append(0.5)
    #         else: li.append(0)
    #     elif operator == '>':
    #         if x*x+y*y > radius ** 2: li.append(0.5)
    #         else: li.append(0)
    #     training_set.append(li)


   # training_set = [[float(x) for x in line.split() if x != '=>'] for line in open(file, 'r').read().splitlines() if line.strip() != '']
   # print (training_set) #[[1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [0.0, 0.0, 0.0]]
    layer_counts = [3, 9, 2, 1, 1]
    print ('layer counts', layer_counts) # This is the first output. [3, 2, 1, 1] with teh given x_gate.txt


    # x_vals = [[temp[0:len(temp)-1]] for temp in training_set] # x_vals starts with first input values
   #print (x_vals) # [[[1.0, -1.0]], [[-1.0, 1.0]], [[1.0, 1.0]], [[-1.0, -1.0]], [[0.0, 0.0]]]
   # make the x value structure of the NN by putting bias and initial value 0s.
    # for i in range(len(training_set)):
    #     for j in range(len(layer_counts)):
    #         if j == 0: x_vals[i][j].append(1.0)
    #         else: x_vals[i].append([0 for temp in range(layer_counts[j])])
    #     x_vals[i][-1] = [training_set[i][-1]]
   # print (x_vals) # [[[1.0, -1.0, 1.0], [0, 0], [0], [0]], [[-1.0, 1.0, 1.0], [0, 0], [0], [0]], ...

    # by using the layer counts, set initial weights [3, 2, 1, 1] => 3*2 + 2*1 + 1*1: Total 6, 2, and 1 weights are needed
    weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-1)]

    # build the structure of BP NN: E nodes and negative_gradients 
     # Whenever FF is done once, error will be updated. Start with 10 (a big num)
    # count how many times you trained the network, this can be used for index calc or for decision making of 'restart'
    alpha = 0.3
    momentum = 0
    # calculate the initail error sum. After each forward feeding (# of training sets), calculate the error and store at error list
    prev = []
    # for k in range(len(training_set)):
    #     x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
    #     # print(errors[k])
    #     E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp
    #     prev = [[negative_grad[i][j]*alpha for j in range(len(weights[i]))] for i in range(len(weights))]
    #     weights = update_weights(weights, negative_grad, alpha, prev, momentum)
    # err = sum(errors) #inital error sum

   # print(err)
   # while err > 1:
   #    weights = weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-1)]
   #    for k in range(len(training_set)):
   #       x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
   #       E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp
   #       weights = update_weights(weights, negative_grad, alpha)
   #    err = sum(errors)
    err = 10
    x_vals = []
    training_set = []
    E_vals = []
    negative_grad = []
    errors = []
    
    for count in range(2000000):
        alpha = 0.3
      # alpha = alpha_initial * (DROP ** (math.floor(count / DECAY)))
        # print(err)
        if count % 2 == 0: 
            for w in weights: print(w)
        # if (time.time() - start_time) > 95: 
        #     for w in weights: print(w)
        #     return
        # if err < 1: alpha = 3
        # if err < 0.5: alpha = 1
        # if err < 0.1: alpha = 0.5
        # if err < 0.05: alpha = 0.3
        #construct random point 
        print(err)
        training_set = []
        x = round(random.uniform(-1.5, 1.5), 2)
        y = round(random.uniform(-1.5, 1.5), 2)
        li = [x, y]
        temp_list = []
        temp_list.append(li)
        if operator == ">=" or operator == '>':
            if x*x+y*y >= radius ** 2: temp_list.append([1])
            else: temp_list.append([0])
        elif operator == "<=" or operator == '<':
            if x*x+y*y <= radius**2: temp_list.append([1])
            else: temp_list.append([0])
        

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
            x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
            err = sum(errors)
            if err > 0.3: alpha = 0.5
            E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp

            prev = [[negative_grad[i][j]*alpha for j in range(len(weights[i]))] for i in range(len(weights))]
            weights= update_weights(weights, negative_grad, alpha, prev, momentum)

            

      # for k in range(len(training_set)):
      #    x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct) 
      # err = sum(errors)
        # print(err)

        # if err > 0.1 and count == 10000 or err > 0.025 and count == 20000:
        #     weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-1)]
        #     E_vals = [[*i] for i in x_vals]  
        #     negative_grad = [[*i] for i in weights]  
        #     errors = [10]*len(training_set)  
 

        #     for k in range(len(training_set)):
        #        x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
        #        E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp
        #        prev = [[negative_grad[i][j]*alpha for j in range(len(weights[i]))] for i in range(len(weights))]
        #        weights = update_weights(weights, negative_grad, alpha, prev, momentum)
        #     for k in range(len(training_set)):
        #        x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct) 
        #     err = sum(errors)
    
      



    for w in weights: print(w)
if __name__ == '__main__': main()

#Kingsley Kim 3, 22