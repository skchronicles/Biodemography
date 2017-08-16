#####################################################
# Skyler Kuhn
# Biodemography Analysis
# Center for the Study of Biological Complexity
# Version 1.2
#####################################################

from __future__ import generators, print_function, division
from math import factorial
from scipy.stats import chi2_contingency, chisquare
import numpy as np
from os import path
import os, re, preprocess, time


def find_current_dir():
    here = os.path.abspath(os.path.dirname(__file__))
    current_dir = here.split("/")[-1]
    return current_dir


def pre_process_data(linelist):
    """Empty Fields within ICD data point are changed from Null to 0"""
    for index in range(len(linelist)):
        if not linelist[index]:
            linelist[index] = '0'
    return linelist


def uniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in range(len(items)):
            for cc in uniqueCombinations(items[i+1:],n-1):
                yield [str(items[i])]+cc


def createICDdictionary(filename):
    """This function takes the sorted_icd_codes file as an arg. and create the following dictionary:
    ex. {'1': 'BEXT', '3': 'CALI', '2': 'BINT',....,'35': 'XTRN'}"""
    fh = open(filename)
    ICDdict = {}
    for line in fh:
        line = line.strip().split()
        ICDdict[line[0]] = line[1]
        #ICDdict[line[0]] = "Q"+line[1]   # the data set has a "Q" before each ICD code
    print(ICDdict)
    return ICDdict


def _file2dictionary(filename):
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


def support_counter(linelist, agelist, supp_dict):
    support_count_dict = supp_dict
    try:
        start_index = linelist.index("Qtot") + 1
    except ValueError:
        start_index = 9

    countslist = linelist[start_index:start_index + 35] + agelist
    for item in countslist:
        if item in support_count_dict:
            support_count_dict[item] += 1
        else:
            support_count_dict[item] = 1
    return support_count_dict


def files2dictionary(filename, countryID, supp_dict):
    """Creates a dictionary to hold all the information for each biological sex below. It has following structure
        {"Sex1_mdlt2450": {"0":{"1":datavalue, "2":dataValue....}, "2.5":{"1":datavalue, "2":dataValue....}...}..}
            -- where: [Sex#countryID][Age][ICDcode] = one_datapoint"""

    fh = open(filename)
    header = next(fh)

    data_dict = {}
    data_dict[countryID] = {}

    numlist = range(1, 36)
    agelist = []
    for line in fh:
        linelist = line.strip().split(",")
        age = linelist[4]
        agelist.append(age)
        for icdrep in numlist:
            if str(age) not in data_dict[countryID]:
                data_dict[countryID][str(age)] = {}
                #if str(icdrep) not in data_dict[countryID][str(age)]:
                data_dict[countryID][str(age)][str(icdrep)] = float(linelist[icdrep+8]) # look into changing this to one million
            else:
                data_dict[countryID][str(age)][str(icdrep)] = float(linelist[icdrep+8]) # look into changing this to one million
    fh.close()
    supp_dict.update(support_counter(header.split(","), agelist, supp_dict))
    return data_dict, supp_dict


def apriori(q, q_pvalue, insig, sig):
    """ This function implements a modified version of the apriori algorithm which can be used for speeding up
    an otherwise exhaustive high-performance computing problem. The apriori algorithm is commonly used in mining
    frequent itemsets for boolean association rules. It uses a monotonic "bottom up" approach, where frequent subsets
    are extended one item at a time."""

    insignificant = [] + insig
    significant = [] + sig

    while len(q) > 0:
        element = q[0]
        if isinstance(element, int):
            element = tuple([element]) # it easier to just convert this to a tuple (so everything is the same data type)

        pvalue = q_pvalue[element]    # chi-squared test, verify if the given element satisfies the support criterion

        if pvalue == 1:
            significant.append(element)
            #print significant
            for i in range(element[-1]+1,4):
                if i not in insignificant:
                    #print i, "#####", element
                    tentativeCandidate = tuple(sorted(list(element)+[i])) # add the two lists together (element is a list)
                    if tentativeCandidate not in q and tentativeCandidate not in significant: # then add it to the queue
                        #print "Queue {}\nTentative Candidate{}\nSignificant {}\nInsignicant {}\n" \
                        #      "##################################".format(q,tentativeCandidate,significant,insignificant)
                        q.append(tentativeCandidate)
                        yield q,tentativeCandidate,significant,insignificant
            q.pop(0) #remove it from the queue after we have created/tried all the tentativeCandidates

        else:        # when the p-value not significant
            q.pop(0)
            insignificant.append(element)
            yield q,tentativeCandidate,significant,insignificant
    else:
        yield q,tentativeCandidate,significant,insignificant  # grab the last values before breaking out of the while loop

