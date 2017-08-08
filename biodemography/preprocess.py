#####################################################
# Skyler Kuhn
# Biodemography Data pre-processing
# Center for the Study of Biological Complexity
# Version 1.2
#####################################################
from __future__ import print_function
import os




def pre_process_data(linelist):
    """Empty Fields within ICD data point are changed from Null to 0"""
    for index in range(len(linelist)):
        if not linelist[index]:
            linelist[index] = '0'
    return linelist


def clean_directory():

    print("Cleaning up files before analysis.....")
    for filename in os.listdir("."):
        if filename.startswith("Sex"):
            os.remove(filename)  # Deleting said file: It will be recreated below in Step 2
            print("Removing file {}".format(filename))
    print("Done!\n")

def parse_file(filename):
    """This function takes a filename as a argument and creates
    new files according for each biological sex."""
    
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
            output_file.write(",".join(line) + "\n")
        else:
            output_file2.write(",".join(line) + "\n")
    output_file.close()
    output_file2.close()
    fh.close()


def main():
    ################################
    # Step -1: Pre-processing
    # Pipeline Starts Here: Removing Previous incarnations of each country file that have parsed by biological sex
    clean_directory()

    ################################
    # Step 0: Parsing Data
    # Creating two new files for each biological sex for each country

    for filename in os.listdir("."):
        if filename.startswith("mdlt") and filename.endswith(".csv"):
            # print(filename)
            parse_file(filename)


if __name__ == "__main__":
    main()
