import sys, math
from collections import deque

queue = [None] * numWays

def createCache(cacheSize, cacheLineSize, numWays):
    
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

    memAddressSize = 10
    offset = math.log(cacheLineSize, 2)
    setIndex = math.log(numSets, 2)
    tag = memAddressSize - (offset + setIndex)
    print("Offset is s bits based on cache line size: s =", offset)
    print("Set index is t bits based on number of sets: t =", setIndex)
    print("Tag has remaining bits: tag =", tag)
    #create cache array and fill with all zeros
    cacheSim=[]
    for i in range(numCacheLines):
        cacheSim.append([0,0,0,0,0])

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
        cacheSim[i][2] = -1
        cacheSim[i][4] = -1
        lineCounter = lineCounter + 1
        wayNumber = wayNumber + 1

    for i in range(numCacheLines):
        print("cachSim[", i, "]: ", cacheSim[i])


def LRUQueue(tag):
    if tag not in queue:
        queue[0] = tag
        queue.rotate(-1)


#Main method
print("This is a cache simulator")

#createCache(256, 64, 2)
#createCache(4096, 128, 4)
createCache((1*1024), 64, 16)
file = open(sys.argv[1], "r")
while True:
    inputLine = file.readline()
    if inputLine == "":
        break

    memFields = inputLine.split()
    print("Memory address is", memFields[2])
