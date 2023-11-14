import time
import datetime
# import traceback
import sys
from xtquant import xtdata
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant

import pandas as pd

import datetime


def get_tick(code, start_time, end_time, period='tick'):
    from xtquant import xtdata

    xtdata.download_history_data(code, period=period, start_time=start_time, end_time=end_time)
    data = xtdata.get_local_data(field_list=[], stock_list=[code], period=period, count=10)
    result_list = data[code]
    df = pd.DataFrame(result_list)

    df['time_str'] = df['time'].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000.0))
    return df


def process_timestamp(df, filename):
    df = df.set_index('time_str')
    result = df.resample('3S').first().ffill()
    # result = result[(result.index >= '2022-07-20 09:30') & (result.index <= '2022-07-20 15:00')]
    result = result.reset_index()
    result.to_csv(filename + '.csv')


def dump_single_code_tick():
    # 导出单个转债的tick数据
    # 11--沪市可转债 12--深市可转债
    code='128022'
    start_date = '20210113'
    end_date = '20210130'

    post_fix = 'SZ' if code.startswith('12') else 'SH'
    code = '{}.{}'.format(code,post_fix)
    filename = '{}'.format(code)
    df = get_tick(code, start_date, end_date)

dump_single_code_tick()
