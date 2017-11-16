# Exercise: Model Validation Task 2

# os: This module provides a portable way of using operating system dependent functionality.
import os
# xlrd: Library for developers to extract data from Microsoft Excel (tm) spreadsheet files
import xlrd
# re: The re module provides Perl-style regular expression patterns.
import re
# datetime: This module enables to acquire dates from MS Excel float data
import datetime
# math provides mathematical calculations as exponentials and ln
from math import exp, log, pow, sqrt
# norm.cdf enables the possibility of calculating N(0,1) cumulative distribution funtion
from scipy.stats import norm
from datetime import datetime
start=datetime.now()




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
    date_exception = []
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
    for i in range(750):                        # They calculate the last 750 historical equity returns.
        for j in range(4,7):
            values[i+1][j] = (values[i+1][j-3] - values[i+2][j-3])/ values[i+2][j-3]
    for i in range(len(values) - 2):
        values[i+1][7] = values[i+2][0]



# The following commands calculate for each underlying and historical date 750 tomorrow's equity price.
# In other words, each historical date of the last 750 days contains 750 hypotheticaltomorrow price.
# Thus, we use 3 matrix, one for each equity underlying.

    bac_tomorrow = []
    msft_tomorrow = []
    aaple_tomorrow = []

# Each matrix will contain the equity price, its equity return and next to theese two columns, 750 hyphotetical prices.

    for i in range(752):                            # Creation of 3 empty matrices to be filled.
        bac_tomorrow.append([0]*752)
        msft_tomorrow.append([0]*752)
        aaple_tomorrow.append([0]*752)
    for i in range(751):                            # Insertion of equity price and return in the corresponding matrices.
        bac_tomorrow[i+1][0] = values[i+1][1]
        bac_tomorrow[i+1][1] = values[i+1][4]
        msft_tomorrow[i+1][0] = values[i+1][2]
        msft_tomorrow[i+1][1] = values[i+1][5]
        aaple_tomorrow[i+1][0] = values[i+1][3]
        aaple_tomorrow[i+1][1] = values[i+1][6]
    
    bac_tomorrow[0][0] = 'BAC'                      # Column names of the matrices
    msft_tomorrow[0][0] = 'MSFT'
    aaple_tomorrow[0][0] = 'AAPLE'
    bac_tomorrow[0][1] = 'Eq_return_BAC'
    msft_tomorrow[0][1] = 'Eq_return_MSFT'
    aaple_tomorrow[0][1] = 'Eq_return_AAPLE'
    
    for j in range(2, 752):                         # Column names of the matrices (750 hypothetical prices)
        bac_tomorrow[0][j] = 'hypothetical price' + str(j-1)
        msft_tomorrow[0][j] = 'hypothetical price' + str(j-1)        
        aaple_tomorrow[0][j] = 'hypothetical price' + str(j-1)
        
    for i in range(750):                            # With the following calculations, we obtain the 750 hyphothetical prices for each day and for each equity.
        for j in range(2,752):
            bac_tomorrow[i+1][j] = bac_tomorrow[i+2][0]*(bac_tomorrow[j-1][1] + 1)
            msft_tomorrow[i+1][j] = msft_tomorrow[i+2][0]*(msft_tomorrow[j-1][1] + 1)
            aaple_tomorrow[i+1][j] = aaple_tomorrow[i+2][0]*(aaple_tomorrow[j-1][1] + 1)

            
# The next steps are the calculación of the value of the actual and the hypothetical portfolios.
# Thus, before proceeding, we need to know the time of maturity for each day.

