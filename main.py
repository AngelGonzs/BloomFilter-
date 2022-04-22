from cmath import log
import hashlib
import csv
import sys
import os
import math
import pandas as pd

# USE THIS SPACE TO RETRIEVE COMMAND LINE 
# ARGUMENTS AND CREATE GLOBAL VARIABLES

# inputSamples will be first argument, checkList is second
samples = sys.argv[1]
check = sys.argv[2]

samplesCSV = os.path.abspath(samples)
checkCSV = os.path.abspath(check)

#Statement below is used to then get the length of our input with pandas
inputSample = pd.read_csv(samplesCSV)


inputLen = len(inputSample.axes[0]) + 1

# Just checking that the length is right
# print(inputLen)



# COMMENCE THE BLOOM FILTER CLASS

class bloomFilter:

    # BloomFilter constructor
    # Parameters:
    #   n is the size of our input
    #   p is our false-positive rate (hardcoded)
    #   m is the number of bits needed in the bloomFilter (calculated)
    #   k is the amount of hash functions we will need, seen in later methods (calculated)
    def __init__(self, n):
        self.n = n
        self.p = 0.0000001
        self.m = math.ceil((n * math.log(self.p)) / math.log(1 / pow(2, math.log(2))))

        # FORMULAE EXTRACTED FROM:
        # https://hur.st/bloomfilter/

        self.filter = [0] * self.m
        # Initialize our bloom filter with 0's which will
        # indicate that it is completely empty
        self.filterSize = len(self.filter)
        # doing this for cleaning up code when calculating k later on


    # Hashes the input the necessary amount of times
    # We use hashing based on SHA256 and use modulus of the size of the filter to avoid any index errors
    # The usage of the i in the for loop lets us do the following:
    #      We divide the filter in <= k sections which will be determined to 10^i (i in range (k))
    #      Doing this we hope to have 1 or 2 hashes per section for each of our inputs, optimally 1 per section
    #
    # Parameters:
    # s : input email
    def hashing(self, s):

        k = round((self.m / self.n) * math.log(2))
        hashes = []

        for i in range(k):


            add = int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16) % (10 ** (i + 1)) % BF.filterSize
            # add = int(hashlib.sha224(s.encode("utf-8")).hexdigest(), 16) % (10 ** (i + 1)) % BF.filterSize


            hashes.append(add)

        return hashes

    # use this method to add the emails to our bloomFilter
    # we get their hashes and input their index onto the bloomFilter list
    # Parameter: s input email
    def add(self, input):

        hashes = self.hashing(input)

        for hash in hashes:
            self.filter[hash] = 1
            # We use a 1 to indicate that this index
            # has been used by a hashed input 

    # Similar to the add method, we get the hashes and verify if these are in the list
    # Were it not to be in the list, we assure that it is not in the DB
    # Parameter: s input emails
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

# We start by creating our bloom filter
BF = bloomFilter(inputLen)

# NOW THAT OUR BLOOM FILTER IS INITIALIZED
# ALL THAT IS LEFT IS TO ENTER OUR SAMPLES

with open(samplesCSV, 'r') as inputFile:
    inputReader = csv.reader(inputFile)

    for line in inputReader:
        BF.add(line[0])


# Now we create the results.csv file and use our check method in BF
# To determine whether the inputs might be in our DB or not.
with open("results.csv", 'w') as results:

    # Remember to change to open(checkArg)
    with open(checkCSV, 'r') as check_file:
        csv_reader = csv.reader(check_file)

        fieldnames = ['Email', 'Probability']
        results_writer = csv.DictWriter(results, fieldnames=fieldnames)

        results_writer.writeheader()

        for line in csv_reader:
            results_writer.writerow({'Email': line[0], 'Probability': BF.check(line[0])})



