def flip_pancakes(stack):

    sortedStack = sorted(stack)
    flippityDoo = []
    #abbaba = [1,2,4,5]
    #print(abbaba[len(abbaba)-1:len(abbaba)])

    while(sortedStack!=stack):
    #for i in [1,2]:
        offfset = excludeCorrectBase(stack)
        print("original stack: " )
        print(stack)
        #ignore previously sorted numbers
        stackToSort = stack[0:(len(stack)-offfset)]
        #find highest number in to sort stack
        maxInt = max(stackToSort)
        #print(maxInt)
        #flip stack from that index
        flipAt = stackToSort.index(maxInt)
        if type(flipAt) is not int:
            flipAt= flipAt[1]
        
        if flipAt > 0:
            flippityDoo.append(flipAt)
            print(f"\t 1flipping at {flipAt}")
            partA = stackToSort[0:flipAt+1]
            print("flipping this part")
            print(partA)        
            partA = invertList(partA)
            stackOut = partA
            partB = stackToSort[flipAt+1:len(stackToSort)]
            stackOut.extend(partB)
        else:
            stackOut = stackToSort
            flippityDoo.append(len(stackToSort)-1)
            print(f"\t 2flipping at {len(stackToSort)-1}")
        
        
        print("new stack: ")
        print(stackOut)
        
        stackOut = invertList(stackOut)
        partC = stack[len(stack)-offfset:len(stack)]
        
        append3 = len(stackOut)-1
        

        stackOut.extend(partC)
        print("fully flipped")
        print(stackOut)
        stack = stackOut
        print("-------")
        print("fully flipped")
        
        if stack != sortedStack:
            flippityDoo.append(append3)
            print(f"\t 3flipping at {append3}")
        
        #stack = invertList(stackOut[0:len(stackOut-i)])
        #outB = stackOut[len(stackOut-i):stackOut]
        #stack = outA.extend(outB)
    
    return flippityDoo


# find largest
# flip stack up until the largest number found - puts largest number at the start
# flip whole stack - puts lares tnumber at the back
# flip stack up until the largest number found (excluding last value)

def invertList(listIn):
    invertedList = []
    for i in range(len(listIn)):
        invertedList.append(listIn[len(listIn)-i-1])
    return invertedList

def excludeCorrectBase(offsetInput):
    length = len(offsetInput)
    sortedList = sorted(offsetInput)
    offset = 0
    while offsetInput[length-offset:length] == sortedList[length-offset:length]:
        offset+=1
    offset -=1
    print(f"\toffset: {offset}")
    return offset


instr = [1,5,8,3]
#instr = [1,2,3,4]
#instr = [1,99, 7 , 5, 8, 21]
print(flip_pancakes(instr))



#desired: [1,2,3,4]
# [3, 2, 1, 4]