# The working days between the last day of our historical data (30.04 April) and 2nd March 2015 are 218 days. Taking into account
# 9 days that NASDAQ is closed, the final number of working days is 209

    working_days_final = 209
    maturity_years = []
    for i in range(751):                            # Creation of a matrix that will contain the days of maturity
        maturity_years.append([0]*2)
    maturity_years[0][0] = 'Date'
    maturity_years[0][1] = 'time_to_maturity'
    for i in range(750):
        maturity_years[i+1][0] = values[i+1][7]
        maturity_years[i+1][1] = (working_days_final + int(i))/250.0
        
    bac_portfolio_price = []                        # Creation of a matrix that will contain the parameters to calculate the portfolio prices and also the portfolio prices (Today's portfolio price)
    msft_portfolio_price = []
    aaple_portfolio_price = []
    
    
    # r = 0.03, q = 0.01, sigma = 0.2
    # r - q = 0.02    
    for i in range(751):                            # This matrix contains BAC today's price for the last 750 historical dates and we perform different operations to obtain
        bac_portfolio_price.append([0]*6)           # F, d1, d2, N(d1), N(d2) parameters and option price.
    bac_portfolio_price[0][0] = 'F'
    bac_portfolio_price[0][1] = 'd1'
    bac_portfolio_price[0][2] = 'd2'
    bac_portfolio_price[0][3] = 'N(d1)'
    bac_portfolio_price[0][4] = 'N(d2)'
    bac_portfolio_price[0][5] = 'P'
    for i in range(750):                            
        bac_portfolio_price[i+1][0] = values[i+2][1]*exp(0.02*maturity_years[i+1][1])
        bac_portfolio_price[i+1][1] = (1.0/(0.2*sqrt(maturity_years[i+1][1])))*((log(bac_portfolio_price[i+1][0]/16.0)) + ((pow(0.2,2)/2.0)*maturity_years[i+1][1]))
        bac_portfolio_price[i+1][2] = bac_portfolio_price[i+1][1] - (0.2*sqrt(maturity_years[i+1][1]))
        bac_portfolio_price[i+1][3] = norm.cdf(bac_portfolio_price[i+1][1]) 
        bac_portfolio_price[i+1][4] = norm.cdf(bac_portfolio_price[i+1][2])    
        bac_portfolio_price[i+1][5] = (exp(-0.03*maturity_years[i+1][1]))*((bac_portfolio_price[i+1][0]*bac_portfolio_price[i+1][3]) - (16*bac_portfolio_price[i+1][4]))   


   
    for i in range(751):                            # This matrix contains MSFT today's price for the last 750 historical dates and we perform different operations to obtain  
        msft_portfolio_price.append([0]*6)          # F, d1, d2, N(d1), N(d2) parameters and option price. 
    msft_portfolio_price[0][0] = 'F'
    msft_portfolio_price[0][1] = 'd1'
    msft_portfolio_price[0][2] = 'd2'
    msft_portfolio_price[0][3] = 'N(d1)'
    msft_portfolio_price[0][4] = 'N(d2)'
    msft_portfolio_price[0][5] = 'P'
    for i in range(750):
        msft_portfolio_price[i+1][0] = values[i+2][2]*exp(0.02*maturity_years[i+1][1])
        msft_portfolio_price[i+1][1] = (1.0/(0.2*sqrt(maturity_years[i+1][1])))*((log(msft_portfolio_price[i+1][0]/40.0)) + ((pow(0.2,2)/2.0)*maturity_years[i+1][1]))
        msft_portfolio_price[i+1][2] = msft_portfolio_price[i+1][1] - (0.2*sqrt(maturity_years[i+1][1]))
        msft_portfolio_price[i+1][3] = norm.cdf(-msft_portfolio_price[i+1][1]) 
        msft_portfolio_price[i+1][4] = norm.cdf(-msft_portfolio_price[i+1][2])    
        msft_portfolio_price[i+1][5] = (exp(-0.03*maturity_years[i+1][1]))*(((40*msft_portfolio_price[i+1][4]) - msft_portfolio_price[i+1][0]*msft_portfolio_price[i+1][3]))
        

    
    for i in range(751):                            # This matrix contains AAPLE today's price for the last 750 historical dates and we perform different operations to obtain
        aaple_portfolio_price.append([0]*6)         # F, d1, d2, N(d1), N(d2) parameters and option price. 
    aaple_portfolio_price[0][0] = 'F'
    aaple_portfolio_price[0][1] = 'd1'
    aaple_portfolio_price[0][2] = 'd2'
    aaple_portfolio_price[0][3] = 'N(d1)'
    aaple_portfolio_price[0][4] = 'N(d2)'
    aaple_portfolio_price[0][5] = 'P'
    for i in range(750):
        aaple_portfolio_price[i+1][0] = values[i+2][3]*exp(0.02*maturity_years[i+1][1])
        aaple_portfolio_price[i+1][1] = (1.0/(0.2*sqrt(maturity_years[i+1][1])))*((log(aaple_portfolio_price[i+1][0]/600.0)) + ((pow(0.2,2)/2.0)*maturity_years[i+1][1]))
        aaple_portfolio_price[i+1][2] = aaple_portfolio_price[i+1][1] - (0.2*sqrt(maturity_years[i+1][1]))
        aaple_portfolio_price[i+1][3] = norm.cdf(aaple_portfolio_price[i+1][1]) 
        aaple_portfolio_price[i+1][4] = norm.cdf(aaple_portfolio_price[i+1][2])    
        aaple_portfolio_price[i+1][5] = (exp(-0.03*maturity_years[i+1][1]))*((aaple_portfolio_price[i+1][0]*aaple_portfolio_price[i+1][3]) - (600*aaple_portfolio_price[i+1][4]))    
        
    portfolio_price = []            # To obtain the 750 current portfolio values of the 750 historical dates,
    for i in range(751):            # we have calculated the option price of each equity and then these prices are multiplied by the number of options the portfolio has.
        portfolio_price.append([0])
    portfolio_price[0] = 'portfolio_price'
    for i in range(750):
        portfolio_price[i+1] = (100*bac_portfolio_price[i+1][5]) + (30*msft_portfolio_price[i+1][5]) + (3*aaple_portfolio_price[i+1][5])
    
    
