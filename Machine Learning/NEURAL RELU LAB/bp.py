import sys; args = sys.argv[1:]
myVar = open(args[0], 'r').read().splitlines()
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
def ff(ts, xv, weights, t_funct): #xv is a list of lists

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
    err = 0
    for i in range(len(ts[-1])):
       err += (ts[-1][i]- xv[-1][i]) ** 2
    err = err / 2
    return xv, err


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

def main():


    t_funct = 'T3' # we default the transfer(activation) function as 1 / (1 + math.e**(-x))
    training_set = []; ind = 0
    for line in myVar:
        if line.strip() != '':
            line = line.strip()
            line = line.split()
            temp_list = []
            ind = line.index('=>')
            for i in range(0, ind):
                if line[i] == ' ': continue
                temp_list.append(float(line[i]))
            temp_list_2 = []

            for j in range(ind+1, len(line)):
                if line[j] == ' ': continue
                temp_list_2.append(float(line[j]))
            temp_list_3 = [temp_list, temp_list_2]

            training_set.append(temp_list_3)  


    # training_set = [[float(x) for x in line.split() if x != '=>'] for line in myVar if line.strip() != '']
   # print (training_set) #[[1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [0.0, 0.0, 0.0]]
   #new training set format [[[1.0, 0.0, 1.0], [0.0, 1.0]], [[1.0, 0.0, 1.0], [1.0]],  ]

    if len(training_set[-1][1]) == 2: layer_counts = [len(training_set[0][0])+1, 2, 2, 2]
    else: layer_counts = [len(training_set[0][0])+1, 2, 1, 1]
    print ('layer counts', layer_counts) # This is the first output. [3, 2, 1, 1] with teh given x_gate.txt

    x_vals = []
    for ts in training_set:
        x_vals.append(ts[0:len(ts)-1])
    # x_vals = [temp[0:len(temp)-1] for temp in training_set]
    for i in range(len(training_set)):
      for j in range(len(layer_counts)):
            if j == 0: x_vals[i][j].append(1.0)
            else: x_vals[i].append([0 for temp in range(layer_counts[j])])

    weights = []
   # by using the layer counts, set initial weights [3, 2, 1, 1] => 3*2 + 2*1 + 1*1: Total 6, 2, and 1 weights are needed
    # weights = [[0.29, 0.6, 0.7, -0.06, 0.96, -0.82, 1.34, 1.32], [1.59, -0.81, -0.63, 0.35], [0.39, -2.0]]
    if layer_counts[-1] == 1:
        weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-1)]
    else:
        weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
        temp_list = []
        for i in range(layer_counts[-1]):
            temp_list.append(round(random.uniform(-2.0, 2.0), 2))
        weights.append(temp_list)

    
    E_vals = [[*i] for i in x_vals]  
    negative_grad = [[*i] for i in weights] 
    errors = [10]*len(training_set)  
    count = 1  
    alpha = 0.1
    momentum = 0.3
    # return 
   # calculate the initail error sum. After each forward feeding (# of training sets), calculate the error and store at error list
    prev = []
    for k in range(len(training_set)):
        x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
        # print(errors[k])
        E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp
        prev = [[negative_grad[i][j]*alpha for j in range(len(weights[i]))] for i in range(len(weights))]
        weights= update_weights(weights, negative_grad, alpha, prev, momentum)
    for k in range(len(training_set)):
        x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
    err = sum(errors) 

    # while err > 1: 
    #     if layer_counts[-1] == 1:
    #         weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-1)]
    #     else:
    #         weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
    #         temp_list = []
    #         for i in range(layer_counts[-1]):
    #             temp_list.append(round(random.uniform(-2.0, 2.0), 2))
    #         weights.append(temp_list)
    #     for k in range(len(training_set)):
    #         x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
    #     # print(errors[k])
    #         E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp

    #         weights = update_weights(weights, negative_grad, alpha)

    #     for k in range(len(training_set)):
    #         x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
    #     err = sum(errors) 

    temp_err_1 = sum(errors); temp_err_2 = 0; count = 1

    while err > 0.01*math.sqrt(len(training_set)) and count <= 100000:

        for k in range(len(training_set)):
            x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
            E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp
            prev = [[negative_grad[i][j]*alpha for j in range(len(weights[i]))] for i in range(len(weights))]
            weights= update_weights(weights, negative_grad, alpha, prev, momentum)
        for k in range(len(training_set)):
            x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
        err = sum(errors)
        if count % 2 == 0: temp_err_1 = sum(errors)
        else: temp_err_2 = sum(errors)

        # if err > 0.1 and count == 10000 or err > 0.025 and count == 20000:
        if abs(temp_err_1 - temp_err_2) < 0.000001:
            # print(errors); print(x_vals[1]); print(E_vals[1]); print(weights); print(negative_grad); return
            training_set = []; ind = 0
            for line in myVar:
                if line.strip() != '':
                    line = line.strip()
                    line = line.split()
                    temp_list = []
                    ind = line.index('=>')
                    for i in range(0, ind):
                        if line[i] == ' ': continue
                        temp_list.append(float(line[i]))
                    temp_list_2 = []

                    for j in range(ind+1, len(line)):
                        if line[j] == ' ': continue
                        temp_list_2.append(float(line[j]))
                    temp_list_3 = [temp_list, temp_list_2]

                    training_set.append(temp_list_3)  
            # print("DSKFHJSDFHKSDHFKSDJFHSDKJFHSKDJFHSDKJFHSDKHJFHSDKJF")

            x_vals = []
            x_vals = [temp[0:len(temp)-1] for temp in training_set]
            for i in range(len(training_set)):
                for j in range(len(layer_counts)):
                    if j == 0: x_vals[i][j].append(1.0)
                    else: x_vals[i].append([0 for temp in range(layer_counts[j])])


        # by using the layer counts, set initial weights [3, 2, 1, 1] => 3*2 + 2*1 + 1*1: Total 6, 2, and 1 weights are needed

            if layer_counts[-1] == 1:
                weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-1)]
            else:
                weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-2)]
                temp_list = []
                for i in range(layer_counts[-1]):
                    temp_list.append(round(random.uniform(-2.0, 2.0), 2))
                weights.append(temp_list)

            
            E_vals = [[*i] for i in x_vals]  
            negative_grad = [[*i] for i in weights]  
            errors = [10]*len(training_set)  
            count = 1  
            alpha = 0.1
            temp_err_1 = sum(errors); temp_err_2 = 0; count = 1

            for k in range(len(training_set)):
                x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)

                E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp
                prev = [[negative_grad[i][j]*alpha for j in range(len(weights[i]))] for i in range(len(weights))]

                weights = update_weights(weights, negative_grad, alpha, prev, momentum)
            for k in range(len(training_set)):
                x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
            # print(x_vals); print(E_vals); 
            err = sum(errors)

        

            

        

     
        count += 1
        print(err)
    for w in weights:
        print(w)
    # print final weights of the working NN
    weights = [[-6.133831805457579, -6.13344096024769, -6.133277323953907, 8.987286090140312, -1.3998732391012583, -1.403109566608535, -1.399703509635396, 2.2095711925756087],
                [7.039245723835456, -11.620076324335129, -5.138846535176057, 0.6520600374786573],
                [4.941916326829336, 1.9467442464168725]]
    
        
if __name__ == '__main__': main()

#Kingsley Kim 3, 22