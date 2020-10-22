import pandas as pd

df = pd.read_csv('companies.csv')
df.drop_duplicates(subset='company_name', keep=False, inplace=True)
df.to_csv('companies.csv', index=False)