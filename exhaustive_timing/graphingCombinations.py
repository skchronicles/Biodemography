#####################################################
# Skyler Kuhn & Hasan Alkhairo
# Biodemography Analysis
# Center for the Study of Biological Complexity
# Version 1.2.1 for more timing purposes. 
# Do not use this. Refer to Combinations.py for analysis
#####################################################

from __future__ import generators, print_function, division
from math import factorial
import os
import time
import matplotlib.pyplot as plt

def uniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for cc in uniqueCombinations(items[i+1:],n-1):
                yield [str(items[i])]+cc

def createICDdictionary(filename):
    """ This function takes the sorted_icd_codes file as an arg. and create the following dictionary:
    ex. {'1': 'BEXT', '3': 'CALI', '2': 'BINT',....,'33': 'XTRN'}"""
    fh = open(filename)
    ICDdict = {}
    for line in fh:
        line = line.strip().split()
        ICDdict[line[0]] = "Q"+line[1]   # the data set has a "Q" before each ICD code
    print (ICDdict)
    return ICDdict

def fileTOdictionary(filename):
    fh = open(filename)
    header = next(fh)
    data_dict = {}
    numlist = range(1,36)
    for line in fh:
        line = line.strip().split(",")
        for x in numlist:
            #dictionary below has the following structure
            #{"0":{"1":datavalue, "2":dataValue....}, "2.5":{"1":datavalue, "2":dataValue....}}
            #So we have the key being the age, and the value being a nested dict with the key being the ICD column number and the value being the number from the data set
            if str(line[4]) not in data_dict:
                data_dict[str(line[4])] = {}
                data_dict[str(line[4])][str(x)] = line[x+8]
            else:
                data_dict[str(line[4])][str(x)] = line[x+8]
    print(data_dict)
    return data_dict

def parse_file(filename):
    """This function takes a filename as a argument and creates two new files according to sex."""
    fh = open(filename)
    header = next(fh)
    output_file = open("Sex" + "1_" + filename, "a")
    output_file.write(header)
    output_file2 = open("Sex" + "2_" + filename, "a")
    output_file2.write(header)

    for line in fh:
        line = line.strip().split(",")  # split by "," because it is a csv file
        #line = re.split(r'(\s+)',line) #this regular expression based split was used to perserve white space in the line.
        if int(line[2]) == 1:
            output_file.write(",".join(line) + "\n")
        else:
            output_file2.write(",".join(line) + "\n")
    output_file.close()
    output_file2.close()
    fh.close()

def ICD_calculations(uc,fileDict):
    for k,v in fileDict.items():
        summed_ICD = 0.0
        for x in uc:
            summed_ICD += float(fileDict[k][x])
        yield k, summed_ICD

def Test_ICD_calculations(uc,fileDict):
    for k,v in fileDict.items():
        summedlist = []
        summed_ICD = 0.0
        summed_NOT_ICD = 0.0
        summedNotList = []
        code_not_in_list = list(set(['24', '25', '26', '27', '20', '21', '22', '23', '28', '29', '1', '3', '2', '5',
                                     '4', '7', '6', '9', '8', '11', '10', '13', '12', '15', '14', '17', '16', '19',
                                     '18', '31', '30', '35', '34', '33', '32']) - set(uc))
        for x in uc:
            summedlist.append(float(fileDict[k][x]))
            summed_ICD += float(fileDict[k][x])
        for y in code_not_in_list:
            summedNotList.append(float(fileDict[k][y]))
            summed_NOT_ICD += float(fileDict[k][y])
        yield k,summed_ICD, summedlist ,"-999", summed_NOT_ICD, summedNotList

def CalculationsPerDimension(dimensionsize):
    totalnumbydim = factorial(35)/(factorial(dimensionsize)*factorial(35-dimensionsize))
    return totalnumbydim


if __name__== "__main__":
    for filename in os.listdir("."):
        if filename.startswith("Sex"):
            os.remove(filename)
    ICDdict = {}
    for filename in os.listdir("."):
        if filename.startswith("mdlt24") and filename.endswith(".csv"):
            parse_file(filename)
        elif filename.startswith("sorted"):
            ICDdict = createICDdictionary(filename)

    for filename in os.listdir("."):
        #fileDict = {}
        if filename.startswith("Sex1"):  # this will have to be moved to line 70 (where we are generating unique combs)
            fileDict = fileTOdictionary(filename)
    timelist = []
    TotalDimensions = 4

    outFH = open("timing_combinations.txt","w")

    for dimension in range(TotalDimensions):
        start = time.clock()

        for uc in uniqueCombinations(range(1,36,1), dimension):
            print("##################"+" Combination: "+str(uc)+" #######################")
            for ICDsummation in Test_ICD_calculations(uc,fileDict):
                #print("{}".format(ICDsummation))
                pass
        endtime = time.clock()

        timelist.append(endtime-start)
        outFH.write("{}\t{}\n".format(dimension, endtime-start))

    print(timelist)
    plt.xlabel("Dimension Size")
    plt.ylabel("Time (s)")
    plt.plot(range(TotalDimensions),timelist)
    #plt.show()


    print("\n\nTotal Number of Unique Combinations per Dimension:")
    outFH.write("\n\nTotal Number of Unique Combinations per Dimension:\n")
    sumofCalcs = 0
    pltstring = ""
    for i in range(1,36):
        sumofCalcs += int(CalculationsPerDimension(i))
        print(i, int(CalculationsPerDimension(i)))
        outFH.write("{}\t{}\n".format(i, int(CalculationsPerDimension(i))))
        pltstring += "{}: {}, ".format(i, int(CalculationsPerDimension(i)))
    #plt.figtext(.01, .5, pltstring,size="x-small", ha='center')
    plt.savefig("timingGraph.png")
    print("Total Number of Unique Combinations for 35 Dimensions: ", sumofCalcs)





