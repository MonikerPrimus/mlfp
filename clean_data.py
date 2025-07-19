#Input: csv file of data
#This code finds what columns have above the threshold (configurable) of nan values and removes them
#Output: same csv file but with columns removed

import pandas as pd
import math
original_file_path = input("Enter the path to the data file: ") or '../2024HealthcareFiles/OP_DTL_RSRCH_PGYR2024_P06302025_06162025.csv'
#../2024HealthcareFiles/OP_DTL_RSRCH_PGYR2024_P06302025_06162025.csv

cleaned_csv = input("What would you like to name the cleaned data file? (default: cleaned_data.csv): ") or 'cleaned_data.csv'
print("\n \n ------------------Starting Data Cleaning process------------------ \n "  )
print("Cleaning data from: ", original_file_path)
print("Saving cleaned data to: ", cleaned_csv)
print("\n Please Wait...\n")
df = pd.read_csv(original_file_path, low_memory=False)
pd.reset_option('display.max_rows')
pd.options.display.max_columns = None

#Counts the number of Nans under each column and displays it in a list
counts_list = []
for name, current_column in df.items():
    count = 0
    for value in current_column:
        if type(value) is float:
            if math.isnan(value):
                count+= 1
    counts_list.append(count)

#Take the list of number of Nans for each columns
#And convert that list to a list of percentages of how much of each column  is NaN
percentages_list=[]
for current_count in counts_list:
    percentages_list.append(current_count / len(df) * 100)
    
#Format those percentages to remove extraneous decimal points
formatted_percentage_list = ["{:.1f}".format(percentage) for percentage in percentages_list]

#Find out which columns must be removed, and make a cleaned date frame 
list_of_column_names = []
for index, percentage in enumerate(formatted_percentage_list):
    if float(percentage) > 80.0: #Percentage Threshold of whether the column should be deleted
        list_of_column_names.append(df.columns[index])

cleaned_df = df.copy()
cleaned_df.drop(columns=list_of_column_names, inplace=True)
print("Task Complete \n \n")

print("\n \n ------------------Columns in original data set------------------ \n "  )
print (len(df.columns))
print("\n \n ------------------Columns in cleaned data set------------------ \n ")
print (len(cleaned_df.columns))
print("\n \n ------------------Headers in cleaned data set------------------ \n ")
print(list(cleaned_df.columns))

#Export csv
print("\n \n ------------------Exporting cleaned data set------------------ \n ")
print(" \n Please Stand By..... \n")
df.to_csv(cleaned_csv, index=False)  
print("CSV Created")
print("Task Complete \n \n")