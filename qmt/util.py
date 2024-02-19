from functools import cache
import akshare as ak
import pandas as pd

df = ak.bond_zh_cov()


def getNameFromCode(stock_code):
    if '.' not in stock_code:
        stock_code = to_long_name(stock_code)

    bond_code = stock_code.split(".")[0]
    line = df.loc[df["债券代码"] == bond_code, "债券简称"]
    if line.empty:
        return stock_code
    else:
        return line.values[0]


def sizeBigThan(stock_code):
    stock_individual_info_em_df = ak.stock_individual_info_em(symbol=stock_code)

    return stock_individual_info_em_df[stock_individual_info_em_df['item'] == '总市值']['value'] > 50 * 10 ** 8


def s(num):
    if num == 0:
        return "0"
    if num.is_integer():
        return str(int(num))
    else:
        return "{:.2f}".format(num)

# 同时带上了总市值信息


def get_all_data():
    import akshare as ak

    all_cube = get_data()
    all_cube.reset_index(level=0, inplace=True)
    all_cube.rename(columns={'index': '可转债代码'}, inplace=True)

    all_stock = ak.stock_zh_a_spot_em()
    # 使用 merge 方法关联表A和表B，基于正股代码列
    merged_df = pd.merge(all_cube, all_stock, left_on='正股代码', right_on='代码', how='left')

    if len(merged_df) < 100:
        raise Exception

    merged_df["正股总市值"] = merged_df["总市值"]

    return merged_df


def to_long_name(code):
    post_fix = 'SZ' if code.startswith('12') else 'SH'
    code = '{}.{}'.format(code, post_fix)
    return code


def get_data():
    from qmt.jisilu.jisilu_data import Jisilu
    obj = Jisilu()
    data = obj.run()
    return data


@cache
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
