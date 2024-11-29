# -*-coding=utf-8-*-
__author__ = 'Rocky'
'''
http://30daydo.com
Contact: weigesysu@qq.com
'''

import re
from loguru import logger
import parsel
import datetime
import time
import pandas as pd
import execjs
import os
import requests

user = '张家诚'  # 填入你的集思录账号
password = 'Garry194278'  # 填入你的集思录密码


class BaseService(object):

    def __init__(self, logfile='default.log'):
        self.logger = logger
        self.logger.add(logfile)
        self.init_const_data()
        self.params = None
        self.cookies = None

    def init_const_data(self):
        '''
        常见的数据初始化
        '''
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')

    def get_url_filename(self, url):
        return url.split('/')[-1]

    def get(self, url, _json=False, binary=False, retry=5):

        start = 0
        while start < retry:

            try:
                r = requests.get(
                    url=url,
                    params=self.params,
                    headers=self.headers,
                    cookies=self.cookies)

            except Exception as e:
                self.logger.error('base class error '.format(e))
                start += 1
                continue

            else:
                if _json:
                    result = r.json()
                elif binary:
                    result = r.content
                else:
                    r.encoding = 'utf8'
                    result = r.text
                return result

        return None

    def post(self, url, post_data, _json=False, binary=False, retry=5):

        start = 0
        while start < retry:

            try:
                r = requests.post(
                    url=url,
                    headers=self.headers,
                    data=post_data
                )

            except Exception as e:
                print(e)
                start += 1
                continue

            else:
                if _json:
                    result = r.json()
                elif binary:
                    result = r.content
                else:
                    result = r.text
                return result

        return None

    @property
    def headers(self):
        raise NotImplemented

    def parse(self, content):
        '''
        页面解析
        '''
        response = parsel.Selector(text=content)
        return response

    def time_str(self, x):
        return x.strftime('%Y-%m-%d')

    def notify(self, title):
        # send_message_via_wechat(title)
        logger.info('可以执行发消息到自己的微信')
        logger.info(title)

    def convert_timestamp(self, t):
        return datetime.datetime.fromtimestamp(int(t / 1000)).strftime('%Y-%m-%d')


filename = 'encode_jsl.js'
path = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(path, filename)

headers = {
    'Host': 'www.jisilu.cn', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
    'Cache-Control': 'no-cache', 'Accept': 'application/json,text/javascript,*/*;q=0.01',
    'Origin': 'https://www.jisilu.cn', 'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Referer': 'https://www.jisilu.cn/login/',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8'
}


def decoder(text):
    with open(full_path, 'r', encoding='utf8') as f:
        source = f.read()

    ctx = execjs.compile(source)
    key = '397151C04723421F'
    return ctx.call('jslencode', text, key)


def login(user, password):
    session = requests.Session()
    url = 'https://www.jisilu.cn/account/ajax/login_process/'
    username = decoder(user)
    jsl_password = decoder(password)
    data = {
        'return_url': 'https://www.jisilu.cn/',
        'user_name': username,
        'password': jsl_password,
        'net_auto_login': '1',
        '_post_type': 'ajax',
    }

    js = session.post(
        url=url,
        headers=headers,
        data=data,
    )

    ret = js.json()
    if ret.get('errno') == 1:
        print('登录成功')
        return session
    else:
        print('登录失败')
        raise ValueError('登录失败')


