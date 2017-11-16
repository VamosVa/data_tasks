# Exercise: Model Validation Task 1
# 2-sample Kolmogorov Smirnov test

# os: This module provides a portable way of using operating system dependent functionality.
import os
# xlrd: Library for developers to extract data from Microsoft Excel (tm) spreadsheet files
import xlrd
# datetime: This module enables to acquire dates from MS Excel float data
import datetime
# scipy enables to perform KM test
from scipy.stats import ks_2samp

v = []
w = []

for path, subdirs, files in os.walk(r'C:\Users\Principal\Desktop'):
    for name in files:
        if 'TimeSeries' in name:        
            v.append(path)       # Now we have a list with all the directories and other list with all names of the files
            w.append(name)       # It is really useful if we have more MS Excel files.
# print(v)
# print (w)
values = []                      # This matrix reads the data from excel and keeps also the last 750 equity returns from the different equity underlyings.
for i in range(1008):            # In case of more than one MS excel file, it should be defined after command of the line 33.
    values.append([0]*8)
# Get Excel directory: This command selects the path for each excel file. Again, useful if there is more than one MS excel file.
for i in range(len(v)):
    exceptions = 0
    os.chdir(v[i])                                                                                                                    
# Open Excel and get its name: This command selects the file which is going to be inserted in the database                                                                                         
    we =  xlrd.open_workbook(w[i])                                      
    title = w[i]                                                                                                                                                                      
    # Get Excel sheet                                                                                        
    #ws1 = we.sheet_by_name('BAC')
    ws1 = we.sheet_by_index(0)
    for i in range(2,1009):                     # The dates from the first column are inserted in the matrix values.
        cell = ws1.cell_value(rowx=i, colx=0)   # type, <class 'xlrd.sheet.Cell'>
        cell_as_datetime = datetime.datetime(*xlrd.xldate_as_tuple(cell, we.datemode))
        values[i-1][0] = cell_as_datetime 
    values[0][0] = 'Date'                       # Titles of the different columns are inserted.
    values[0][1] = 'BAC'                        
    values[0][2] = 'MSFT'
    values[0][3] = 'AAPLE'
    for i in range(len(values) - 1):            # The following commands write in the matrix values the data of the equity undeerlyings.
        for j in range(1,4):
            values[i+1][j] = ws1.cell(i+2,j).value
    values[0][4] = 'Eq_return_BAC'              # Titles of the different columns are inserted.
    values[0][5] = 'Eq_return_MSFT'
    values[0][6] = 'Eq_return_AAPLE'
    values[0][7] = 'Date_return'
    for i in range(len(values) - 2):                        # They calculate the last 750 historical equity returns.
        for j in range(4,7):
            values[i+1][j] = (values[i+1][j-3] - values[i+2][j-3])/ values[i+2][j-3]
    for i in range(len(values) - 2):
        values[i+1][7] = values[i+2][0]        
    bac = []
    bac_1 = []
    msft = []
    msft_1 = []
    aaple = []
    aaple_1 = []    
    for i in range((len(values) - 2)/2):
        bac.append([0])                 #It contains the first half of the bac values
        bac_1.append([0])                #It contains the second half of the bac values 
        msft.append([0])                #It contains the first half of the msft values
        msft_1.append([0])               #It contains the second half of the msft values         
        aaple.append([0])               #It contains the first half of the aaple values
        aaple_1.append([0])              #It contains the second half of the aaple values 
    for i in range((len(values) - 2)/2):
        bac[i] = values[i+1][4]  
        msft[i] = values[i+1][5]         
        aaple[i] = values[i+1][6]
        bac_1[i] = values[i+504][4]  
        msft_1[i] = values[i+504][5]         
        aaple_1[i] = values[i+504][6]
    KM1 = ks_2samp(bac, bac_1)       # two sample KS test
    KM2 = ks_2samp(msft, msft_1)      # two sample KS test
    KM3 = ks_2samp(aaple, aaple_1)     # two sample KS test
    print(KM1)
    print(KM2)        
    print(KM3)    