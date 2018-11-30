# CacheSimulator
A simulator for a cache that simulates set associative caches with LRU replacement/write-back policies.

To Clone on git:

git clone https://github.com/Vekktone/CacheSimulator.git

Usage- There are two main ways to run the cache simulator program:

(1) If you are running with one of the 10 designated memory trace
files defined in the project requirements, the command is:

sh run_sim.sh [memTraceFile]

(2) If you are using a custom trace file with user defined parameters, the command is:

sh run_sim.sh [memTraceFile] [cacheSizeInBytes] [cacheLineSizeInBytes] [numberOfWays]
