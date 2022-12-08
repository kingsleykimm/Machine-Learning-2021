import sys; args = sys.argv[1:]
#Tae Ha Kim
import math


def transfer(t_funct, input):
    ret_list = []
    for i in range(len(input)):
        summation = sum(input[i])
        if t_funct == 'T1':
            ret_list.append(summation)
        elif t_funct == 'T2':
            if summation > 0:
                ret_list.append(summation)
            else:
                ret_list.append(0.0)
        elif t_funct == 'T3':
            ret_list.append((1 + math.e ** (-1*summation)) ** (-1))
        elif t_funct == 'T4':
            ret_list.append(((1 + math.e ** (-1*summation)) ** (-1))*2-1)
    return ret_list

def dot_product(input, weights, stage):
    ret_list = []
    for i in range(stage):
        sub_list = []
        for j in range(len(input)):
            sub_list.append(input[j]*weights[i*len(input)+j])
        ret_list.append(sub_list)
    return ret_list

def evaluate(file, input_vals, t_funct):
    input_file = open(file)
    weights = []
    counter = 0
    for val in input_vals:
        val = float(val)
    for line in input_file.readlines():
        line_split = line.strip('\n').split(' ')
        sub_list = []
        for num in line_split:
            sub_list.append(float(num))
        weights.append(sub_list) #0 index is 0 layer's weights
    #for dot product, pass weights as layer
    while counter < len(weights) - 1:
        input_vals = transfer(t_funct, 
                        dot_product(input_vals, weights[counter], len(weights[counter])//len(input_vals)))
        counter += 1
    #last run of dot product
    input_vals = dot_product(input_vals, weights[len(weights)-1], len(weights[len(weights)-1])//len(input_vals))
    
    return input_vals


def main():

   file, inputs, t_funct, transfer_found = '', [], 'T1', False
   for i in range(len(args)):
      if i == 0:
         file = args[i]
      elif not transfer_found:
         t_funct, transfer_found = args[i], True
      else:
         inputs.append(float(args[i]))
   if len(file)==0: exit("Error: Weights file is not given")
   li =(evaluate(file, inputs, t_funct))
   for x in li:
      print (x, end=' ')
if __name__ == '__main__': main()