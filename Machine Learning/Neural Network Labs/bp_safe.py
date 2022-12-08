import sys; args = sys.argv[1:]
myVar = open(args[0], 'r').read().splitlines()
import math, random

#possible fixes: Leaky RELU
#Kaiming-He weight initialization - could initialize weights so they take on values per a normal distribution centered @0 with st.dev sqrt(2/n), n is #of nodes feeding n
#uniform distribution between ±sqrt(2/n)
def transfer(t_funct, input_list):
    return [0.001*x if x < 0 else x for x in input_list]
def derv(t_funct, input):
    if input > 0:
        return 1
    elif input < 0:
        return 0.001
    else:
        return 0.1
def initialize_weights(layer_counts):
    return [[round(random.gauss(0, math.sqrt(2.0/layer_counts[i])), 2) 
                    for j in range(layer_counts[i]*layer_counts[i+1])] for i in range(len(layer_counts)-1)]
    
# returns a list of dot_product result. the len of the list == stage
# dot_product([x1, x2, x3], [w11, w21, w31, w12, w22, w32], 2) => [x1*w11 + x2*w21 + x3*w31, x1*w12, x2*w22, x3*w32] 
def dot_product(input, weights, stage):
    return [sum([input[x]*weights[x+s*len(input)] for x in range(len(input))]) for s in range(stage)]

# Complete the whole forward feeding for one input(training) set
# return updated x_vals and error of the one forward feeding
def ff(ts, xv, weights, t_funct):

   ''' ff coding goes here '''
   counter = 0
   while counter < len(weights) - 1:

      xv[counter+1] = transfer(t_funct, dot_product(xv[counter], weights[counter], len(weights[counter])//len(xv[counter])))
      counter += 1
   xv[counter+1] = dot_product(xv[counter], weights[counter], len(weights[counter])//len(xv[counter]))
   err = (ts[-1] - xv[-1][0])**2 / 2
   return xv, err


# Complete the back propagation with one training set and corresponding x_vals and weights
# update E_vals (ev) and negative_grad, and then return those two lists
def bp(ts, xv, weights, ev, negative_grad):   

    ''' bp coding goes here '''

    ev[len(xv)-1] = [(ts[-1]-xv[-1][0])]
    counter = len(weights)-1
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
                                    1)) * derv('T3', xv[counter][i]))
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
    file1 = open(args[0], 'w')
    for i in range(15):
        num = round(random.uniform(-1.5, 1.5), 2)
        string = str(num) + " => " + str(num**2) + "\n"
        file1.write(string)

    t_funct = 'T0' # we default the transfer(activation) function as 1 / (1 + math.e**(-x))
    training_set = [[float(x) for x in line.split() if x != '=>'] for line in myVar if line.strip() != '']

   # print (training_set) #[[1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [0.0, 0.0, 0.0]]
   #new training set format [[[1.0, 0.0, 1.0], [0.0, 1.0]], [[1.0, 0.0, 1.0], [1.0]],  ]
    # if len(training_set[-1][1]) == 2: layer_counts = [len(training_set[0]), 3, 2, 2]
    layer_counts = [len(training_set[0]), 5, 3, 1, 1]
    print ('layer counts', layer_counts) # This is the first output. [3, 2, 1, 1] with teh given x_gate.txt
    x_vals = [[temp[0:len(temp)-1]] for temp in training_set]
    for i in range(len(training_set)):
      for j in range(len(layer_counts)):
            if j == 0: x_vals[i][j].append(1.0)
            else: x_vals[i].append([0 for temp in range(layer_counts[j])])
   # by using the layer counts, set initial weights [3, 2, 1, 1] => 3*2 + 2*1 + 1*1: Total 6, 2, and 1 weights are needed
    # weights = [[round(random.uniform(-2.0, 2.0), 2) for j in range(layer_counts[i]*layer_counts[i+1])]  for i in range(len(layer_counts)-1)]
    weights = initialize_weights(layer_counts)
    E_vals = [[*i] for i in x_vals]  
    negative_grad = [[*i] for i in weights]  
    errors = [10]*len(training_set)  
    count = 1  
    alpha = 0.1
    momentum = 0.25
    prev = []
   # calculate the initail error sum. After each forward feeding (# of training sets), calculate the error and store at error list
    for k in range(len(training_set)):
        x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
        E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp
        prev = [[negative_grad[i][j]*alpha for j in range(len(weights[i]))] for i in range(len(weights))]
        weights= update_weights(weights, negative_grad, alpha, prev, momentum)
    for k in range(len(training_set)):
        x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
    err = sum(errors)
    

    temp_err_1 = sum(errors); temp_err_2 = 0; count = 1
    
    while err > 0.005*math.sqrt(len(training_set)) and count <= 100000:
        print(err)
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
        
        if (count == 20000 and err > 0.05) or abs(temp_err_1 - temp_err_2) < 0.00001: 
            # print("DSKFHJSDFHKSDHFKSDJFHSDKJFHSKDJFHSDKJFHSDKHJFHSDKJF")
            x_vals = [[temp[0:len(temp)-1]] for temp in training_set]
            for i in range(len(training_set)):
                for j in range(len(layer_counts)):
                    if j == 0: x_vals[i][j].append(1.0)
                    else: x_vals[i].append([0 for temp in range(layer_counts[j])])
            E_vals = [[*i] for i in x_vals]  
            negative_grad = [[*i] for i in weights]  
            errors = [10]*len(training_set)  
            temp_err_1 = sum(errors); temp_err_2 = 0; count = 1
            weights = initialize_weights(layer_counts)
            for k in range(len(training_set)):
                x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
                E_vals[k], negative_grad = bp(training_set[k], x_vals[k], weights, E_vals[k], negative_grad) #bp
                prev = [[negative_grad[i][j]*alpha for j in range(len(weights[i]))] for i in range(len(weights))]
                weights= update_weights(weights, negative_grad, alpha, prev, momentum)
            for k in range(len(training_set)):
                x_vals[k], errors[k] = ff(training_set[k], x_vals[k], weights, t_funct)
            err = sum(errors)

       
        

     
        count += 1

    # print final weights of the working NN

    for w in weights: print (w)
    
if __name__ == '__main__': main()

#Kingsley Kim 3, 22


