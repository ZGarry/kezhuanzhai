import akshare as ak

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
