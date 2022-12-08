import sys; args = sys.argv[1:]
import math
def main():
    sizeSpec = int(args[0]) #width is after the size
    width = args[1]
    real_width = 0
    width_check = True
    grid = []
    for i in range(len(width)):
        if width[i] in "RGB":
            width_check = False #checks if 2nd argument is R, G, B or number
    if width_check == False: #no second width argument, need to find own
        if sizeSpec == 1:
            real_width = 1
        else:
            for i in range(math.ceil(math.sqrt(sizeSpec)), sizeSpec):

                if sizeSpec & i == 0:
                    real_width = i
                    break
        height = sizeSpec // real_width
        for i in range(height):
            for j in range(real_width):
                sample = {"reward": 0, "N": False, "W": False, "E": False, "S": False}
                grid.append(sample)
    else: #case where there is a second width argument
        width = int(args[1])
        for i in range(height):
            for j in range(width):
                sample = {"reward": 0, "N": False, "W": False, "E": False, "S": False}
                grid.append(sample)

    rewards = []
    barriers = []
    neighbors = []
    goal = 0
    reward = 0
    start = 0
    reward_found = False #need to check if a reward is there and set the default to 12
    if width_check == False:
        start = 1
    else:
        start = 2

    for i in range(start, len(args)):
        if "R" in args[i]:
            if len(args[i]) == 3: #R:# sets the reward number
                reward = int(args[i][2])
                reward_found = True
            elif len(args[i]) == 2: # R# case
                if reward_found == False:
                    grid[int(args[i][1])]['reward'] = 12
                else:
                    grid[int(args[i][1])]['reward'] = reward
            elif len(args[i]) == 4:
                grid[int(args[i][1])]['reward'] = int(args[i][3]) #R#:# case
        elif "G" in args[i]:
            if "0" in args[i]:
                goal = 0
            if "1" in args[i]:
                goal = 1
        elif "B" in args[i]: #need to flip these from existing booleans 
            if len(args[i]) == 2:
                grid[int(args[i][1])]['N'] = not grid[int(args[i][1])]['N']
                grid[int(args[i][1])]['W'] = not grid[int(args[i][1])]['W']
                grid[int(args[i][1])]['E'] = not grid[int(args[i][1])]['E']
                grid[int(args[i][1])]['S'] = not grid[int(args[i][1])]['S']
            elif len(args[i]) > 2:
                pos = int(args[i][1])
                for j in range(2, len(args[i])):
                    dire = args[i][j]
                    grid[pos][dire] = not grid[pos][dire]
    #bfs section

    

            

    # #####
    # #####
    # #####
    # #####

    # return

if __name__ == '__main__':
    main()
#Kingsley Kim 3, 22