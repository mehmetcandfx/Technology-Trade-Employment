import pandas as pd
import os
cwd=os.getcwd()#[:-4]
#print(cwd)
df18 = pd.read_csv(f'{cwd}/Data/Eurostat/csv/EARN_SES18_14.csv')
#df14 = pd.read_csv(f'{cwd}Data/Eurostat/csv/EARN_SES14_14.csv')
#df10 = pd.read_csv(f'{cwd}Data/Eurostat/csv/EARN_SES10_14.csv')
#df06 = pd.read_csv(f'{cwd}Data/Eurostat/csv/EARN_SES06_14.csv')

df18.describe(include='all')