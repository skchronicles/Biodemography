#####################################################
# Skyler Kuhn & Hasan Alkhairo
# Biodemography Analysis
# Center for the Study of Biological Complexity
# Version 1.2
# Python Version: 2.7
#####################################################

from __future__ import generators, print_function, division
from math import factorial
import os
import time
import matplotlib.pyplot as plt

def uniqueCombinations(items, n):
    """ This function generates all possible unique given a cardinal set size."""
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
    """ This function takes a file and converts it to a sparse matrix nested dictionary, [age][icd_column_number]."""
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
    """Given a combination, this function will yield the summation of that particular unique combination for each age group.
    More specifically, it will yield in this order: unique combination (type list), age (type string),
    Summation of the ICD combination (type float), list of values that were summed to give the previous value (type list),
    dummy delimiter value of -999 (type string), the summation of the ICD combinations not included in the first set (type float ),
    list of values that were summed to give the previous value (type list)"""
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
        yield uc,k,summed_ICD, summedlist ,"-999", summed_NOT_ICD, summedNotList

def CalculationsPerDimension(dimensionsize):
    """ This calculates the Number of Unique possible combinations per size of Cardinal Set. """
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
    fileDict = {}
    for filename in os.listdir("."):  # right now this only works with one file, this will be modified later to work with all 7
        if filename.startswith("Sex1"):
            fileDict = fileTOdictionary(filename)
    timelist = []
    TotalDimensions = 5

    for dimension in range(TotalDimensions):

        start = time.clock()

        #Given a cardinal set size, this for loop will generate all unique possible combinations for it.
        for uc in uniqueCombinations(range(1,36,1), dimension):
            print("##################"+" Combination: "+str(uc)+" #######################")

            #For each combination generated by the outer for loop, this for loop below will pass the combination to the Test_ICD_calculation generator.
            #Reference Test_ICD_calculations for full description
            for ICDsummation in Test_ICD_calculations(uc,fileDict):
                #print("{}".format(ICDsummation))
                pass #Further statistical calculation will happen here

        endtime = time.clock()
        timelist.append(endtime-start)

    # ---- Creates Graph of Cardinal Set Size vs. Timing -------------------------------------------------------------
    print(timelist)
    plt.title("Cardinal Set Size vs. Time")
    plt.xlabel("Dimension Size")
    plt.ylabel("Time (s)")
    plt.plot(range(TotalDimensions),timelist)
    plt.show()

    # ---- Calculating the Number of Unique Combinations per Cardinal Set --------------------------------------------
    # (To find out the number of unique combinations for all 35 cardinal sets)
    print("\n\nTotal Number of Unique Combinations per Dimension: ")
    sumofCalcs = 0
    for i in range(1,36):
        sumofCalcs += int(CalculationsPerDimension(i))
        print(i, int(CalculationsPerDimension(i)))
    print("Total Number of Unique Combinations for 35 Dimensions: ", sumofCalcs)