def apriori_v3(q, insig, sex_file_dict, countries_list, age):
    """ This function implements a modified version of the apriori algorithm which can be used for speeding up
    an otherwise exhaustive high-performance computing problem. The apriori algorithm is commonly used in mining
    frequent itemsets for boolean association rules. It uses a monotonic "bottom up" approach, where frequent subsets
    are extended one item at a time."""

    q = [[int(num)] for num in q]  # queue is formatted as a nested list
    insignificant = [[int(num)] for num in insig]
    significant = []

    #print("\nInsig", insignificant)
    #print("Sig", significant)
    #print("Queue\n", q)

    while len(q) > 0:
        element = q[0]
        obs_freqs = []

        for country in countries_list:
            icd_freq = 0
            for freq in element:
                icd_freq += round(float(sex_file_dict[country][age][str(freq)]) * 1000000)
            obs_freqs.append(icd_freq)

        chisq, pvalue = chisquare(obs_freqs)

        if pvalue >= 0.01:
            significant.append(element)

            for i in range(int(element[-1])+1,36):
                if [i] not in insignificant:
                    tentativeCandidate = sorted(list(element)+[i])  # add the two lists together (element is a list)
                    if tentativeCandidate not in q and tentativeCandidate not in significant: # then add it to the queue

                        q.append(tentativeCandidate)
            q.pop(0) #remove it from the queue after we have created/tried all the tentativeCandidates

        else:        # when the p-value not significant
            q.pop(0)
            insignificant.append(element)
    return significant  # grab the last values before breaking out of the while loop


def bottom_up_trim(q, sex_file_dict, countries_list, age):
    """ Before implementing the apriori algorithm, we prune insignificant item-sets of size one from
    the queue. The generated insig list will help us avoid generating redundant combinations.
    Returns: pruned queue and an insigficant set to be passed to the aprori_v2 function. """
    insig = []
    sig = []

    for num in q:
        obs_freqs = []
        for country in countries_list:

            icd_freq = round(float(sex_file_dict[country][age][str(num)]) * 1000000)
            obs_freqs.append(icd_freq)

        print("Tested values for {}\t{}".format(num, obs_freqs))
        # Calculate chi-square test here
        if 0 not in obs_freqs:
            chisq, pvalue = chisquare(obs_freqs)
            if pvalue <= 0.01:
                # print("Removing {} from the Queue".format(num))
                insig.append(num)
            else:
                # print("Significant: ", pvalue)
                sig.append(num)
        else:  # meaning at least one of the frequencies is zero (to perform chi-squared test counts must be >)
            insig.append(num)
    q = sig
    return q, insig


def runpreprocessing(numofcountryfiles, numofsexfiles):
    """This check to see if the number of biological sex files is twice the number  of
       country files. If not, the preprocessing.py is envoked."""

    if numofsexfiles/float(numofcountryfiles) == 2.0:
        return False
    else:
        return True


def chi_square_analysis(obs_list):
    """Had to change interpreter from Python 3.5 to 2.7 (located in /usr/bin/python)"""
    obs = np.array(obs_list)
    chi2, p, dof, expected = chi2_contingency(obs)
    return chi2, p, dof, expected


def parse_file(filename):
    """This function takes a filename as a argument and creates new files according for each biological sex."""
    print(filename)
    fh = open(filename)
    header = next(fh)
    output_file = open("Sex" + "1_" + filename, "a")
    output_file.write(header)
    output_file2 = open("Sex" + "2_" + filename, "a")
    output_file2.write(header)

    for line in fh:
        line = line.strip().split(",")  # split by "," because it is a csv file
        line = pre_process_data(line)
        if int(line[2]) == 1:
            print(line)
            output_file.write(",".join(line) + "\n")
        else:
            output_file2.write(",".join(line) + "\n")
    output_file.close()
    output_file2.close()
    fh.close()


def ICD_calculations(uc,fileDict):
    for k, v in fileDict.items():
        summed_ICD = 0.0
        for x in uc:
            summed_ICD += float(fileDict[k][x])
        yield k, summed_ICD


def find_not_in_icd_set(lenoforginalset, numbers_set):
    """This function will find all the icd codes (represented as numbers) not in a given set."""
    originalset = [str(i) for i in range(1, lenoforginalset+1, 1)]

    numbers_not_in_set = list(set(originalset)-set(numbers_set))
    numbers_not_in_set = sorted([int(num) for num in numbers_not_in_set])
    numbers_not_in_set = [str(num) for num in numbers_not_in_set]

    return numbers_not_in_set

def countfiles():
    parsedfiles = 0
    originalfiles = 0
    for filename in os.listdir("."):
        if filename.startswith("mdlt") and filename.endswith(".csv"):
            originalfiles += 1
        elif "Sex" in filename:
            parsedfiles += 1
    return parsedfiles, originalfiles

def longdescription():
    """This function displays project information."""
    print()
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.rst')) as f:
        long_description = f.read()

    print(long_description)


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


