# The directory contains the module's executable files. It serves as a entry point for the application code.

Description of Programs:
-- "__init__.py": Entry point for the project script, calls your main application code: "pipeline.py" and "preprocess.py"
-- "pipeline.py": core program of the pipeline, calls preprocess.py if needed, implements the Apriori Algorithm, controls flow of information
-- "preprocess.py": pre-processing program, invoked if pipeline.py detects that the country data files have not been parsed
-- "../cached_scripts/": contains supplementary scripts created during the the developement process  

  
