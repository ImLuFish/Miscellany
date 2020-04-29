import pandas as pd
import numpy as np
import re


df1 = pd.read_excel("固定资产.xlsx", sheet_name=3)
df2 = df1.iloc[1:]
df3 = df2.drop(columns=['Unnamed: 16', 'Unnamed: 22', 'Unnamed: 23', 'Unnamed: 24'])
df3.columns = ['项目', '编号', 'NC入账时间', '完工日期', '资产名称/摘要', '原值', '残值率', '使用年限(年)',
       '使用年限(月)', '累计折旧', '净值', '净残值', '是否提足折旧', '是否在本年提足折旧', '期初累计折旧',
       '每月应折旧额', '本年折旧月份', '折旧月份(按完工日期）', '本年折旧', '差异']
df3["NC入账时间"] = pd.to_datetime(df3["NC入账时间"])
df3["完工日期"] = pd.to_datetime(df3["完工日期"])
df3 = df3[['项目', 'NC入账时间', '资产名称/摘要', '累计折旧', '完工日期',  '编号', '原值', '残值率', '使用年限(年)',
       '使用年限(月)', '净值', '净残值', '是否提足折旧', '是否在本年提足折旧', '期初累计折旧',
       '每月应折旧额', '本年折旧月份', '折旧月份(按完工日期）', '本年折旧', '差异']]
pat = "[A-Za-z0-9\u4E00-\u9FFF]+"
df3["特征码"] = df3["资产名称/摘要"].apply(lambda x: "".join(re.compile(pat).findall(x)))
df2018 = df3[["项目", "NC入账时间", "原值", "编号", "累计折旧", '资产名称/摘要']]
df2018 = df2018.rename(columns={"累计折旧": "2018累计折旧", '资产名称/摘要': '2018资产名称/摘要'})
df2018 = df2018.sort_values(["项目", "NC入账时间", "原值", "编号", '2018资产名称/摘要']).reset_index(drop=True)


def calc(x):
    df = x.reset_index(drop=True)
    return df[["2018累计折旧", "项目", "2018资产名称/摘要"]]


df2018a = df2018.groupby(["NC入账时间", "原值"]).apply(calc).reset_index()
df2018a = df2018a.rename(columns={"level_2": "索引号"})
# 组内予以升序编号; 但是运行偏慢;
# df2018.groupby(["NC入账时间", "原值"]).cumcount() is OK

df4 = pd.read_excel("固定资产.xlsx", sheet_name=4, header=1)
df4 = df4.drop(columns=['Excel名'])
df4 = df4.drop(columns=['Unnamed: 18', 'Unnamed: 0'])
df4 = df4.rename(columns={"本年折旧.1": "本年折旧"})


def calc(x):
    try:
        return pd.to_datetime(x)
    except:
        return np.nan


df4["NC入账时间"] = df4["NC入账时间"].apply(calc)
df4["完工日期"] = df4["完工日期"].apply(calc)
df4 = df4.iloc[:-1]

for i in range(len(df4)):
    if pd.isna(df4.loc[i, "资产名称/摘要"]):
        df4.loc[i, "资产名称/摘要"] = df4.loc[i, "编号"]

df4["特征码"] = df4["资产名称/摘要"].apply(lambda x: "".join(re.compile(pat).findall(x)))
df4 = df4[['项目', 'NC入账时间', '原值', '累计折旧', '编号', '完工日期', '资产名称/摘要',  '残值率', '使用年限(年)',
       '使用年限(月)',  '净值', '净残值', '是否提足折旧', '是否在本年提足折旧', '期初累计折旧',
       '每月应折旧额', '本年折旧月份', '折旧月份(按完工日期）', '本年折旧', '差异', ]]

df2019 = df4.copy()
df2019 = df2019.sort_values(["项目", "NC入账时间", "原值", "编号", "资产名称/摘要"]).reset_index(drop=True)


def calc(x):
    df = x.reset_index(drop=True)
    return df[["项目", '累计折旧', '编号', '完工日期', '资产名称/摘要', '残值率', '使用年限(年)',
       '使用年限(月)', '净值', '净残值', '是否提足折旧', '是否在本年提足折旧', '期初累计折旧',
       '每月应折旧额', '本年折旧月份', '折旧月份(按完工日期）', '本年折旧', '差异']]


df2019a = df2019.groupby(["NC入账时间", "原值"]).apply(calc).reset_index()
df2019a = df2019a.rename(columns={"level_2": "索引号"})
df2018a["原值"] = df2018a["原值"].apply(lambda x: round(x, 2))
df2019a["原值"] = df2019a["原值"].apply(lambda x: round(x, 2))

res = pd.merge(df2019a, df2018a, "left", on=["NC入账时间", "原值", "索引号"], indicator=True)
res = res.rename(columns={"_merge": "合并状态"})
res[["累计折旧", "2018累计折旧"]] = res[["累计折旧", "2018累计折旧"]].applymap(lambda x: round(x, 2))
res = res.rename(columns={"项目_x":"2019项目名称", "项目_y": "2018项目名称"})
res = res.sort_values(["2019项目名称", "NC入账时间", "原值", "索引号"])
res = res[['2019项目名称', 'NC入账时间', '原值', '索引号', '累计折旧', '编号', '完工日期', '资产名称/摘要',
       '残值率', '使用年限(年)', '使用年限(月)', '净值', '净残值', '是否提足折旧', '是否在本年提足折旧',
       '期初累计折旧', '每月应折旧额', '本年折旧月份', '折旧月份(按完工日期）', '本年折旧', '差异', '2018累计折旧', '2018项目名称',
       '2018资产名称/摘要', '合并状态']]
res = res.reset_index(drop=True)
res.to_csv("合并结果.csv", index=False, encoding="gbk")