def main():

    ################################
    # Step 1: Pre-processing Check
    # Pipeline Starts Here: Data is checked to see if pre-processing is necessary. If so, 'preprocess.py' is envoked.

    longdescription()  # Prints a description of the project.

    # Finding the counts of the country files relative to the biological sex files (should be a 1:2 ratio)
    parsedfiles, originalfiles = countfiles()  # if the ratio is different, then runpreproccessing is called.

    # Checking to see if all of the files for each country have been parsed by biological sex (represented by 1 or 2).
    if runpreprocessing(numofcountryfiles=originalfiles, numofsexfiles=parsedfiles):
        preprocess.main()
        print("\nBeginning Analysis")
        time.sleep(2)

    print("\n\n###########################################################################")
    print("# Step 2: Data Storage and Management")
    ################################
    # Step 2: Data Storage and Management
    # Two Dictionaries (for each sex) are created to house the data. Minimum support criterion are also calculated here.
    sex1_file_dict = {}
    sex1_age_icd_support = {}

    sex2_file_dict = {}
    sex2_age_icd_support = {}

    for filename in os.listdir("."):
        sex1_datafile = re.match("(^Sex1_\w+)_\d+.csv", filename)
        sex2_datafile = re.match("(^Sex2_\w+)_\d+.csv", filename)
        if sex1_datafile:
            #print("Match Sex1:", filename, ":", sex1_datafile.group(1))
            argus = files2dictionary(filename, sex1_datafile.group(1), sex1_age_icd_support)
            print("Sex1", "\n", argus[0], "\n", argus[1])
            sex1_file_dict.update(argus[0]), sex1_age_icd_support.update(argus[1])  # concatenating dicts
        elif sex2_datafile:
            #print("Match Sex2:", filename, ":", sex2_datafile.group(1), "\n")
            argus = files2dictionary(filename, sex2_datafile.group(1), sex2_age_icd_support)
            print("Sex2", "\n", argus[0], "\n", argus[1])
            sex2_file_dict.update(argus[0]), sex2_age_icd_support.update(argus[1])

    print("\n\n###########################################################################")
    print("# Step 3: Apriori Algorithm")
    ################################
    # Step 3: Apriori Algorithm
    # Implementing a modified version of the Apriori algorithm for speeding up an otherwise exhaustive HPC problem

    # Creating a list of all countries
    sex1_countries_list = sex1_file_dict.keys()
    sex2_countries_list = sex2_file_dict.keys()
    sex1_file_dict.values()

    # Creating an age support dictionary. This is used to make sure the minimum support count for each age is met.
    age_support_dict = {}
    for key, value in sex1_age_icd_support.items():
        try:
            int(key)
            if sex1_age_icd_support[key] == len(sex1_countries_list):   # checking minimum support counts
                age_support_dict[key] = value
        except ValueError:
            pass
    print("Age Support Dict: ", age_support_dict)

    signifOUTFH = open("results.tsv", "w")
    signifOUTFH.write("Sex\tAge\tSignificant_Combination\n")

    counter1 = 0
    print("Countries Evaluated: {}\n".format(sex1_countries_list))
    for country_age_dict in sex1_file_dict.values():
        counter1 += 1
        for age, icds_dict in country_age_dict.items():
            if age in age_support_dict and counter1 <= 1:  # meaning this age is in all six files

                qu = [str(i) for i in range(1, 36, 1)]
                #icd_count = round(float(sex1_file_dict[country][age][i]) * 1000000)
                qu, insig = bottom_up_trim(qu, sex1_file_dict, sex1_countries_list, age)
                print("Sex1:\tAge\t{}\nNew Queue\t{}\nInsignificant\t{}\n".format(age,qu, insig))
                """!!!!!!!!!!!!! Tie in APRIORI ALGORITHM here :D !!!!!!!!!!!!!"""
                significant_combinations = apriori_v3(qu, insig, sex1_file_dict, sex1_countries_list, age)
                if len(significant_combinations) > 0:
                    signifOUTFH.write("{}\t{}\t{}\n".format("1", age, significant_combinations))
                print("Apriori Significant Combs", significant_combinations)
                print("##################################\nSuccess!")

    print("Countries Evaluated: {}\n".format(sex2_countries_list))
    counter2 = 0
    for country_age_dict in sex2_file_dict.values():
        counter2 += 1
        for age, icds_dict in country_age_dict.items():
            if age in age_support_dict and counter2 <= 1:  # meaning this age is in all six files

                qu = [str(i) for i in
                      range(1, 36, 1)]
                qu, insig = bottom_up_trim(qu, sex2_file_dict, sex2_countries_list, age)
                print("Sex2:\tAge\t{}\nNew Queue\t{}\nInsignificant\t{}\n".format(age, qu, insig))
                """!!!!!!!!!!!!! Tie in APRIORI ALGORITHM here :D !!!!!!!!!!!!!"""
                significant_combinations = apriori_v3(qu, insig, sex2_file_dict, sex2_countries_list, age)
                if len(significant_combinations) > 0:
                    signifOUTFH.write("{}\t{}\t{}\n".format("2", age, significant_combinations))
                print("Apriori Significant Combs", significant_combinations)
                print("##################################\nSuccess!")
    signifOUTFH.close()

if __name__ == "__main__":

    main()

