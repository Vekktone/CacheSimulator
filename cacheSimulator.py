import sys, math, time
from cache import createCache, printCache
import cache

#Main method
#print("This is a cache simulator")

cacheSize = int(sys.argv[2])
cacheLineSize = int(sys.argv[3])
numWays = int(sys.argv[4])

#create cache data structure
createCache(cacheSize, cacheLineSize, numWays)

#initialize variables for computations
cacheSim = cache.cacheSim
numCacheLines = cache.numCacheLines
numSets = cache.numSets
cacheLinesPerSet = cache.cacheLinesPerSet
accessCount = 0
missCount = 0

#open trace file and begin reading
file = open(sys.argv[1], "r")
while True:
    inputLine = file.readline()
    if inputLine == "" or inputLine == "#eof":
        break
    
    #break line of text into PC, R/W, and Address, save into list
    accessFields = inputLine.split()
    if (len(accessFields) != 3):
        continue

    accessCount = accessCount + 1

    #print("accessCount =", accessCount)

    addr = int(accessFields[2], 16)
    #print("addr is", addr)
    memOffet = addr & (cacheLineSize - 1)
    memSetIndex = addr >> int(math.log(cacheLineSize, 2)) & (numSets - 1)
    memTag = addr >> (int(math.log(numSets, 2)) + int(math.log(cacheLineSize, 2)))
    #print("Offset is", memOffset)
    #print("Cache line starts at", cacheLineStart)
    #print("Set index is", memSetIndex)
    #print("Tag is", memTag)

    hitFlag = 0
    fullSetCounter = 0;
    if(accessFields[1] == "R"):
        #check if cache miss or hit
	#figure out what rows in the cache are associated with the set number
        startingRow = cacheLinesPerSet * int(memSetIndex)
        #print("Starting row is", startingRow)
        for i in range(startingRow, startingRow + cacheLinesPerSet):
            if (cacheSim[i][2] == memTag):
                #print("CACHE HIT!")
                hitFlag = 1
                cacheSim[i][5] = time.time()
                break

        fullFlag = 1
        oldestTime = 1000000000000000000000000  #use a large time value by default for LRU comparison
        oldestRow = -1

        if (hitFlag == 0):
            #print("Cache miss. Need to insert.")
            missCount = missCount + 1
            for i in range(startingRow, startingRow + cacheLinesPerSet):
                if (cacheSim[i][3] == 0): #valid bit 0, this is an empty slot
                    fullFlag = 0
                    break
                if (cacheSim[i][5] < oldestTime):
                    oldestTime = cacheSim[i][5]
                    oldestRow = i
            if (fullFlag == 0):
                #print("Cache set has empty slots. Inserting...")
                cacheSim[i][2] = memTag
                cacheSim[i][4] = "data"
                cacheSim[i][3] = 1
                cacheSim[i][5] = time.time()
            else:
                #print("Cache set full, replacing using LRU.")
                cacheSim[oldestRow][2] = memTag
                cacheSim[oldestRow][4] = "data"
                cacheSim[oldestRow][3] = 1
                cacheSim[oldestRow][5] = time.time()
	
    elif(accessFields[1] == "W"):
        #print("Write detected. Using Write back policy.")
        startingRow = cacheLinesPerSet * int(memSetIndex)
        for i in range(startingRow, startingRow + cacheLinesPerSet):
            if (cacheSim[i][2] == memTag):
                #print("CACHE WRITE HIT! Updating...")
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
            #print("Cache write miss. Need to insert.")
            missCount = missCount + 1
            for i in range(startingRow, startingRow + cacheLinesPerSet):
                if (cacheSim[i][3] == 0): #valid bit 0, this is an empty slot
                    fullFlag = 0
                    break
                if (cacheSim[i][5] < oldestTime):
                    oldestTime = cacheSim[i][5]
                    oldestRow = i
            if (fullFlag == 0):
                #print("Cache set has empty slots. Inserting...")
                cacheSim[i][2] = memTag
                cacheSim[i][4] = "data"
                cacheSim[i][3] = 1
                cacheSim[i][5] = time.time()
            else:
                #print("Cache set full, replacing using LRU.")
                cacheSim[oldestRow][2] = memTag
                cacheSim[oldestRow][4] = "data"
                cacheSim[oldestRow][3] = 1
                cacheSim[oldestRow][5] = time.time()
missRate = (missCount/accessCount) * 100
#print("Access count is", accessCount)
#print("Miss count is", missCount)
print ("Cahe miss rate: {:0.2f}%".format(missRate, 3))
