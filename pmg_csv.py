import sys
import re
import csv
import os
import pandas as pd

def pandasCombiner(files, isTest = False):
     dfs = [] # List of csv files converted to pandas data frames
     for file in files: # Iterate over each csv file
          if os.path.getsize(file) == 0: # Check for empty file
               raise Exception('Empty File Detected')
          with open(file) as f: # Opens the file
               df = pd.read_csv(f) # Convert csv to dataframe
               df['filename'] = [os.path.basename(file) for x in range(df.shape[0])] # Add 'filename' column
               dfs.append(df) # Add dataframe to list
     combined = pd.concat(dfs) # Combines the dataframes
     combinedDf = combined[[c for c in combined if c not in ['filename']] + ['filename']] # Makes'filename' column the last column (https://stackoverflow.com/questions/35321812/move-column-in-pandas-dataframe)
     if isTest: # Changes return type for tests
          return combinedDf 
     combinedCSV = combinedDf.to_csv('combined.csv', index=False, compression=None) # Sent to stdout
def iterativeCombiner(files, isTest = False):
     headers = [] # List of headers across all provided files
     numCols = [] # List of number of columns in each file
     sameHeaders = True # Check for same headers across all files
     disjointHeaders = True # Check for disjoint headers i.e. no files share a header
     for i in range(len(files)): # Iterate over each csv file
          if os.path.getsize(files[i]) == 0: # Check for empty file
               raise Exception('Empty File Detected')
          with open(files[i]) as f: # Opens the file
               reader = csv.reader(f) # Used to read file
               for r in reader: # Only retrieves the first line (the header)
                    numCols.append(len(r)) # Add row length to list
                    if headers == []: # Sets empty headers list to headers of first file, prevents triggering sameHeaders or disjointHeaders inappropriately
                         headers = r
                    for h in r: # Iterate over each header in the current file
                         if h not in headers: # Add new headers to list, new headers mean the headers for each file aren't the same
                              headers.append(h)
                              sameHeaders = False;
                         else: # If a new header is the same as a header already in the list, the headers for each file are not disjoint
                              disjointHeaders = False;
                    break # End loop after first iteration
     
     headers.append('filename') # Add 'filname' to list of headers
     curHeaders = [] # Headers for the current file
     combined = [] # List of lists that will be written to the csv
     
     if not isTest: # Headers should not be included in list of lists for testing purposes
          combined.append(headers) # Csv begins with headers
    
     for i in range(len(files)): # Iterate over each csv file
          with open(files[i]) as f: # Opens the file
               reader = csv.reader(f) # Used to read file
               header = True # Used to check if on first iteration
               if disjointHeaders: # Only calculate number of empty columns once
                    leftCols = sum(numCols[:(i-1)]) # Number of empty cells to the left
                    rightCols = sum(numCols[i:]) # Number of empty cells to the right
               for r in reader: # Iterate over each row in the file
                    curRow = ['' for x in range(len(headers)-1)] # Declare empty array of length equal to headers length (without added 'filename' column)
                    if header: # Check if first iteration
                         curHeaders = r # Updates curHeaders
                         header = False # Ensures curHeaders isn't incorrectly updated on furture iteartions
                    else:
                         if sameHeaders: # If headers are all the same, rows don't need to be iterated saving considerable time for large datasets that share headers
                              curRow = r
                         elif disjointHeaders: # Combined row is the current row bookended by empty cells for each column whose header is not in the current file
                              curRow = ['' for x in range(leftCols)] + r + ['' for x in range(rightCols)]
                         else: # Worst case scenario: When there is overlap between headers, processing is infeasible for large files ***
                              for c in r: # Iterate over each item in row
                                  curRow[headers.index(curHeaders[r.index(c)])] = c # Places the current item in the same column as its respective header
                         curRow.append(os.path.basename(files[i])) # Append filename to row (https://www.geeksforgeeks.org/python-program-to-get-the-file-name-from-the-file-path/)
                         combined.append(curRow) # Append row to the list of lists to be written to csv
                    curRow = [] # Reset curRow for next row
               curHeaders = [] # Reset curHeaders for next file
     if isTest: # Changes return type for tests
          return combined, headers
     with open('combined.csv', 'w', newline='') as f: # Create new combined.csv file (https://www.scaler.com/topics/how-to-create-a-csv-file-in-python/)
        writer = csv.writer(f) # Used to write file
        for r in combined: # Writes file row by row
            writer.writerow(r)
if __name__ == '__main__':
     if len(sys.argv) < 2: # Command line should include both this file, the optional 'pandas' parameter, and at least one csv file
          print("Usage: python3 path_to_this_file pandas(optional) path_to_input_file_1 path_to_input_file_2 ... path_to_input_file_N > file_name.csv") # Usage Message
     elif len(sys.argv) == 2 and sys.argv[1] == 'pandas': # Ensure user provided at least one csv along with 'pandas' parameter
          print("Usage: python3 pandas(optional) path_to_this_file path_to_input_file_1 path_to_input_file_2 ... path_to_input_file_N > file_name.csv") # Usage Message
     elif len(sys.argv) > 2 and sys.argv[1] == 'pandas': # Use pandas only if 'pandas' parameter is provided
          pandasCombiner(sys.argv[2:])
     else:
          iterativeCombiner(sys.argv[1:])

# Time Complexity, f = # files, n_i = # entries for file i, m_i = # columns for file i

# Same Headers: O(sum from 1 to f of f_i * m_i) + O(sum from 1 to f of f_i * n_i) = O(f(m + n))

# Overlapping Headers: O(sum from 1 to f of f_i * m_i) + O(sum from 1 to f of f_i * n_i * m_i) = O(fm(n + 1)) Too slow
            
# Disjoint Headers: O(sum from 1 to f of f_i * m_i) + O(sum from 1 to f of f_i * (n_i + m)) = O(f(2m + n))
