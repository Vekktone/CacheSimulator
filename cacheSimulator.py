import sys

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




file = open(sys.argv[1], "r")
while True:
    inputline = file.readline()
    if inputline == "":
        break
    print(inputline)

print("This is a cache simulator")

createCache(256, 64, 2)
