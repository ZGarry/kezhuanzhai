import akshare as ak
import pandas as pd

df = ak.bond_zh_cov()


def getNameFromCode(stock_code):
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
    if num.is_integer():
        return str(int(num))
    else:
        return "{:.2f}".format(num)

# 同时带上了总市值信息


def get_all_data():
    import akshare as ak

    all_cube = get_data()

    all_stock = ak.stock_zh_a_spot_em()
    # 使用 merge 方法关联表A和表B，基于正股代码列
    merged_df = pd.merge(all_cube, all_stock, left_on='正股代码', right_on='代码', how='left')
    all_cube['正股总市值'] = merged_df['总市值']

    if len(all_cube) < 100:
        raise Exception

    return all_cube


def to_long_name(code):
    post_fix = 'SZ' if code.startswith('12') else 'SH'
    code = '{}.{}'.format(code, post_fix)
    return code


def get_data():
    import akshare as ak
    import webbrowser
    url = "https://app.jisilu.cn/data/cbnew/#cb"
    webbrowser.open(url)
    s = gen_cookie()
    for i in range(20):
        bond_cb_jsl_df = ak.bond_cb_jsl(cookie=s)
        if len(bond_cb_jsl_df) > 300:
            return bond_cb_jsl_df
    raise Exception('执行了一定次数最后还是没有跑完')


def gen_cookie():
    import time

    # 获取当前的秒级时间戳
    timestamp = int(time.time())*1000
    cookie = f"kbz_newcookie=1; kbz__user_login=1ubd08_P1ebax9aXXB4WRiEuSR_7lbSi2drf6tnl09fWvpvHqt_YzKnPrZupk6PZwqCRqt2noN6gp8XckquskamYq5qwlu7V28DTjKSokaKZpLGWpKaty8DTjKSvkaGXpKmtnKmNso_LotHVjL3Q7uLh1dqbrJCmgZvPyt7F4_DoicfAl5Omj6OzgcfK4q-ppJnkrZafgbTo0dzGy97XtOLgppepmKGrl5CJv8HJtsWYl87fzNiYqNXE3-ieibzU6dHjxqKpkqmPpKell6mMysPcwuXhkKWUq6eonw..; kbzw__Session=ermpq6dp20spnhfpo4r0ot45t4; Hm_lvt_164fe01b1433a19b507595a43bf58262={timestamp}; kbzw__user_login=7Obd08_P1ebax9aXXB4WRiUtWyf7kZyh6dbc7OPm1Nq_1KLZrsfTxKTcq6KsnqfD15GnrdeqmNWVpNzbmrGgp5utmJiyoO3K1L_RpKaZqZ6vkq6CsqS0zL_NjKWwpZqvoquZr5OYsqDNos6-n8bk4-LY48OllqWnk6C42c_Y6OzcmbrLgqeRpaeumLjZz6qtsInxoquLlqLn59_duNXDv-LpmK6frpCpl5efvsC1va2gmeHS5NGXqdvE4uacmKTY0-Pm2piqnbCQpo-npaOYtNHH1evemK6frpCplw..; Hm_lpvt_164fe01b1433a19b507595a43bf58262=1701664800; SERVERID=0e73f01634e37a9af0b56dfcd9143ef3|1701664816|1701664770"
    return cookie
