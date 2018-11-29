# -*- coding: utf-8 -*-
import pandas as pd
def co2():
    # 读取Excel文件中的Data sheet
    data = pd.read_excel('ClimateChange.xlsx', sheetname='Data', parse_cols='A,C,G:AB')
    co2data = data[data['Series code']=='EN.ATM.CO2E.KT']
    
    # 把Country code列作为索引，该列就从数据列中消失成为了索引
    co2data.set_index('Country code', inplace=True)
    # 删除Series code列， axis=1表示按列删除
    co2data = co2data.drop(labels=['Series code'], axis=1)
    # 将数据中的无效值..替换为NaN
    co2data.replace({'..': pd.np.NaN}, inplace=True)
    # axis=1 表示按行进行填充值，ffill表示按照前面一个值进行填充, bfill表示按照后面一个值进行填充
    co2data = co2data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    # 丢弃数据中全部为NaN的行或列
    co2data = co2data.dropna(how='all')
    # axis=1表示按行对数据进行求和
    co2data['Sum emissions'] = co2data.sum(axis=1)
    co2data = co2data['Sum emissions']

    country = pd.read_excel('ClimateChange.xlsx', sheetname='Country', parse_cols='A, B, E')
    # inplace=True表示就地处理也即对原对象进行修改，不会返回新的对象
    country.set_index('Country code', inplace=True) 

    # 对两个DataFrame进行按列合并，前提是两个DataFrame的索引要一直，这很重要
    df = pd.concat([co2data, country], axis=1)

    # 对数据按Income group分组后求和
    df_sum = df.groupby('Income group').sum()

    # 对数据按Sum emissions列进行降序排序后，在按Income group列进行分组，得到的每组数据里都是已排序，然后设置索引
    df_max = df.sort_values(by='Sum emissions', ascending=False).groupby('Income group').head(1).set_index('Income group')
    # 对数据的列名进行重新更新
    df_max.columns = ['Highest emissions', 'Highest emission country']
    # 对数据的列名顺序进行调整
    df_max = df_max.reindex(columns=['Highest emission country', 'Highest emissions'])

    df_min = df.sort_values(by='Sum emissions').groupby('Income group').head(1)
    df_min.set_index('Income group', inplace=True)
    df_min.columns = ['Lowest emissions', 'Lowest emission country']
    df_min =  df_min.reindex(columns=['Lowest emission country', 'Lowest emissions'])
    # 按列合并两个DataFrame
    return pd.concat([df_sum, df_max, df_min], axis=1)
    

if __name__=='__main__':
    print(co2())
