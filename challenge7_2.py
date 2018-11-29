# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def co2_gdp_plot():
    data = pd.read_excel('ClimateChange.xlsx', sheetname='Data', parse_cols='A,C,G:AB')

    co2data = data[data['Series code']=='EN.ATM.CO2E.KT'].set_index('Country code')
    co2data.drop('Series code', axis=1, inplace=True)
    co2data.replace({'..':pd.np.NaN}, inplace=True)
    co2data = co2data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)

    # 对数据中全行或全列为NaN的数据进行填充0
    co2data = co2data.fillna(0)
    co2data['CO2-SUM'] = co2data.sum(axis=1)
    co2data = co2data['CO2-SUM']

    co2data = (co2data - co2data.min()) / (co2data.max() - co2data.min())

    gdpdata = data[data['Series code']=='NY.GDP.MKTP.CD'].set_index('Country code')
    gdpdata.drop('Series code', axis=1, inplace=True)
    gdpdata.replace({'..':pd.np.NaN}, inplace=True)
    gdpdata = gdpdata.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)

    gdpdata.fillna(0, inplace=True)
    gdpdata['GDP-SUM'] = gdpdata.sum(axis=1)
    gdpdata = gdpdata['GDP-SUM']

    gdpdata = (gdpdata - gdpdata.min()) / (gdpdata.max() - gdpdata.min())

    gdp_co2 = pd.concat([co2data, gdpdata], axis=1)

    china = [np.round(i, decimals=3).tolist() for i in list(gdp_co2.loc['CHN'].values)]

    five = ['CHN', 'USA', 'GBR', 'FRA','RUS']
    # 在数据中的标签
    five_labels = []
    # 在数据中的刻度
    five_position = []
    for i in range(len(gdp_co2)):
        if gdp_co2.index[i] in five:
            five_labels.append(gdp_co2.index[i])
            five_position.append(i)

    fig = plt.subplot()
    gdp_co2.plot(kind='line', title='GDP-CO2', ax=fig)
    plt.xlabel('Countries')
    plt.ylabel('Values')
    plt.xticks(five_position, five_labels, rotation='vertical')
    plt.show()

    return fig, china


if __name__=='__main__':
    fig, china = co2_gdp_plot()
    print(china)
