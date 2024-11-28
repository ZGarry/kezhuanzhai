from functools import cache
import akshare as ak
import pandas as pd
from diskcache import Cache

cache_dir = './.cache'
cache = Cache(cache_dir)

@cache.memoize()
def get_bond_info(date_str):
    print(1)
    return ak.bond_zh_cov()

@cache.memoize()
def get_stock_info(date_str):
    print(2)
    return ak.stock_info_a_code_name()

@cache.memoize()
def get_etf_info(date_str):
    print(3)
    return ak.fund_etf_category_sina(symbol="ETF基金")

# 获取当日日期
import datetime
date_str = datetime.datetime.now().strftime('%Y%m%d')

# 这些其实每天执行一次就可以了
df = get_bond_info(date_str)
# 获取所有A股股票的代码和名称（不包含债券）
stock_info = get_stock_info(date_str)
# 获取所有ETF的信息
etf_info = get_etf_info(date_str)

# qmtLongCode shortCode 中文名
@cache.memoize()
def getNameFromCode(stock_code):
    if '.' not in stock_code:
        stock_code = to_long_name(stock_code)

    short_code = stock_code.split(".")[0]
    line = df.loc[df["债券代码"] == short_code, "债券简称"]
    if line.empty:
        line = stock_info.loc[stock_info["code"] == short_code, "name"]
        if line.empty:
            # 在ETF中查找
            line = etf_info[etf_info['代码'].str.contains(short_code, na=False)]
            if line.empty:
                return stock_code
            else:
                return line.iloc[0]['名称']
        else:
            return line.values[0]
    else:
        return line.values[0]


def show(num):
    if num == 0:
        return "0"
    if num.is_integer():
        return str(int(num))
    else:
        return "{:.2f}".format(num)


# 转换为qmt使用的长名
def to_long_name(code):
    post_fix = 'SZ' if code.startswith('12') else 'SH'
    code = '{}.{}'.format(code, post_fix)
    return code

# 从集思录获取数据
def get_data():
    from jisilu.jisilu_data import Jisilu
    obj = Jisilu()
    data = obj.run()
    return data

@cache.memoize()
def get_trade_date_hist_sina(year):
    tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
    return tool_trade_date_hist_sina_df


def today_is_trade_day():
    # 获取今天年
    from datetime import datetime
    current_datetime = datetime.now()
    current_year = current_datetime.year

    # 获取全量数据
    df = get_trade_date_hist_sina(current_year)

    # 获取今天年月日
    today_str = current_datetime.strftime("%Y-%m-%d")
    today = datetime.strptime(today_str, "%Y-%m-%d").date()
    # 判断今天是否是交易日
    if today in df['trade_date'].values:
        return True
    else:
        return False
