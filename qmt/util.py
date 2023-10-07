import akshare as ak

df = ak.bond_zh_cov()


def getNameFromCode(stock_code):
    bond_code = stock_code.split(".")[0]
    return df.loc[df["债券代码"] == bond_code, "债券简称"].values[0]
