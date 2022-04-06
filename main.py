from cmath import log
import hashlib
import csv 
import sys
import math
import pandas as pd

# USE THIS SPACE TO RETRIEVE COMMAND LINE 
# ARGUMENTS AND CREATE GLOBAL VARIABLES


# Has to be changed to CML values later
inputSample = pd.read_csv("samples.csv")
checkSample = pd.read_csv("check.csv")

inputLen = len(inputSample.axes[0]) + 1
checkLen = len(checkSample.axes[0]) + 1



# COMMENCE THE BLOOM FILTER CLASS

class bloomFilter:

    #BloomFilter constructor
    #Parameters: (check CIIC 4020 Labs for format)
    def __init__(self, n, m, p, filter, filterSize):
        self.n = n
        self.m = math.ceil((n * math.log(p)) / math.log( 1 / pow(2, log(2) ) ) )
        self.p = p

        self.filter = filter
        self.filterSize = filterSize



    # Initialize our bloom filter with 0's which will
    # indicate that it is empty
    def initializeBloom(self):
        bloomSize = math.ceil((self.inputSize * math.log(self.falseRate)) / math.log(1 / pow(2, math.log(2))))

        self.filter = [0 for i in range(bloomSize)]
        self.filterSize = bloomSize
        # FORMULA EXTRACTED FROM:
        # https://hur.st/bloomfilter/

    
    # Hashes the input the necessary amount of times
    # s : input
    def hashing(self, s):

        k = round( (self.m / self.n) * math.log(2))

        hashes = []

        for i in range(k):

            if i % 2 == 0:
                add = int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16) % (10 ** (i+1)) * (i+1) % self.filterSize

            else:
               add = abs(hash(s)) % (10 ** 6) * (i+1) % self.filterSize

        hashes.append(add)

        return hashes


    def add(self, input):

        hashes = self.hashing(input)

        for hash in hashes:

            self.filter[hash] = 1
            # We use a 1 to indicate that this index
            # has been used by a hashed input 



    def check(self, input):

        hashes = self.hashing(input)

        for hash in hashes:

            if self.filter[hash] == 0:
                return "Not in the DB"

        
        return "Probably in the DB"

    

# WE ARE NOW DONE WITH THE METHODS FOR THE BLOOM FILTER CLASS
# AHEAD WE WILL BE ADDING THE CALLS NECESSARY TO BEGIN THE 
# PROGRAM AND ADDING ALL THE SAMPLES NEEDED TO RUN AND TEST IT



# MAIN CALLS:

filter = []

BF = bloomFilter(inputLen, 0, 0.0001, filter, 0)


BF.initializeBloom() # Initialize the bloom filter and all the empty variables


# NOW THAT OUR BLOOM FILTER IS INITIALIZED
# ALL THAT IS LEFT IS TO ENTER OUR SAMPLES



with open("samples.csv", 'r') as inputFile:

    inputReader = csv.reader(inputFile)

    for line in inputReader:

        BF.add(line[0])

    
print(BF.filter)