# Now we obtain the hypothetical prices for each historical date
    fut_bac_portfolio_price = []                        # Creation of a matrix that will contain the parameters to calculate the portfolio prices and also the portfolio prices (Today's portfolio price)
    fut_msft_portfolio_price = []
    fut_aaple_portfolio_price = []
    fut_portfolio_price = []
        
    
#### BAC ####    
    param_f_bac_portfolio_price = []   
    param_d1_bac_portfolio_price = []
    param_d2_bac_portfolio_price = []
    param_n_d1_bac_portfolio_price = []
    param_n_d2_bac_portfolio_price = []
    param_p_bac_portfolio_price = []                # It contains BAC call option price of 750 hypothetical tomorrow price for the 750 last values (in other words, 750 x 750)
    for i in range(751):                            # This matrix contains BAC today's price for the last 750 historical dates
        param_f_bac_portfolio_price.append([0]*750)
        param_d1_bac_portfolio_price.append([0]*750)
        param_d2_bac_portfolio_price.append([0]*750)
        param_n_d1_bac_portfolio_price.append([0]*750)
        param_n_d2_bac_portfolio_price.append([0]*750)
        param_p_bac_portfolio_price.append([0]*750)
    for i in range(750):                            # Now, F, d1, d2, N(d1), N(d2) parameters and option price are calculated
        for j in range(750):
            param_f_bac_portfolio_price[i+1][j] = bac_tomorrow[i+1][j+2]*exp(0.02*maturity_years[i+1][1])
            param_d1_bac_portfolio_price[i+1][j] = (1.0/(0.2*sqrt(maturity_years[i+1][1])))*((log(param_f_bac_portfolio_price[i+1][j]/16.0)) + ((pow(0.2,2)/2.0)*maturity_years[i+1][1]))
            param_d2_bac_portfolio_price[i+1][j] = param_d1_bac_portfolio_price[i+1][j] - (0.2*sqrt(maturity_years[i+1][1]))
            param_n_d1_bac_portfolio_price[i+1][j] = norm.cdf(param_d1_bac_portfolio_price[i+1][j]) 
            param_n_d2_bac_portfolio_price[i+1][j] = norm.cdf(param_d2_bac_portfolio_price[i+1][j])    
            param_p_bac_portfolio_price[i+1][j] = (exp(-0.03*maturity_years[i+1][1]))*((param_f_bac_portfolio_price[i+1][j]*param_n_d1_bac_portfolio_price[i+1][j]) - (16*param_n_d2_bac_portfolio_price[i+1][j]))    

  
