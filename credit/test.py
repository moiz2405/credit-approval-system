import pandas as pd
df = pd.read_excel("customer_data.xlsx")
df.columns = df.columns.str.strip().str.lower().str.strip("'\"")
print([repr(col) for col in df.columns])


df = pd.read_excel("loan_data.xlsx")
df.columns = df.columns.str.strip().str.lower().str.strip("'\"")
print(df.columns.tolist())