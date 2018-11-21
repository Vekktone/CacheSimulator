import sys

file = open(sys.argv[1], "r")
while True:
    inputline = file.readline()
    if inputline == "":
        break
    print(inputline)

print("This is a cache simulator")