#### MSFT ####    
    param_f_msft_portfolio_price = []   
    param_d1_msft_portfolio_price = []
    param_d2_msft_portfolio_price = []
    param_n_d1_msft_portfolio_price = []
    param_n_d2_msft_portfolio_price = []
    param_p_msft_portfolio_price = []               # It contains MSFT put option price of 750 hypothetical tomorrow price for the 750 last values (in other words, 750 x 750)
    for i in range(751):                            # This matrix contains BAC today's price for the last 750 historical dates
        param_f_msft_portfolio_price.append([0]*750)
        param_d1_msft_portfolio_price.append([0]*750)
        param_d2_msft_portfolio_price.append([0]*750)
        param_n_d1_msft_portfolio_price.append([0]*750)
        param_n_d2_msft_portfolio_price.append([0]*750)
        param_p_msft_portfolio_price.append([0]*750)
    for i in range(750):                            # Now, F, d1, d2, N(d1), N(d2) parameters and option price are calculated
        for j in range(750):
            param_f_msft_portfolio_price[i+1][j] = msft_tomorrow[i+1][j+2]*exp(0.02*maturity_years[i+1][1])
            param_d1_msft_portfolio_price[i+1][j] = (1.0/(0.2*sqrt(maturity_years[i+1][1])))*((log(param_f_msft_portfolio_price[i+1][j]/40.0)) + ((pow(0.2,2)/2.0)*maturity_years[i+1][1]))
            param_d2_msft_portfolio_price[i+1][j] = param_d1_msft_portfolio_price[i+1][j] - (0.2*sqrt(maturity_years[i+1][1]))
            param_n_d1_msft_portfolio_price[i+1][j] = norm.cdf(-param_d1_msft_portfolio_price[i+1][j]) 
            param_n_d2_msft_portfolio_price[i+1][j] = norm.cdf(-param_d2_msft_portfolio_price[i+1][j])    
            param_p_msft_portfolio_price[i+1][j] = (exp(-0.03*maturity_years[i+1][1]))*((40*param_n_d2_msft_portfolio_price[i+1][j]) - (param_f_msft_portfolio_price[i+1][j]*param_n_d1_msft_portfolio_price[i+1][j]))
    
    
#### AAPLE ####    
    param_f_aaple_portfolio_price = []   
    param_d1_aaple_portfolio_price = []
    param_d2_aaple_portfolio_price = []
    param_n_d1_aaple_portfolio_price = []
    param_n_d2_aaple_portfolio_price = []
    param_p_aaple_portfolio_price = []              # It contains AAPLE call option price of 750 hypothetical tomorrow price for the 750 last values (in other words, 750 x 750)
    for i in range(751):                            # This matrix contains BAC today's price for the last 750 historical dates
        param_f_aaple_portfolio_price.append([0]*750)
        param_d1_aaple_portfolio_price.append([0]*750)
        param_d2_aaple_portfolio_price.append([0]*750)
        param_n_d1_aaple_portfolio_price.append([0]*750)
        param_n_d2_aaple_portfolio_price.append([0]*750)
        param_p_aaple_portfolio_price.append([0]*750)
    for i in range(750):                            # Now, F, d1, d2, N(d1), N(d2) parameters and option price are calculated
        for j in range(750):
            param_f_aaple_portfolio_price[i+1][j] = aaple_tomorrow[i+1][j+2]*exp(0.02*maturity_years[i+1][1])
            param_d1_aaple_portfolio_price[i+1][j] = (1.0/(0.2*sqrt(maturity_years[i+1][1])))*((log(param_f_aaple_portfolio_price[i+1][j]/600.0)) + ((pow(0.2,2)/2.0)*maturity_years[i+1][1]))
            param_d2_aaple_portfolio_price[i+1][j] = param_d1_aaple_portfolio_price[i+1][j] - (0.2*sqrt(maturity_years[i+1][1]))
            param_n_d1_aaple_portfolio_price[i+1][j] = norm.cdf(param_d1_aaple_portfolio_price[i+1][j]) 
            param_n_d2_aaple_portfolio_price[i+1][j] = norm.cdf(param_d2_aaple_portfolio_price[i+1][j])    
            param_p_aaple_portfolio_price[i+1][j] = (exp(-0.03*maturity_years[i+1][1]))*((param_f_aaple_portfolio_price[i+1][j]*param_n_d1_aaple_portfolio_price[i+1][j]) - (600*param_n_d2_aaple_portfolio_price[i+1][j]))
    
#####

