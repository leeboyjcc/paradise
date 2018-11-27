# -*- coding: utf-8 -*-
import pandas as pd
def co2():
    data = pd.read_excel('ClimateChange.xlsx', sheetname='Data', parse_cols='A,C,G:AB')
    co2data = data[data['Series code']=='EN.ATM.CO2E.KT']
    co2data.set_index('Country code', inplace=True)
    co2data = co2data.drop(labels=['Series code'], axis=1)
    co2data.replace({'..': pd.np.NaN}, inplace=True)
    co2data = co2data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    co2data = co2data.dropna(how='all')
    co2data['Sum emissions'] = co2data.sum(axis=1)
    co2data = co2data['Sum emissions']

    country = pd.read_excel('ClimateChange.xlsx', sheetname='Country', parse_cols='A, B, E')
    country.set_index('Country code', inplace=True) 

    df = pd.concat([co2data, country], axis=1)

    df_sum = df.groupby('Income group').sum()

    df_max = df.sort_values(by='Sum emissions', ascending=False).groupby('Income group').head(1).set_index('Income group')
    df_max.columns = ['Highest emissions', 'Highest emission country']
    df_max = df_max.reindex(columns=['Highest emission country', 'Highest emissions'])

    df_min = df.sort_values(by='Sum emissions').groupby('Income group').head(1)
    df_min.set_index('Income group', inplace=True)
    df_min.columns = ['Lowest emissions', 'Lowest emission country']
    df_min =  df_min.reindex(columns=['Lowest emission country', 'Lowest emissions'])

    return pd.concat([df_sum, df_max, df_min], axis=1)
    

if __name__=='__main__':
    print(co2())
