import pandas as pd

# 数据位置
filePath = 'data/2017-2022-08-25日线数据.csv'
# 数据
df = pd.read_csv(filePath, index_col=0)
# 日期数据范围
dateRange = []
# 每日数据
day2df = {}


# 计算部分中间数据
df['value'] = 100/df['convPrice']*df['closePriceEqu']
df['ratio'] = df['closePriceBond']/df['value']-1
df['doubleLow'] = df['closePriceBond'] + \
    df['ratio']*100
df['closePriceBond'] = df['closePriceBond'].apply(
    lambda x: round(x, 2))

# 计算数据范围
dateRange = list(set(df['tradeDate']))
dateRange.sort()

# 计算日数据
for date_str in dateRange:
    day2df[date_str] = df[df['tradeDate'] == date_str]