# 爬取集思录 可转债的数据
class Jisilu(BaseService):
    def __init__(self):
        super(Jisilu, self).__init__(logfile='jisilu.log')

        self.date = datetime.datetime.now().strftime('%Y-%m-%d')
        # self.date = '2020-02-07' # 用于调整时间
        self.timestamp = int(time.time() * 1000)
        self.url = 'https://www.jisilu.cn/data/cbnew/cb_list_new/?___jsl=LST___t={}'.format(self.timestamp)
        self.pre_release_url = 'https://www.jisilu.cn/data/cbnew/pre_list/?___jsl=LST___t={}'.format(self.timestamp)

        self.get_session()

    @property
    def headers(self):
        _header = {
            'Host': 'www.jisilu.cn', 'Connection': 'keep-alive', 'Pragma': 'no-cache',
            'Cache-Control': 'no-cache', 'Accept': 'application/json,text/javascript,*/*;q=0.01',
            'Origin': 'https://www.jisilu.cn', 'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Referer': 'https://www.jisilu.cn/login/',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8'
        }
        return _header

    def get_session(self):
        self.session = login(user, password)

    def download(self, url, data, retry=5):

        for i in range(retry):
            try:
                r = self.session.post(url, headers=self.headers, data=data)
                if not r.text or r.status_code != 200:
                    continue
                else:
                    return r
            except Exception as e:
                self.logger.info(e)
                self.notify(title=f'下载失败 {self.__class__}')
                continue

        return None

    def run(self, adjust_no_use=True):

        post_data = {
            "fprice": None,
            "tprice": None,
            "curr_iss_amt": None,
            "volume": None,
            "svolume": None,
            "premium_rt": None,
            "ytm_rt": None,
            "rating_cd": None,
            "is_search": "N",
            "btype": "C",
            "listed": "Y",
            "qflag": "N",
            "sw_cd": None,
            "bond_ids": None,
            "rp": 50,
        }

        js = self.download(self.url, data=post_data)
        if not js:
            return None

        ret = js.json()
        bond_list = ret.get('rows', {})
        df = self.data_parse(bond_list, adjust_no_use)

        # 保存换手率数据，使用指定的日期
        self.save_turnover_rates(df, self.date)
        return df

    def save_turnover_rates(self, df, date_str):
        """保存换手率数据
        
        Args:
            df: 数据框
            date_str: 日期字符串
        """
        try:
            os.makedirs("data", exist_ok=True)
            
            turnover_data = df[['换手率']].copy()
            turnover_data['date'] = date_str
            
            if os.path.exists(self.turnover_file):
                turnover_data.to_csv(self.turnover_file, mode='a', header=False)
            else:
                turnover_data.to_csv(self.turnover_file)
                
            logger.info(f"成功保存{len(turnover_data)}条换手率数据，日期：{date_str}")
            
        except Exception as e:
            error_msg = f"保存换手率数据失败: {e}"
            logger.error(error_msg)

    def get_session(self):
        self.session = login(user, password)

    def download(self, url, data, retry=5):

        for i in range(retry):
            try:
                r = self.session.post(url, headers=self.headers, data=data)
                if not r.text or r.status_code != 200:
                    continue
                else:
                    return r
            except Exception as e:
                self.logger.info(e)
                self.notify(title=f'下载失败 {self.__class__}')
                continue

        return None

    def identify_margin(self, x):
        if len(x) == 0:
            return '否'
        else:
            return '是'

    def data_parse(self, bond_list, adjust_no_use):

        cell_list = []
        for item in bond_list:
            cell_list.append(pd.Series(item.get('cell')))
        df = pd.DataFrame(cell_list)

        if adjust_no_use:
            # 类型转换 部分含有%
            df['price'] = df['price'].astype('float64')
            df['convert_price'] = df['convert_price'].astype('float64')
            df['premium_rt'] = df['premium_rt'].astype('float64')
            df['force_redeem_price'] = df['force_redeem_price'].astype('float64')
            df['margin_flg'] = df['icons'].map(self.identify_margin)
            df['icons'] = df['icons'].map(str)
            rename_columns = {'bond_id': '可转债代码', 'bond_nm': '可转债名称',
                              'price': '可转债价格', 'stock_nm': '正股名称',
                              'stock_id': '正股代码',
                              'sprice': '正股现价',
                              'sincrease_rt': '正股涨跌幅',
                              'convert_price': '最新转股价', 'premium_rt': '溢价率',
                              'increase_rt': '可转债涨幅',
                              'convert_value': '转股价值',
                              'dblow': '双低',
                              'put_convert_price': '回售触发价', 'convert_dt': '转股起始日',
                              'maturity_dt': '到期时间',
                              # 'short_maturity_dt': '到期时间',
                              'volume': '成交额(万元)',
                              'force_redeem_price': '强赎价格', 'year_left': '剩余时间',
                              # 'next_put_dt': '回售起始日',
                              'rating_cd': '评级',
                              # 'issue_dt': '发行时间',
                              # 'redeem_tc': '强制赎回条款',
                              # 'adjust_tc': '下修条件',
                              # 'adjust_condition': '下修条件',
                              'turnover_rt': '换手率',
                              'convert_price_tips': '下修提示',
                              # 'put_tc': '回售',
                              'adj_cnt': '提出下调次数',
                              'svolume': '正股成交量',
                              #   'ration':'已转股比例'
                              'convert_amt_ratio': '转债剩余占总市值比',
                              'curr_iss_amt': '剩余规模', 'orig_iss_amt': '发行规模',
                              # 'ration_rt': '股东配售率',
                              'option_tip': '期权价值',
                              # 'bond_nm_tip': '强赎提示',
                              'redeem_dt': '强赎日期',
                              'list_dt': '上市日期',
                              'ytm_rt': '到期收益率',
                              # 'redeem_icon': '强赎标志',
                              'icons': '标记',
                              'margin_flg': '是否两融标的',

                              'adj_scnt': '下修成功次数',
                              'convert_cd_tip': '转股日期提示',
                              'ref_yield_info': '参考YTM',
                              # 'year_left':'剩余年限',
                              # 'guarantor': '担保',
                              }

            df = df.rename(columns=rename_columns)
            # df = df[list(rename_columns.values())]
            df['更新日期'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        df = df.set_index('可转债代码', drop=True)
        return df

    def to_excel(self, df):
        try:
            df.to_excel(f'jisilu_{self.date}.xlsx')
        except Exception as e:
            print(e)

    def convert_float(self, x):
        if not x:
            return None

        if '%' in x:
            ration = 100
        else:
            ration = 1

        x = re.sub('%', '', x)
        try:
            ret = float(x) * ration
        except Exception as e:
            self.logger.error('转换失败{}'.format(e))
            ret = None

        return ret


def main():
    """获取当天数据"""
    obj = Jisilu()
    obj.run()


if __name__ == '__main__':
    main()

