#coding:gbk

def init(ContextInfo):
	print("hello init")
	ContextInfo.set_universe(['127047.SZ'])
	ContextInfo.x = 0
	account = '6000000223'
	C.acct = account
	C.accoutType = 'STOCK'
	C.buy_code = 23 if C.accoutType.lower() == 'stock' else 33
	
def handlebar(ContextInfo):
	df = ContextInfo.get_market_data(['close'], stock_code = ContextInfo.get_universe(), skip_paused = True, period = '1d', dividend_type = 'front')
	print("今日价格", df)
	if df < 100:
		order_shares('127047.SZ', 100, ContextInfo, 'testS')
		print("买入100股")
	if df > 105:
		order_shares('127047.SZ', -200, ContextInfo, 'testS')
		print("卖出200股")
	
	ContextInfo.x += 1
	print("hello handlebar")
	d = ContextInfo.barpos
	t = ContextInfo.get_bar_timetag(d)
	date = timetag_to_datetime(t, "%y%m%d")
	print(d,t,date)
	print("x："+str(ContextInfo.x))
	

	ipoStock=get_ipo_data("STOCK")#返回新股信息
	print('当日新股', ipoStock)
	limit_info = get_new_purchase_limit(C.acct)
	print('账户限额', limit_info)
	stock_volume_dict = {i : ipoStock[i]['maxPurchaseNum'] for i in ipoStock}
	stock_price_dict = {i : ipoStock[i]['issuePrice'] for i in ipoStock}
	for stock in stock_volume_dict:
		market = stock[-2:]
		if market not in limit_info:
			print(market, limit_info, '缺少限制信息')
			continue
			stock_volume_dict[stock] = min(stock_volume_dict[stock], limit_info[market])
	print('新股可申字典', stock_volume_dict)
	for stock in stock_volume_dict:
		if not stock_volume_dict[stock] >0:
		print(f"{stock} {C.get_stock_name(stock)} 可申购数量不大于0 跳过申购")
		continue
		passorder(C.buy_code,1101, C.acct, stock,11,stock_price_dict[stock], stock_volume_dict[stock],'新股申购',2,stock,C)
		print(f"新股申购 {stock} {stock_volume_dict[stock]}股")

	ipobond=get_ipo_data("BOND")#返回新债信息
	print('当日新债', ipobond)
	bond_volume_dict = {i : ipobond[i]['maxPurchaseNum'] for i in ipobond}
	bond_price_dict = {i : ipobond[i]['issuePrice'] for i in ipobond}
	print('新债可申字典', bond_volume_dict)
	for bond in stock_volume_dict:
		passorder(C.buy_code,1101, C.acct, bond,11,bond_price_dict[bond], bond_volume_dict[bond],'新债申购',2,bond,C)
		print(f"新债申购 {bond} {bond_volume_dict[bond]}张")