# These commands entitle the columns of the tables
    for i in range(750):
        param_f_bac_portfolio_price[0][i] = 'F' + str(i)  
        param_d1_bac_portfolio_price[0][i] = 'd1-' + str(i)
        param_d2_bac_portfolio_price[0][i] = 'd2-' + str(i)
        param_n_d1_bac_portfolio_price[0][i] = 'N(d1)-' + str(i)
        param_n_d2_bac_portfolio_price[0][i] = 'N(d2)-' + str(i)
        param_p_bac_portfolio_price[0][i] = 'P' + str(i)
        param_f_msft_portfolio_price[0][i] = 'F' + str(i) 
        param_d1_msft_portfolio_price[0][i] = 'd1-' + str(i)
        param_d2_msft_portfolio_price[0][i] = 'd2-' + str(i)
        param_n_d1_msft_portfolio_price[0][i] = 'N(d1)-' + str(i)
        param_n_d2_msft_portfolio_price[0][i] = 'N(d2)-' + str(i)
        param_p_msft_portfolio_price[0][i] = 'P' + str(i)
        param_f_aaple_portfolio_price[0][i] = 'F' + str(i)
        param_d1_aaple_portfolio_price[0][i] = 'd1-' + str(i)
        param_d2_aaple_portfolio_price[0][i] = 'd2-' + str(i)
        param_n_d1_aaple_portfolio_price[0][i] = 'N(d1)-' + str(i)
        param_n_d2_aaple_portfolio_price[0][i] = 'N(d2)-' + str(i)
        param_p_aaple_portfolio_price[0][i] = 'P' + str(i)

#####
# Let's calculate now the 750 portfolio values for each historical date of the last three years

    for i in range(751):
        fut_bac_portfolio_price.append([0]*751)
        fut_msft_portfolio_price.append([0]*751)
        fut_aaple_portfolio_price.append([0]*751)
        fut_portfolio_price.append([0]*751)
    for i in range(750):
        fut_bac_portfolio_price[0][i+1] = 'BAC_portfolio_price ' + str(i)
        fut_msft_portfolio_price[0][i+1] = 'MSFT_portfolio_price ' + str(i)             
        fut_aaple_portfolio_price[0][i+1] = 'AAPLE_portfolio_price ' + str(i)
        fut_portfolio_price[0][i+1] = 'hyp_portfolio_price ' + str(i)
        fut_bac_portfolio_price[i+1][0] = values[i+1][7]                  # Copying dates
        fut_msft_portfolio_price[i+1][0] = values[i+1][7]                 # Copying dates
        fut_aaple_portfolio_price[i+1][0] = values[i+1][7]                # Copying dates
        fut_portfolio_price[i+1][0] = values[i+1][7]                      # Copying dates  
        for j in range(750):
            fut_bac_portfolio_price[i+1][j+1] = 100*param_p_bac_portfolio_price[i+1][j]     # We multiply the option price by the number of options
            fut_msft_portfolio_price[i+1][j+1] = 30*param_p_msft_portfolio_price[i+1][j]    # We multiply the option price by the number of options
            fut_aaple_portfolio_price[i+1][j+1] = 3*param_p_aaple_portfolio_price[i+1][j]   # We multiply the option price by the number of options
        
    for i in range(750):
        for j in range(750):
            fut_portfolio_price[i+1][j+1] = (fut_bac_portfolio_price[i+1][j+1]) + (fut_msft_portfolio_price[i+1][j+1]) + (fut_aaple_portfolio_price[i+1][j+1])  #Finally, we obtain the portfolio value 
        
        
