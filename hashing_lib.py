#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#INPUT DATA FROM "passwords1.txt" and "passwords2.txt"

listPasswords1=[]
listPasswords2=[]
filePassword1 = open("passwords1.txt", 'r')
lines_p1 = filePassword1.readlines()
for line in lines_p1:
    listPasswords1.append(line.strip())

filePassword2 = open("passwords2.txt", 'r')
lines_p2 = filePassword2.readlines()
for line in lines_p2:
    listPasswords2.append(line.strip())
    
#SET VARIABLES USED IN THE BLOOM FILTER  
    
n=len(listPasswords1)
p=0.0015
import math
m=math.ceil((n * math.log(p)) / math.log(1 / pow(2, math.log(2))))
k = round((m / n) * math.log(2))


#HASH FUNCTION

def fnv1_64(string, seed=0):
    """
    Returns: The FNV-1 hash of a given string. 
    """
    #Constants
    FNV_prime = 1099511628211
    offset_basis = 14695981039346656037

    #FNV-1a Hash Function
    hash = offset_basis + seed
    for char in string:
        hash = hash * FNV_prime
        hash = hash ^ ord(char)
    return hash

#BLOOM FILTER CLASS. HERE, WE INIT THE BIT-ARRAY AND ADD INOUT DATA IN OUR BLOOM FILTER

class BloomFilter:

    sizeArray=0
    number_HashFucntion=0
    array_BloomFilter=[]
    count=0
    @property
    def size(self):
        return self.sizeArray
    @property
    def numHash(self):
        return self.number_HashFucntion
    @property
    def arrayBloom(self):
        return self.array_BloomFilter
    
    def init(self,k,m):
        self.sizeArray=m
        self.number_HashFucntion=k
        
        for i in range(n):
            self.array_BloomFilter.append(0)
    
    def add(self,strings):
        print(self.number_HashFucntion)
        print(self.sizeArray)
        h=0
        for psw in strings:
            a=false
            for seed in range(self.number_HashFucntion):
                index=fnv1_64(psw,seed) % self.sizeArray
                if self.array_BloomFilter[index]==1 and a==false:
                    self.count+=1
                    a=true
                self.array_BloomFilter[index]=1
                

#THIS FOLLOWING FUNCTION 'checkPassw' checks how many password in listPasswords2 (i.e. in passowrds2.txt) are in our Bloom Filter.
def checkPassw(BloomFilter, listPasswords2):
    countCheck=0
    for psw in listPasswords2:
        count=0
        for seed in range(BloomFilter.number_HashFucntion):
            index=fnv1_64(psw,seed) % BloomFilter.sizeArray
            if BloomFilter.array_BloomFilter[index]==1:
                count+=1
            if count==BloomFilter.number_HashFucntion:
                countCheck+=1
            
    return countCheck

#BONUS SECTION

#This following function 'falsePositives' allows to calculate the exact number of false positive.
def falsePositives(BloomFilter, listPasswords1, listPasswords2):
    countFalsePositives=0
    for psw in listPasswords2:
        count=0
        for seed in range(BloomFilter.number_HashFucntion):
            index=fnv1_64(psw,seed) % BloomFilter.sizeArray
            if (BloomFilter.array_BloomFilter[index]==1):
                    count+=1
            else:
                break
            if count==BloomFilter.number_HashFucntion and not(psw in listPasswords1):
                countFalsePositives+=1
                
    return countFalsePositives


#MAIN FUNCTION THAT CALLS PREVIOUS FUNCTION AND PRINT OUT ALL OUTPUT DATA
import time

def BloomFilterFunc(listPasswords1, listPasswords2):
    start = time.time()
    #init our bloom filter
    BloomFilter.init(BloomFilter,k,m)
    #add all passowrd from listPassowrds1 to our bloom filter
    BloomFilter.add(BloomFilter,listPasswords1)
    #check and save into 'countPassw' the number of occurences of password (from passwords2) in the bloom filter
    countPassw=checkPassw(BloomFilter,listPasswords2)
    end = time.time()
    
    #print output data
    
    print('Number of occurences of password (from passwords2) in the bloom filter: ', countPassw)
    print('Number of hash function used: ', k)
    print('Number of duplicates detected: ', BloomFilter.count)
    print('Probability of false positives: ', p)
    print('Execution time: ', end-start)
    

    
#EXECUTE FUNCTIONS
BloomFilterFunc(listPasswords1, listPasswords2)
print('Number of flase positive: ', falsePositives(BloomFilter,listPasswords1,listPasswords2))

