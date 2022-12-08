import math, random

numArms = 0
totalArr = list()
countArr = list()
def bandit(testNum, armIdx, pullVal):
    global totalArr
    global countArr
    global numArms

    if testNum == 0:
        numArms = armIdx
        totalArr = []
        countArr = []
        for i in range(numArms):
            totalArr.append(0)
            countArr.append(0)
        return random.choice(list(range(numArms)))

    elif testNum > 0:
        totalArr[armIdx] += 1
        countArr[armIdx] += pullVal
        c = 1.5
        epsilon = 1/testNum
         #might need to put this stuff after the if loop
        # if testNum <= 30:
        #     return random.choice(list(range(numArms)))
        # prob = random.random()
        # if prob < epsilon:
        #     temp = []
        #     for i in range(numArms):
        #         if i != armIdx:
        #             temp.append(i)
        #     return random.choice(temp)
        max = 0
        maxInd = 0
        for k in range(numArms):
            if totalArr[k] == 0:
                val = float('inf')
            else:
                val = countArr[k] / totalArr[k]
                val += c * math.sqrt(math.log10(testNum) / totalArr[k])
            if max < val:
                max = val
                maxInd = k  #how to stop from dividing by 0 at the start?
        
        return maxInd
        #testNum is what pull number is happening (between from 1 - 999) since it's 1000 pulls
        #armIndex is index number that was requested in prior call
        #pullVal is the value resulting from that pull
def main():
    # first_choice = bandit(0, 10, 0)
    # print(first_choice)
    # print(numArms)
    # print(bandit(1, first_choice, random.gauss(0,1)))
    # print([i for i in countArr])
    
    return

if __name__ == '__main__':
    main()
#Kingsley Kim 3, 22