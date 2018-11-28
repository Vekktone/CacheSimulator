import sys, math, time

cacheSim=[]
numCacheLines = 0
numSets = 0
cachLinesPerSet = 0

memAddressSize = 0
offset = 0
setIndex = 0
tag = 0

def printCache(cacheSim):
    for i in range(numCacheLines):
        print("cachSim[", i, "]: ", cacheSim[i])

   
def createCache(cacheSize, cacheLineSize, numWays):
    
    global numCacheLines
    global numSets
    global cacheLinesPerSet

    global offset
    global setIndex
    global tag
    global memAddressSize
    global cacheSim
    global queue

    #need to determine if cacheSize is in MB, KB, or B, for now
    #assume all values are in bytes
    numCacheLines = cacheSize//cacheLineSize
    numSets = numCacheLines//numWays
    cacheLinesPerSet = numCacheLines//numSets
 
    #print out metrics
    print("cacheSize: ", cacheSize, " bytes")
    print("cacheLineSize: ", cacheLineSize, " bytes")
    print("numCacheLines: ", numCacheLines)
    print("numSets: ", numSets)
    print("numWays: ", numWays)
    print("The cache consists of ", numSets, " sets each consisting of numCacheLines/numSets: ", cacheLinesPerSet, " cache Lines.")
    print()
    print("The memory address is partitioned into 3 parts: tag, set index, and offset")
    
    memAddressSize = 12
    offset = math.ceil(math.log(cacheLineSize, 2))
    setIndex = math.ceil(math.log(numSets, 2))
    tag = memAddressSize - (offset + setIndex)
    print("Offset is s bits based on cache line size: s =", offset)
    print("Set index is t bits based on number of sets: t =", setIndex)
    print("Tag has remaining bits: tag =", tag)
    #create cache array and fill with all zeros
    for i in range(numCacheLines):
        cacheSim.append([0,0,0,0,0,-1])

    #initialize the set values accordingly
    lineCounter = 0
    setNumber = 0
    wayNumber = 0
    for i in range(numCacheLines):
        if (lineCounter == cacheLinesPerSet):
            lineCounter = 0
            setNumber = setNumber + 1
            wayNumber = 0
        cacheSim[i][0] = setNumber
        cacheSim[i][1] = wayNumber
        cacheSim[i][2] = "-1"
        cacheSim[i][4] = "-1"
        lineCounter = lineCounter + 1
        wayNumber = wayNumber + 1

#Main method
print("This is a cache simulator")

#createCache(256, 64, 2)
#createCache(4096, 128, 4)
#createCache((1*1024), 64, 16)
createCache((4*1024*1024), 4, 16)

#printCache(cacheSim)

