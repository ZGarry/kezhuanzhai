from loguru import logger
import datetime
import time
import pandas as pd
import execjs
import os
import requests

class Jisilu:
    """集思录数据获取类"""
    
    def __init__(self, date_str=None):
        """初始化
        
        Args:
            date_str: 可选的日期字符串，格式为'%Y-%m-%d'
        """
        # 初始化日期和时间戳
        if date_str:
            self.date = date_str
            dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            self.timestamp = int(dt.timestamp() * 1000)
        else:
            self.date = datetime.datetime.now().strftime('%Y-%m-%d')
            self.timestamp = int(time.time() * 1000)
            
        # 设置URL和文件路径
        self.url = f'https://www.jisilu.cn/data/cbnew/cb_list_new/?___jsl=LST___t={self.timestamp}'
        self.turnover_file = "data/turnover_rates.csv"
        
        # 登录集思录
        self.session = self._login()
        
    @property
    def headers(self):
        """请求头"""
        return {
            'Host': 'www.jisilu.cn',
            'Connection': 'keep-alive',
            'Accept': 'application/json,text/javascript,*/*;q=0.01',
            'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'Referer': 'https://www.jisilu.cn/login/',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8'
        }
        
    def _login(self):
        """登录集思录"""
        # 获取加密密钥
        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, 'encode_jsl.js'), 'r', encoding='utf8') as f:
            js = execjs.compile(f.read())
            
        # 加密用户名和密码
        key = '397151C04723421F'
        username = js.call('jslencode', '张家诚', key)
        password = js.call('jslencode', 'Garry194278', key)
        
        # 登录
        session = requests.Session()
        login_data = {
            'return_url': 'https://www.jisilu.cn/',
            'user_name': username,
            'password': password,
            'net_auto_login': '1',
            '_post_type': 'ajax',
        }
        
        response = session.post(
            'https://www.jisilu.cn/account/ajax/login_process/',
            headers=self.headers,
            data=login_data
        )
        
        if response.json().get('errno') != 1:
            raise ValueError('登录失败')
            
        return session
        
    def get_data(self):
        """获取可转债数据"""
        post_data = {
            "is_search": "N",
            "listed": "Y",
            "rp": 50,
        }
        
        for _ in range(3):  # 重试3次
            try:
                response = self.session.post(self.url, headers=self.headers, data=post_data)
                if response.status_code == 200 and response.text:
                    return response.json().get('rows', [])
            except Exception as e:
                logger.error(f"获取数据失败: {e}")
                time.sleep(1)
                
        return None
        
    def process_data(self, data):
        """处理可转债数据"""
        if not data:
            return None
            
        # 转换为DataFrame
        df = pd.DataFrame([item['cell'] for item in data])
        
        # 重命名列
        rename_map = {
            'bond_id': '可转债代码',
            'bond_nm': '可转债名称',
            'price': '可转债价格',
            'turnover_rt': '换手率',
            # 可以根据需要添加其他列
        }
        df = df.rename(columns=rename_map)
        
        # 设置索引
        df = df.set_index('可转债代码', drop=True)
        
        return df
        
    def save_turnover_rates(self, df):
        """保存换手率数据"""
        try:
            os.makedirs("data", exist_ok=True)
            
            # 准备新数据
            turnover_data = df.reset_index()
            turnover_data = turnover_data[['可转债代码', '可转债名称', '换手率']].copy()
            turnover_data['date'] = self.date
            
            # 读取已有数据(如果文件存在)
            if os.path.exists(self.turnover_file):
                existing_data = pd.read_csv(self.turnover_file)
                # 移除多余的列
                existing_data = existing_data[['可转债代码', '可转债名称', '换手率', 'date']]
                # 移除同一天的数据
                existing_data = existing_data[existing_data['date'] != self.date]
                # 合并新旧数据
                turnover_data = pd.concat([existing_data, turnover_data], ignore_index=True)
            
            # 保存时不生成额外的索引列
            turnover_data.to_csv(self.turnover_file, index=False)
                
            logger.info(f"成功保存{len(turnover_data)}条换手率数据，日期：{self.date}")
            
        except Exception as e:
            logger.error(f"保存换手率数据失败: {e}")
            
    def run(self):
        """运行数据获取流程"""
        data = self.get_data()
        if data:
            df = self.process_data(data)
            if df is not None:
                self.save_turnover_rates(df)
            return df
        return None


def test_demo():
    """测试获取历史数据"""
    from datetime import datetime, timedelta
    
    today = datetime.now()
    test_dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)]
    
    for date in test_dates:
        try:
            print(f"\n获取 {date} 的数据...")
            obj = Jisilu(date)
            df = obj.run()
            
            if df is not None:
                print(f"成功获取数据，共 {len(df)} 条记录")
                print("\n换手率前5名：")
                print(df[['可转债名称', '换手率']].sort_values('换手率', ascending=False).head())
            else:
                print(f"获取 {date} 数据失败")
                
            time.sleep(1)  # 避免请求过快
            
        except Exception as e:
            print(f"处理 {date} 数据时出错: {e}")

def main():
    """获取当天数据"""
    obj = Jisilu()
    obj.run()

if __name__ == '__main__':
    test_demo()

