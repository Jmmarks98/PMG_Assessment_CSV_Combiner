import unittest
import csv
import os
import sys
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal

from pmg_csv import pandasCombiner
from pmg_csv import iterativeCombiner

class TestCombiner(unittest.TestCase):
            
     def test_pandasCombiner(self):
          same_columns_test_files = ['/Users/jmarks/Desktop/PMG_Assessment/Same_Columns_CSVs/accessories.csv', # *** Change to directories to local test files
                                     '/Users/jmarks/Desktop/PMG_Assessment/Same_Columns_CSVs/clothing.csv',
                                     '/Users/jmarks/Desktop/PMG_Assessment/Same_Columns_CSVs/household_cleaners.csv']
          
          numRows = 0 # Sum of rows across files
          numCols = 0 # Sum of columns across files
          for file in same_columns_test_files: # Iterate over each csv file
               with open(file) as f: # Opens the file
                    df = pd.read_csv(f) # Convert csv to dataframe
                    numRows += df.shape[0]
                    numCols = df.shape[1] # All the above files should have the same columns
                    
          actual = pandasCombiner(same_columns_test_files, isTest = True) # Function Call
          
          self.assertEqual(actual.shape[0], numRows) # Check correct number of rows
          self.assertEqual(actual.shape[1], numCols+1) # Check correct number of columns

          ###############################################################################
          
          overlapping_columns_test_files = ['/Users/jmarks/Desktop/PMG_Assessment/Ovelapping_Columns_CSVs/accessories_O.csv', # *** Change to directories to local test files
                                            '/Users/jmarks/Desktop/PMG_Assessment/Ovelapping_Columns_CSVs/clothing_O.csv',
                                            '/Users/jmarks/Desktop/PMG_Assessment/Ovelapping_Columns_CSVs/household_cleaners_O.csv']
          overlapping_headers = [] # Sum of unique headers across files
          numRows = 0 # Sum of rows across files
          for file in overlapping_columns_test_files: # Iterate over each csv file
               with open(file) as f: # Opens the file
                    df = pd.read_csv(f) # Convert csv to dataframe
                    numRows += df.shape[0]
                    if overlapping_headers == []: # Setting list to first file's columns saves an iteration
                         overlapping_headers = list(df.columns)
                    else:
                         for c in list(df.columns): # Add new unique headers to list
                              if c not in overlapping_headers:
                                   overlapping_headers.append(c)
                                   
          actual = pandasCombiner(overlapping_columns_test_files, isTest = True) # Function Call
          
          self.assertEqual(actual.shape[0], numRows) # Check correct number of rows
          self.assertEqual(actual.shape[1], len(overlapping_headers)+1) # Check correct number of columns

          ###############################################################################

          disjoint_columns_test_files = ['/Users/jmarks/Desktop/PMG_Assessment/Disjoint_Columns_CSVs/accessories_D.csv', # *** Change to directories to local test files
                                         '/Users/jmarks/Desktop/PMG_Assessment/Disjoint_Columns_CSVs/clothing_D.csv',
                                         '/Users/jmarks/Desktop/PMG_Assessment/Disjoint_Columns_CSVs/household_cleaners_D.csv'] 
          numRows = 0 # Sum of rows across files
          numCols = 0 # Sum of columns across files
          for file in same_columns_test_files: # Iterate over each csv file
               with open(file) as f: # Opens the file
                    df = pd.read_csv(f) # Convert csv to dataframe
                    numRows += df.shape[0]
                    numCols += df.shape[1] # Number of columns is the sum of columns across files
                    
          actual = pandasCombiner(disjoint_columns_test_files, isTest = True) # Function call
          
          self.assertEqual(actual.shape[0], numRows) # Check correct number of rows
          self.assertEqual(actual.shape[1], numCols+1) # Check correct number of columns

          ###############################################################################

          empty_csv = '/Users/jmarks/Desktop/PMG_Assessment/empty_csv.csv' # Empty CSV generated using touch command

          self.assertRaises(Exception, pandasCombiner, empty_csv, isTest = True) # Check program recognizes and denies empty files
                    
     def test_iterativeCombiner(self):
          same_columns_test_files = ['/Users/jmarks/Desktop/PMG_Assessment/Same_Columns_CSVs/accessories.csv', # *** Change to directories to local test files
                                     '/Users/jmarks/Desktop/PMG_Assessment/Same_Columns_CSVs/clothing.csv',
                                     '/Users/jmarks/Desktop/PMG_Assessment/Same_Columns_CSVs/household_cleaners.csv']
          
          numRows = 0 # Sum of rows across files
          numCols = 0 # Sum of columns across files
          for file in same_columns_test_files: # Iterate over each csv file
               with open(file) as f: # Opens the file
                    df = pd.read_csv(f) # Convert csv to dataframe
                    numRows += df.shape[0]
                    numCols = df.shape[1] # All the above files should have the same columns
                    
          actual, actualHeaders = iterativeCombiner(same_columns_test_files, isTest = True) # Iterative Function Call
          
          expected = pandasCombiner(same_columns_test_files, isTest = True) # Pandas Function Call
          actualDf = pd.DataFrame(actual, columns = actualHeaders) # Convert list of lists to data frame for comparisons
          
          self.assertEqual(len(actual), numRows) # Check correct number of rows
          self.assertEqual(len(actual[0]), numCols+1) # Check correct number of columns
          assert_frame_equal(actualDf.reset_index(drop=True), expected.reset_index(drop=True)) # Check that iterativeCombiner returns the same result as pandasCombiner

          ###############################################################################
          
          overlapping_columns_test_files = ['/Users/jmarks/Desktop/PMG_Assessment/Ovelapping_Columns_CSVs/accessories_O.csv', # *** Change to directories to local test files
                                            '/Users/jmarks/Desktop/PMG_Assessment/Ovelapping_Columns_CSVs/clothing_O.csv',
                                            '/Users/jmarks/Desktop/PMG_Assessment/Ovelapping_Columns_CSVs/household_cleaners_O.csv']
          overlapping_headers = [] # Sum of unique headers across files
          numRows = 0 # Sum of rows across files
          for file in overlapping_columns_test_files: # Iterate over each csv file
               with open(file) as f: # Opens the file
                    df = pd.read_csv(f) # Convert csv to dataframe
                    numRows += df.shape[0]
                    if overlapping_headers == []: # Setting list to first file's columns saves an iteration
                         overlapping_headers = list(df.columns)
                    else:
                         for c in list(df.columns):
                              if c not in overlapping_headers:
                                   overlapping_headers.append(c)
                                   
          actual, actualHeaders = iterativeCombiner(overlapping_columns_test_files, isTest = True) # Iterative Function Call
          
          expected = pandasCombiner(overlapping_columns_test_files, isTest = True) # Pandas Function Call
          actualDf = pd.DataFrame(actual, columns = actualHeaders) # Convert list of lists to data frame for comparisons
          
          self.assertEqual(len(actual), numRows) # Check correct number of rows
          self.assertEqual(len(actual[0]), len(overlapping_headers)+1) # Check correct number of columns
          
          actualDf.replace('', np.nan, inplace=True) # Replaces '' for empty cells with NaN for comparison

          assert_frame_equal(actualDf.reset_index(drop=True), expected.reset_index(drop=True)) # Check that iterativeCombiner returns the same result as pandasCombiner

          ###############################################################################

          disjoint_columns_test_files = ['/Users/jmarks/Desktop/PMG_Assessment/Disjoint_Columns_CSVs/accessories_D.csv', # *** Change to directories to local test files
                                         '/Users/jmarks/Desktop/PMG_Assessment/Disjoint_Columns_CSVs/clothing_D.csv',
                                         '/Users/jmarks/Desktop/PMG_Assessment/Disjoint_Columns_CSVs/household_cleaners_D.csv'] 
          numRows = 0 # Sum of rows across files
          numCols = 0 # Sum of columns across files
          for file in same_columns_test_files: # Iterate over each csv file
               with open(file) as f: # Opens the file
                    df = pd.read_csv(f) # Convert csv to dataframe
                    numRows += df.shape[0]
                    numCols += df.shape[1] # All the above files should have the same columns
                    
          actual, actualHeaders = iterativeCombiner(disjoint_columns_test_files, isTest = True) # Iterative Function Call
          
          expected = pandasCombiner(disjoint_columns_test_files, isTest = True) # Pandas Function Call
          actualDf = pd.DataFrame(actual, columns = actualHeaders) # Convert list of lists to data frame for comparisons
          
          self.assertEqual(len(actual), numRows) # Check correct number of rows
          self.assertEqual(len(actual[0]), numCols+1) # Check correct number of columns

          actualDf.replace('', np.nan, inplace=True) # Replaces '' for empty cells with NaN for comparison
          
          assert_frame_equal(actualDf.reset_index(drop=True), expected.reset_index(drop=True)) # Check that iterativeCombiner returns the same result as pandasCombiner

          ###############################################################################

          empty_csv = '/Users/jmarks/Desktop/PMG_Assessment/empty_csv.csv' # Empty CSV generated using touch command

          self.assertRaises(Exception, iterativeCombiner, empty_csv, isTest = True) # Check program recognizes and denies empty files
if __name__ == '__main__':
    unittest.main()
        
