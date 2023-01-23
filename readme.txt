
CSV Combiner developed by Jacob Marks for PMG Technical Assessment

This application can be run from the command line as follows:

	python3 <path-to-pmg-csv-file> <optional pandas parameter> <path-to-csv-1> <path-to-csv-2> ... <path-to-csv-N>

The combiner can be run in two modes, either iteratively or using pandas data frames. The iterative method is the default and the pandas parameter should be included to use the data frame method, which is recommended for large or numerous files with overlapping columns.

Unit Tests can be run from the command line as follows:
	
python3 -m unittest <path-to-testing-file>

Unit tests check the dimensions of the returned csv, check that the returned csv is equivalent to that produced by pandas.concat, and check that the program rejects empty files

NOTE: The directory to the example files used for testing needs to be updated to match the location of the files or other files you wish to use for testing on your machine. Where these changes need to be made in the testing file are marked with ***. Be careful that the CSVs used for each test are the appropriate type (e.g. identical columns, overlapping columns, or disjoint columns) to ensure test effectiveness. 

