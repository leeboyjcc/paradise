# -*- coding: utf-8 -*-
import pandas as pd
from sklearn import linear_model

def Temperature():

    temperature = pd.read_csv('GlobalSurfaceTemperature.csv')
    gas = pd.read_csv('GreenhouseGas.csv')
    co2 = pd.read_csv('CO2ppm.csv') 

    temperature = temperature.set_index('Year')
    gas = gas.set_index('Year') 
    co2 = co2.set_index('Year') 

    combine = pd.concat([gas, co2, temperature], axis=1)
    feature = combine.iloc[:, 0:4]
    # 按列进行填充
    feature = feature.fillna(method='ffill').fillna(method='bfill')

    # 特征训练数据
    feature_train = feature.loc[1960:2010]
    # 特征预测数据
    feature_test = feature.loc[2011:2017]

    # 目标训练数据
    target_median_train = combine.loc[1960:2010, 'Median']
    #median = linear_model.LinearRegression()
    median = linear_model.BayesianRidge()
    median.fit(feature_train, target_median_train)
    # 目标预测结果
    MedianPredict = median.predict(feature_test)
    MedianPredict = [round(i, 3) for i in MedianPredict.tolist()]


    target_upper_train = combine.loc[1960:2010, 'Upper']
    #upper = linear_model.LinearRegression()
    upper = linear_model.BayesianRidge()
    upper.fit(feature_train, target_upper_train)
    UpperPredict = upper.predict(feature_test)
    UpperPredict = [round(i, 3) for i in UpperPredict.tolist()]


    target_lower_train = combine.loc[1960:2010, 'Lower']
    #lower = linear_model.LinearRegression()
    lower = linear_model.BayesianRidge()
    lower.fit(feature_train, target_lower_train)
    LowerPredict = lower.predict(feature_test)
    LowerPredict = [round(i, 3) for i in LowerPredict.tolist()]

    return UpperPredict, MedianPredict, LowerPredict


if __name__=='__main__':
    u, m, l = Temperature()
    print(u)
    print(m)
    print(l)
