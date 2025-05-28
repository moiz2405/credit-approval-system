import pandas as pd

# Read and print Customer Data
customer_df = pd.read_excel("customer_data.xlsx")
print("Customer Data Columns:", customer_df.columns.tolist())
print(customer_df.head())  # Shows first few rows

# Read and print Loan Data
loan_df = pd.read_excel("loan_data.xlsx")
print("Loan Data Columns:", loan_df.columns.tolist())
print(loan_df.head())  # Shows first few rows