####
# Hypothetical PnL, hyp_pnl = fut_portfolio_price - portfolio_price
    hyp_pnl = []
    for i in range(751):
        hyp_pnl.append([0]*751)
    hyp_pnl[0][0] = 'Date'
    for i in range(750):
        hyp_pnl[0][i+1] = 'hyp_pnl' + str (i+1)
        hyp_pnl[i+1][0] = values[i+1][7]
        for j in range(750):
            hyp_pnl[i+1][j+1] = fut_portfolio_price[i+1][j+1] - portfolio_price[i+1]
    
    hyp_pnl_plus = []
    for i in range(750):
        hyp_pnl.append([0]*750)
    hyp_pnl_sorted = []
    for i in range(750):
        hyp_pnl.append([0]*750)

    # Following calculations give us the portfolio value for the 1st May 2014 (maturity: 208/250 = 0.832)
    bac_portfolio_price0 = 15.09*exp(0.02*0.832)
    bac_portfolio_price1 = (1.0/(0.2*sqrt(0.832)))*((log(bac_portfolio_price0/16.0)) + ((pow(0.2,2)/2.0)*0.832))
    bac_portfolio_price2 = bac_portfolio_price1 - (0.2*sqrt(0.832))
    bac_portfolio_price3 = norm.cdf(bac_portfolio_price1) 
    bac_portfolio_price4 = norm.cdf(bac_portfolio_price2)    
    bac_portfolio_price5 = (exp(-0.03*0.832))*((bac_portfolio_price0*bac_portfolio_price3) - (16*bac_portfolio_price4))

    msft_portfolio_price0 = 40.0*exp(0.02*0.832)
    msft_portfolio_price1 = (1.0/(0.2*sqrt(0.832)))*((log(msft_portfolio_price0/40.0)) + ((pow(0.2,2)/2.0)*0.832))
    msft_portfolio_price2 = msft_portfolio_price1 - (0.2*sqrt(0.832))
    msft_portfolio_price3 = norm.cdf(-msft_portfolio_price1) 
    msft_portfolio_price4 = norm.cdf(-msft_portfolio_price2)    
    msft_portfolio_price5 = (exp(-0.03*0.832))*(((40*msft_portfolio_price4) - msft_portfolio_price0*msft_portfolio_price3))
    
    aaple_portfolio_price0 = 591.48*exp(0.02*0.832)
    aaple_portfolio_price1 = (1.0/(0.2*sqrt(0.832)))*((log(aaple_portfolio_price0/600)) + ((pow(0.2,2)/2.0)*0.832))
    aaple_portfolio_price2 = aaple_portfolio_price1 - (0.2*sqrt(0.832))
    aaple_portfolio_price3 = norm.cdf(aaple_portfolio_price1) 
    aaple_portfolio_price4 = norm.cdf(aaple_portfolio_price2)    
    aaple_portfolio_price5 = (exp(-0.03*0.832))*((aaple_portfolio_price0*aaple_portfolio_price3) - (600*aaple_portfolio_price4))
    
    
    portfolio_price_01_05_2014 = (100*bac_portfolio_price5) + (30*msft_portfolio_price5) + (3*aaple_portfolio_price5)


    # The following step is to sort the hyp_pnl matrix from low to high values and choose the 1% percentile value (1% = 7.5 = 8)

    for i in range(750):
        hyp_pnl_plus.append([0]*750)
    for i in range(750):
        hyp_pnl_sorted.append([0]*750)
    for i in range(750):
        for j in range(750):
            hyp_pnl_plus[i][j] = hyp_pnl[i+1][j+1]
    for i in range(750):
        hyp_pnl_sorted[i] = sorted(hyp_pnl_plus[i])
    _VAR = []
    for i in range(750):    # VAR values for each historical date
        _VAR.append([0])
        _VAR[i] = hyp_pnl_sorted[i][7]
# The values of the portfolio from 01.05.13 to 30.04.2014 are
# the values from the 1st to the 252th. The value of 01.05.14 is PORTFOLIO_PRICE_01_05_2014
    actual_pnl_vs_var = []                          # This matrix contains the actual PNL, the VAR, the exceptions and the Dates
    for i in range(253):
        actual_pnl_vs_var.append([0]*4)
    actual_pnl_vs_var[0][0] = 'Actual PNL'
    actual_pnl_vs_var[0][1] = 'VAR'       
    actual_pnl_vs_var[0][2] = 'Exceptions'
    actual_pnl_vs_var[0][3] = 'Dates'
    actual_pnl_vs_var[1][0] = portfolio_price[1] - portfolio_price_01_05_2014   
    for i in range(251):
        actual_pnl_vs_var[i+2][0] = portfolio_price[i+2] - portfolio_price[i+1]
    for i in range(252):
        actual_pnl_vs_var[i+1][1] = _VAR[i]
        actual_pnl_vs_var[i+1][2] = actual_pnl_vs_var[i+1][0] - actual_pnl_vs_var[i+1][1]
        actual_pnl_vs_var[i+1][3] = values[i+1][7]
    for i in range(252):
        if actual_pnl_vs_var[i+1][2] < 0:
            exceptions += 1
            date_exception.append(values[i+1][7])
print('There are ' + str(exceptions) + ' exceptions. The exceptions took place for the portfolio values of the dates:\n\n')
for i in range(len(date_exception)):
    print(date_exception[i])

print('Calculation time is ' + datetime.now()-start + 'f')