print()
accessCount = 0
missCount = 0
addrCount = 0;
file = open(sys.argv[1], "r")
while True:
    inputLine = file.readline()
    #check if we need to read or write to cache if line is populated 
    if inputLine == "":
        break
    rw = inputLine.split()
    ReadWrite = rw[1]
    # to get R or W
    accessCount = accessCount + 1
    addrCount = addrCount + 1

    #calculate specific metric for each address, save into variables
    memFields = inputLine.split()
    print("addrCount =", addrCount)
    print("Memory address is", memFields[2])
    integer = int(memFields[2], 16)
    print("Mem addr as int is", integer)
    bin_rep = format(integer, '0>12b')
    if (setIndex != 0):
        memOffset = bin_rep[(offset * -1):]
        cacheLineStart = hex(integer-int(bin_rep[(offset * -1):], 2))
        memSetIndex = bin_rep[((offset * -1) - 1): (offset * -1)]
        memTag = hex(int(bin_rep[0:tag], 2))
    else:
        memOffset = bin_rep[(offset * -1):]
        cacheLineStart = hex(integer-int(bin_rep[(offset * -1):], 2))
        memSetIndex = 0
        memTag = hex(int(bin_rep[0:tag + 1], 2))


    #memSetIndex = 0
    print("Binary is", bin_rep)
    print("Offset is", memOffset)
    print("Cache line starts at", cacheLineStart)
    print("Set index is", memSetIndex)
    print("Tag is", memTag)

    hitFlag = 0
    fullSetCounter = 0;
    if(ReadWrite == "R"):
        #check if cache miss or hit
        for i in range(numCacheLines):
            if (cacheSim[i][0] == int(memSetIndex)):
                if (cacheSim[i][2] == memTag and cacheSim[i][4] == cacheLineStart):
                    print("CACHE HIT!")
                    hitFlag = 1
                    break
                if (cacheSim[i][2] != memTag and cacheSim[i][4] != cacheLineStart and cacheSim[i][2] != "-1" and cacheSim[i][4] != "-1"):
                    fullSetCounter = fullSetCounter + 1
                    if (fullSetCounter == cacheLinesPerSet):
                        hitFlag = 2
                        break

        if (hitFlag == 0):
            print("Cache miss with empty slots in set. Need to insert.")
            missCount = missCount + 1
            for i in range(numCacheLines):
                if (cacheSim[i][2] == "-1" and cacheSim[i][4] == "-1"):
                    break
            cacheSim[i][2] = memTag
            cacheSim[i][4] = cacheLineStart
            cacheSim[i][3] = 1
            cacheSim[i][5] = time.time()
            #printCache(cacheSim)
        if (hitFlag == 2):
            print("Cache miss with full slots in set. Must replace using LRU.")
            missCount = missCount + 1
            oldestTime = 10000000000000000
            oldestRow = -1
            for i in range(numCacheLines):
                if (cacheSim[i][0] == int(memSetIndex)):
                    if (cacheSim[i][5] < oldestTime):
                        oldestTime = cacheSim[i][5]
                        oldestRow = i
            print("I will replace row", oldestRow, "since it was least recently used")
            cacheSim[oldestRow][2] = memTag
            cacheSim[oldestRow][4] = cacheLineStart
            cacheSim[oldestRow][3] = 1
            cacheSim[oldestRow][5] = time.time()
        #printCache(cacheSim)

        print()

        missRate = (missCount/accessCount) * 100

    if(ReadWrite == "W"): #copied funcs from read for check hit and miss
        BlockSize = 2^offset
        for i in range(numCacheLines):
            if (cacheSim[i][0] == int(memSetIndex)):
                if (cacheSim[i][2] == memTag and cacheSim[i][4] == cacheLineStart):
                    print("CACHE HIT!")
                    hitFlag = 1
                    break
                    if (cacheSim[i][2] != memTag and cacheSim[i][4] != cacheLineStart and cacheSim[i][2] != "-1" and cacheSim[i][4] != "-1"):
                        fullSetCounter = fullSetCounter + 1
                        if (fullSetCounter == cacheLinesPerSet):
                            hitFlag = 2
                            break
        if (hitFlag == 0):
            missCount = missCount +1
            print("Cache miss with empty slots in set. Need to insert.")
            for i in range(numCacheLines):
                if (cacheSim[i][2] == "-1" and cacheSim[i][4] == "-1"): #if nothing here fill spot
                    cacheSim[i][2] = memTag
                    cacheSim[i][4] = cacheLineStart
                    cacheSim[i][3] = 1
                    cacheSim[i][5] = time.time()
            
        
                              #printCache(cacheSim)
        if (hitFlag == 2):
            print("Cache miss with full slots in set. Must replace using LRU.")
            for i in range(numCacheLines):
                if (cacheSim[i][0] == int(memSetIndex)):
                    if (cacheSim[i][5] < oldestTime):
                        oldestTime = cacheSim[i][5]
                        oldestRow = i
                        print("I will replace row", oldestRow, "since it was least recently used")
                                              #printCache(cacheSim)
                 
        print()
                
        missRate = (missCount/accessCount) * 100
        

print("The miss rate is", missRate, "%")
