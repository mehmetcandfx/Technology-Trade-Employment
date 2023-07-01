# preptools.py

import pandas as pd
import os
import eurostat

def trade_getter():
    df=eurostat.get_data_df('EXT_STEC01', flags=True)
    df=df[(df['partner']=='WORLD')&(df['sizeclas']=='TOTAL')]
    df=df.drop(['freq','sizeclas','partner'], axis=1)
    df=df.rename(columns={'geo\TIME_PERIOD':'code'})
    df_temp = df.melt(id_vars=['nace_r2','stk_flow','unit','code'], var_name='Cols')
    df_temp['year'],df_temp['Colss']=df_temp['Cols'].apply(lambda x : x[0:4]),df_temp['Cols'].apply(lambda x : x[5:])
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
    df=df.set_index(['code','year','nace_r2'])
    return df   