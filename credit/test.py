import pandas as pd
df = pd.read_excel("customer_data.xlsx")
df.columns = df.columns.str.strip().str.lower()
print(df.columns.tolist())
df = pd.read_excel("loan_data.xlsx")
df.columns = df.columns.str.strip().str.lower()
print(df.columns.tolist())