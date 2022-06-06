import pandas as pd
from os.path import exists


df = pd.read_csv('big_dataset.csv')
df_1 = pd.read_csv('2020.csv')
df_2 = pd.read_csv('2021.csv')
df = pd.concat([df, df_1])
df = pd.concat([df, df_2])

df = df.drop_duplicates()
print(df.shape)

df.to_csv('big_dataset.csv', index=False)
