# preptools.py

import pandas as pd
import numpy as np
import os
import eurostat


def wage_getter():
    EARN_SES_47=["EARN_SES06_47","EARN_SES10_47","EARN_SES14_47","EARN_SES18_47"]
    df=pd.concat([eurostat.get_data_df(j, flags=True).assign(year=2006+4*i) for i, j in enumerate(EARN_SES_47)],ignore_index=True)
    df=df[(df['sex']=='T')&(df['indic_se']=='ERN')&(df['sizeclas']=='GE10')]
    df=df.drop(['freq','sex','indic_se','sizeclas'], axis=1)
    df=df.rename(columns={'geo\TIME_PERIOD':'code'})
    df['unit']=df['unit'].replace(np.nan, '', regex=True)+df['currency'].replace(np.nan, '', regex=True)
    df=df.drop(['currency'], axis=1)
    df=df[(df['unit']!= 'NAC')]
    df['value']=df['2006_value'].replace(np.nan, 0, regex=True)+df['2010_value'].replace(np.nan, 0, regex=True)+df['2014_value'].replace(np.nan, 0, regex=True)+df['2018_value'].replace(np.nan, 0, regex=True)
    df=df.drop(['2006_value','2010_value','2014_value','2018_value'], axis=1)
    df['flag']=df['2006_flag'].replace(np.nan, '', regex=True)+df['2010_flag'].replace(np.nan, '', regex=True)+df['2014_flag'].replace(np.nan, '', regex=True)+df['2018_flag'].replace(np.nan, '', regex=True)
    df=df.drop(['2006_flag','2010_flag','2014_flag','2018_flag'], axis=1)
    occupation=pd.DataFrame({
    'isco88': ['ISCO0', 'ISCO1', 'ISCO1-5', 'ISCO2', 'ISCO3', 'ISCO4', 'ISCO5', 'ISCO6', 'OC6-8', 'ISCO7', 'ISCO7-9', 'ISCO8', 'ISCO9','TOTAL'],
    'isco08': ['OC0', 'OC1', 'OC1-5', 'OC2', 'OC3', 'OC4', 'OC5', 'OC6', 'OC6-8', 'OC7', 'OC7-9', 'OC8', 'OC9','TOTAL'],
    'Description': ['Armed forces occupations', 'Managers', 'Non manual workers', 'Professionals', 'Technicians and associate professionals', 'Clerical support workers', 'Service and sales workers', 'Skilled agricultural, forestry and fishery workers', 'Skilled manual workers', 'Craft and related trades workers', 'Manual workers', 'Plant and machine operators and assemblers', 'Elementary occupations','Total']
            })
    df['isco88']=df['isco88'].map(occupation.set_index('isco88')['isco08'])
    df['isco08']=df['isco88'].replace(np.nan, '', regex=True)+df['isco08'].replace(np.nan, '', regex=True)
    s=[['A', 'A', 'Agriculture, forestry and fishing'],['C', 'B', 'Mining and quarrying'],['D', 'C', 'Manufacturing'],['E', 'D', 'Electricity, gas, steam and air conditioning supply'],['E', 'E', 'Water supply, sewerage, waste management and remediation activities'],['F', 'F', 'Construction'],['G', 'G', 'Wholesale and retail trade; repair of motor vehicles and motorcycles'],['H', 'I', 'Accommodation and food service activities'],['I', 'H', 'Transportation and storage'],['I', 'J', 'Information and communication'],['J', 'K', 'Financial and insurance activities'],['K', 'L', 'Real estate activities'],['K', 'M', 'Professional, scientific and technical activities'],['K', 'N', 'Administrative and support service activities'],['L', 'O', 'Public administration and defence; compulsory social security'],['M', 'P', 'Education'],['N', 'Q', 'Human health and social work activities'],['O', 'R', 'Arts, entertainment and recreation'],['O', 'S', 'Other service activities'],['P', 'T', 'Activities of households as employers; undifferentiated goods- and services-producing activities of households for own use'],['Q', 'U', 'Activities of extraterritorial organisations and bodies']]
    sector = pd.DataFrame(s,columns=['nace_r1', 'nace_r2', 'description'])
    df['dummy']=df['nace_r1'].map({item[0]: item[1] for item in s})
    df['nace_r2']=df['dummy'].replace(np.nan, '', regex=True)+df['nace_r2'].replace(np.nan, '', regex=True)
    df=df.drop(['isco88','nace_r1','dummy'], axis=1)
    df=df.set_index(['code','nace_r2','year'])

    return df
    

