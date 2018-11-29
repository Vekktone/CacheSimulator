import sys, math, time

cacheSim=[]
numCacheLines = 0
numSets = 0
cachLinesPerSet = 0

memAddressSize = 0
offset = 0
setIndex = 0
tag = 0
cacheLineSize = 64

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
    
    #memAddressSize = 32
    #offset = math.ceil(math.log(cacheLineSize, 2))
    #setIndex = math.ceil(math.log(numSets, 2))
    #tag = memAddressSize - (offset + setIndex)
    #print("Offset is s bits based on cache line size: s =", offset)
    #print("Set index is t bits based on number of sets: t =", setIndex)
    #print("Tag has remaining bits: tag =", tag)
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


cacheSize = int(sys.argv[2])
cacheLineSize = int(sys.argv[3])
numWays = int(sys.argv[4])
#createCache(256, cacheLineSize, 2)
#createCache((256*1024), cacheLineSize, 16)
#createCache((1*1024), cacheLineSize, 16)
#createCache((4*1024*1024), cacheLineSize, 16)
#createCache((32*1024), cacheLineSize, 16)

createCache(cacheSize, cacheLineSize, numWays)
printCache(cacheSim)

print()
accessCount = 0
missCount = 0
addrCount = 0;
file = open(sys.argv[1], "r")
while True:
    inputLine = file.readline()
    #check if we need to read or write to cache if line is populated 
    if inputLine == "" or inputLine == "#eof":
        break
    
    #calculate specific metric for each address, save into variables
    memFields = inputLine.split()
    if (len(memFields) != 3):
        continue

    accessCount = accessCount + 1
    addrCount = addrCount + 1

    print()
    print("addrCount =", addrCount)

    addr = int(memFields[2], 16)
    print("addr is", addr)
    memOffet = addr & (cacheLineSize - 1)
    memSetIndex = addr >> math.ceil(math.log(cacheLineSize, 2)) & (numSets - 1)
    memTag = addr >> (math.ceil(math.log(numSets, 2)) + math.ceil(math.log(cacheLineSize, 2)))
    #print("Offset is", memOffset)
    #print("Cache line starts at", cacheLineStart)
    #print("Set index is", memSetIndex)
    #print("Tag is", memTag)

    hitFlag = 0
    fullSetCounter = 0;
    if(memFields[1] == "R"):
        #check if cache miss or hit
	#figure out what rows in the cache are associated with the set number
        startingRow = cacheLinesPerSet * int(memSetIndex)
        #print("Starting row is", startingRow)
        for i in range(startingRow, startingRow + cacheLinesPerSet):
            if (cacheSim[i][0] == int(memSetIndex)):
                if (cacheSim[i][2] == memTag):
                    print("CACHE HIT!")
                    hitFlag = 1
                    break

        fullFlag = 1
        oldestTime = 1000000000000000000000000
        oldestRow = -1

        if (hitFlag == 0):
            print("Cache miss. Need to insert.")
            missCount = missCount + 1
            for i in range(startingRow, startingRow + cacheLinesPerSet):
                if (cacheSim[i][3] == 0): #valid bit 0, this is an empty slot
                    fullFlag = 0
                    break
                if (cacheSim[i][5] < oldestTime):
                    oldestTime = cacheSim[i][5]
                    oldestRow = i
            if (fullFlag == 0):
                print("Cache set has empty slots. Inserting...")
                cacheSim[i][2] = memTag
                cacheSim[i][4] = "data"
                cacheSim[i][3] = 1
                cacheSim[i][5] = time.time()
            else:
                print("Cache set full, replacing using LRU.")
                cacheSim[oldestRow][2] = memTag
                cacheSim[oldestRow][4] = "data"
                cacheSim[oldestRow][3] = 1
                cacheSim[oldestRow][5] = time.time()
	
            #printCache(cacheSim)
            #print()
    if(memFields[1] == "W"):
        print("Write detected. Using Write back policy.")
        startingRow = cacheLinesPerSet * int(memSetIndex)
        for i in range(startingRow, startingRow + cacheLinesPerSet):
            if (cacheSim[i][0] == int(memSetIndex)):
                if (cacheSim[i][2] == memTag):
                    print("CACHE WRITE HIT! Updating...")
                    cacheSim[i][2] = memTag
                    cacheSim[i][4] = "dataUpdated"
                    cacheSim[i][3] = 1
                    cacheSim[i][5] = time.time()
                    hitFlag = 1
                    break

        fullFlag = 1
        oldestTime = 1000000000000000000000000
        oldestRow = -1

        if (hitFlag == 0):
            print("Cache write miss. Need to insert.")
            missCount = missCount + 1
            for i in range(startingRow, startingRow + cacheLinesPerSet):
                if (cacheSim[i][3] == 0): #valid bit 0, this is an empty slot
                    fullFlag = 0
                    break
                if (cacheSim[i][5] < oldestTime):
                    oldestTime = cacheSim[i][5]
                    oldestRow = i
            if (fullFlag == 0):
                print("Cache set has empty slots. Inserting...")
                cacheSim[i][2] = memTag
                cacheSim[i][4] = "data"
                cacheSim[i][3] = 1
                cacheSim[i][5] = time.time()
            else:
                print("Cache set full, replacing using LRU.")
                cacheSim[oldestRow][2] = memTag
                cacheSim[oldestRow][4] = "data"
                cacheSim[oldestRow][3] = 1
                cacheSim[oldestRow][5] = time.time()
	
missRate = (missCount/accessCount) * 100
        
print("Access count is", accessCount)
print("Miss count is", missCount)
print("The miss rate is", missRate, "%")
