# import pandas as pd

# # Read the CSV file with a header
# csv_data = pd.read_csv('C:/Users/carolvfs/Documents/GitHub/python_scripts/hrrr_to_anylogic_format/temperature_2024-09-23_day.csv')

# # Read the Excel file without a header
# excel_data = pd.read_excel('C:/Users/carolvfs/Downloads/VerifyDataPointsDay_2024_09_23.xlsx', header=None)

# # Assign the column names from the CSV to the Excel data
# excel_data.columns = csv_data.columns

# # Compare the two DataFrames
# if excel_data.equals(csv_data):
#     print("The Excel and CSV files are identical.")
# else:
#     print("The Excel and CSV files have differences.")

import pandas as pd

# Read the CSV file with a header
csv_data = pd.read_csv('C:/Users/carolvfs/Documents/GitHub/python_scripts/hrrr_to_anylogic_format/temperature_2024-09-23_day.csv')

# Read the Excel file without a header
excel_data = pd.read_excel('C:/Users/carolvfs/Downloads/VerifyDataPointsDay_2024_09_23.xlsx', header=None)

# Assign the column names from the CSV to the Excel data
excel_data.columns = csv_data.columns

# Function to find and print the first difference
def find_first_difference(df1, df2):
    for i in range(len(df1)):
        for col in df1.columns:
            if df1.at[i, col] != df2.at[i, col]:
                print(f"First difference found at row {i + 1}, column '{col}':")
                print(f"Excel file value: {df1.at[i, col]}")
                print(f"CSV file value: {df2.at[i, col]}")
                return
    print("No differences found.")

# Check if DataFrames are identical, if not, find the first difference
if excel_data.equals(csv_data):
    print("The Excel and CSV files are identical.")
else:
    find_first_difference(excel_data, csv_data)