def trade_getter():
    df=eurostat.get_data_df('EXT_STEC01', flags=True)
    df=df[(df['partner']=='WORLD')&(df['sizeclas']=='TOTAL')]
    df=df.drop(['freq','sizeclas','partner'], axis=1)
    df=df.rename(columns={'geo\TIME_PERIOD':'code'})
    df_temp = df.melt(id_vars=['nace_r2','stk_flow','unit','code'], var_name='Cols')
    df_temp['year'],df_temp['Cols']=df_temp['Cols'].apply(lambda x : x[0:4]),df_temp['Cols'].apply(lambda x : x[5:])
    df=df_temp[(df_temp['Cols']=='value')].merge(df_temp[(df_temp['Cols']=='flag')],on=['nace_r2','stk_flow','unit','code','year'],how='outer').rename(columns={'value_x':'value','value_y':'flag'})
    df=df.drop(['Cols_x','Cols_y'], axis=1)
    df['value'],df['year']=df['value'].astype(float),df['year'].astype(int),
    df=df.set_index(['code','year','nace_r2'])
    return df
    
def output_getter():
    df=eurostat.get_data_df('NAMA_10_A64', flags=True)
    df=df[(df['unit']=='CP_MEUR')&(df['na_item']=='B1G')]
    df=df.drop(['freq','na_item'], axis=1)
    df=df.rename(columns={'geo\TIME_PERIOD':'code'})
    df_temp = df.melt(id_vars=['nace_r2','code','unit'], var_name='Cols')
    df_temp['year']=df_temp['Cols'].apply(lambda x : x[0:4])
    df_temp['Cols']=df_temp['Cols'].apply(lambda x : x[5:])
    df=df_temp[(df_temp['Cols']=='value')].merge(df_temp[(df_temp['Cols']=='flag')],on=['nace_r2','code','unit','year'],how='outer').rename(columns={'value_x':'value','value_y':'flag'})
    df=df.drop(['Cols_x','Cols_y'], axis=1)
    df=df[(df['year'].astype(int)>=2002)&(df['year'].astype(int)<=2018)]
    df['value'],df['year']=df['value'].astype(float),df['year'].astype(int),
    df=df.set_index(['code','nace_r2','year'])
    return df   

def lsupply_getter():
    df=eurostat.get_data_df("LFSA_EISN2", True)
    df=df[(df['sex']=='T')&(df['age']=='Y20-64')]
    df=df.drop(['freq','age','sex'],axis=1)
    df=df.rename(columns={'geo\TIME_PERIOD':'code'})
    df_temp = df.melt(id_vars=['nace_r2','isco08','unit','code'], var_name='Cols')
    df_temp['year']=df_temp['Cols'].apply(lambda x : x[0:4])
    df_temp['Cols']=df_temp['Cols'].apply(lambda x : x[5:])
    df=df_temp[(df_temp['Cols']=='value')].merge(df_temp[(df_temp['Cols']=='flag')],on=['nace_r2','isco08','unit','code','year'],how='outer').rename(columns={'value_x':'value','value_y':'flag'})
    df=df.drop(['Cols_x','Cols_y'], axis=1)
    df['value'],df['year']=df['value'].astype(float),df['year'].astype(int),
    df=df.set_index(['code','nace_r2','year'])
    return df
    
    