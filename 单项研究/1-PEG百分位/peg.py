# 真正计算得到PEG
import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Simhei']


def genROEdf(stock="000651", start_year="2000", need_change=True):
    # 可以看一下这个ROEdf的数据输出
    stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(symbol=stock, start_year=start_year)
    ROEdf = stock_financial_analysis_indicator_df[['日期', '净资产收益率(%)']].sort_values(by='日期', ascending=True)

    ROEdf['日期'] = pd.to_datetime(ROEdf['日期'])

    # 对日季度的ROE做处理
    def apply_condition(row):
        if row['日期'].month == 3 and row['日期'].day == 31:
            return row['净资产收益率(%)'] * 4
        elif row['日期'].month == 6 and row['日期'].day == 30:
            return row['净资产收益率(%)'] * 2
        elif row['日期'].month == 9 and row['日期'].day == 30:
            return row['净资产收益率(%)'] * 1.3333
        else:
            return row['净资产收益率(%)']

    # 使用正则表达式匹配只有数字的模式
    ROEdf = ROEdf[ROEdf['净资产收益率(%)'].str.match(r'^\d+\.?\d*$')]
    ROEdf['净资产收益率(%)'] = ROEdf['净资产收益率(%)'].astype(float)
    # 应用条件操作，ROE进行标准化计算
    if need_change:
        ROEdf['净资产收益率(%)'] = ROEdf.apply(apply_condition, axis=1)
        ROEdf.set_index('日期', inplace=True)
        # 重新采样并填充缺失值
        ROEdf = ROEdf.resample('D').ffill()
        # 重新设置索引，将日期列重新加入数据框
        ROEdf.reset_index(inplace=True)
    return ROEdf


def genPEdf(stock="000651"):
    stock_a_indicator_lg_df = ak.stock_a_indicator_lg(symbol=stock)
    PEdf = stock_a_indicator_lg_df[['trade_date', 'pe']]

    PEdf['trade_date'] = pd.to_datetime(PEdf['trade_date'])
    return PEdf


def genMergedDf(stock="000651", start_year="2000"):
    ROEdf = genROEdf(stock, start_year)
    PEdf = genPEdf(stock)
    merged_df = pd.merge(ROEdf, PEdf, left_on='日期', right_on='trade_date', how='inner')
    # 删除多余的日期列
    merged_df.drop(columns=['trade_date'], inplace=True)

    merged_df['PEG'] = merged_df['pe'] / merged_df['净资产收益率(%)']

    print(f"该股票的PEG百分位：{PEGrate(merged_df)}，，PE百分位：{PErate(PEdf)}，ROE百分位：{ROErate(ROEdf)}")

    return ROEdf, PEdf, merged_df


def showPEG(merged_df):
    # 绘制线条
    plt.plot(merged_df['日期'], merged_df['PEG'], label='PE / 净资产收益率(%)')

    # 添加标签和标题
    plt.xlabel('日期')
    plt.ylabel('PE / 净资产收益率(%)')
    plt.title('PE 值除以净资产收益率的折线图')
    plt.legend()
    # 显示图形
    plt.show()


def showPE(PEdf):
    # 绘制线条
    plt.plot(PEdf['trade_date'], PEdf['pe'], label='PE / 净资产收益率(%)')

    # 添加标题和标签
    plt.title('PE Ratio over Time')
    plt.xlabel('Trade Date')
    plt.ylabel('PE')

    # 旋转 x 轴刻度标签，以避免重叠
    plt.xticks(rotation=45)

    # 显示图表
    plt.show()


def PEGrate(PEGdf):
    last_value = PEGdf['PEG'].iloc[-1]
    # 计算 PEG 列的百分位
    percentile = (PEGdf['PEG'] < last_value).mean() * 100
    return percentile


def PErate(PEdf):
    last_value = PEdf['pe'].iloc[-1]
    # 计算 PEG 列的百分位
    percentile = (PEdf['pe'] < last_value).mean() * 100
    return percentile


def ROErate(ROEdf):
    last_value = ROEdf['净资产收益率(%)'].iloc[-1]
    # 计算 PEG 列的百分位
    percentile = (ROEdf['净资产收益率(%)'] < last_value).mean() * 100
    return percentile


ROEdf, PEdf, PEGdf = genMergedDf("603688")
showPE(PEdf)
showPEG(PEGdf)
