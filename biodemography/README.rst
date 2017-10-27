#########################################################################################################
# Skyler Kuhn
# Center for the Study of Biological Complexity
# Biodemography Project: Apriori Aligorithm
# Version 1.2.0
##########################################################################################################

Biodemography | Apriori Algorithm | Data Mining | Combinatorial optimization | WHO

Usage Requirements:   
--- Data files should be in csv format      
--- Required External Packages: [scipy.stats, numpy]  

This package implements an unique method for utilizing frequent item-set data mining techniques 
in exhaustive combinatorics to find conserved patterns in the different global causes of mortality. 
A modified version of the apriori algorithm is implemented to find the common causes mortality
across the globe in a set of 35 icd codes. The theory being that once all of the conserved possible 
combinations leading to morbidity across the globe are determined, one may tentatively identify whether 
the underlying etiologies of these diseases or groups of diseases are genetic or environmental.

# The directory contains the module's executables and datafiles. It serves as a entry point for the application code.

Description of Programs:
-- "__init__.py": Entry point for the project script, calls your main application code: "pipeline.py" and "preprocess.py"
-- "pipeline.py": core program of the pipeline, calls preprocess.py if needed, implements the Apriori Algorithm, controls flow of information
-- "preprocess.py": pre-processing program, invoked if pipeline.py detects that the country data files have not been parsed
-- "../cached_scripts/": contains supplementary scripts created during the the developement process  

Description of Datafiles:
-- "Sex*": the resulting files after "preprocess.py" is called. These are the country files after they have been parsed  
---- by biological sex.
-- "mdlt*.csv": these datasets contain a country's mortality rate information for a range of ages for a set of icd codes 
  
Understanding Mortality and Aging
Center for the Study of Biological Complexity & Department of Computer Science
Labs of Dr. Tarynn Witten and Dr. Alberto
