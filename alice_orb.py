from alice_blue import *
import csv
import datetime
import time
import document_details

username = document_details.username
password = document_details.password
twoFA = document_details.twoFA
api_secret = document_details.api_secret
app_id = document_details.app_id

alice = None
socket_opened = False

open_position = {}
close_position = []


def event_handler_quote_update(message):
	gettingData(message)


def open_callback():
	global socket_opened
	socket_opened = True


def open_socket_now():
	alice.start_websocket(
		subscribe_callback=event_handler_quote_update,
		socket_open_callback=open_callback,
		run_in_background=True,
	)
	while socket_opened == False:
		pass


def main():
	global alice, tickerlist

	access_token = AliceBlue.login_and_get_access_token(
		username=username,
		password=password,
		twoFA=twoFA,
		api_secret=api_secret,
		app_id=app_id,
	)

	with open('access_token.txt', 'w') as wr1:
		wr = csv.writer(wr1)
		wr.writerow([access_token])
	access_token = open('access_token.txt', 'r').read().strip()
	# access_token = "VjHKNcvH3YiHv6FHPvf1RPfzbf_2jyr4MRoHL2XqNJk.Mff4cDQOjJupXE-ZQcUQaA6Nth8gynI0VytRJ5Kqffk"
	alice = AliceBlue(username=username,
					  password=password,
					  access_token=access_token)

	if socket_opened == False:
		open_socket_now()

	orderplacetime = int(9) * 60 + int(20)
	closingtime = int(15) * 60 + int(9)
	timenow = (datetime.datetime.now().hour * 60 +
			   datetime.datetime.now().minute)
	print("Waiting for 9.20 AM , CURRENT TIME:{}".format(
		datetime.datetime.now()))

	while timenow < orderplacetime:
		time.sleep(0.2)
		timenow = (datetime.datetime.now().hour * 60 +
				   datetime.datetime.now().minute)
	print("Ready for trading, CURRENT TIME:{}".format(datetime.datetime.now()))

	while True:
		tickerlist = [
			"ACC", "AUBANK", "AARTIIND", "ABBOTINDIA", "ADANIENT",
			"ADANIGREEN", "ADANIPORTS", "ATGL", "ADANITRANS", "AJANTPHARM",
			"ALKEM", "AMARAJABAT", "AMBUJACEM", "APOLLOHOSP", "APOLLOTYRE",
			"ASHOKLEY", "ASIANPAINT", "AUROPHARMA", "DMART", "AXISBANK",
			"BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BAJAJHLDNG",
			"BALKRISIND", "BANDHANBNK", "BANKBARODA", "BANKINDIA", "BATAINDIA",
			"BERGEPAINT", "BEL", "BHARATFORG", "BHEL", "BPCL", "BHARTIARTL",
			"BIOCON", "BBTC", "BOSCHLTD", "BRITANNIA", "CESC", "CADILAHC",
			"CANBK", "CASTROLIND", "CHOLAFIN", "CIPLA", "COALINDIA", "COFORGE",
			"COLPAL", "CONCOR", "COROMANDEL", "CROMPTON", "CUMMINSIND", "DLF",
			"DABUR", "DIVISLAB", "LALPATHLAB", "DRREDDY", "EDELWEISS",
			"EICHERMOT", "EMAMILTD", "ENDURANCE", "ESCORTS", "EXIDEIND",
			"FEDERALBNK", "FORTIS", "FRETAIL", "GAIL", "GICRE", "GLENMARK",
			"GODREJAGRO", "GODREJCP", "GRASIM", "GUJGASLTD", "GSPL", "HCLTECH",
			"HDFCAMC", "HDFCBANK", "HDFCLIFE", "HAVELLS", "HEROMOTOCO",
			"HINDALCO", "HINDPETRO", "HINDUNILVR", "HINDZINC", "HDFC",
			"ICICIBANK", "ICICIGI", "ICICIPRULI", "ISEC", "IDFCFIRSTB", "ITC",
			"IBULHSGFIN", "INDHOTEL", "IOC", "IRCTC", "IGL", "INDUSINDBK",
			"NAUKRI", "INFY", "INDIGO", "IPCALAB", "JSWENERGY", "JSWSTEEL",
			"JINDALSTEL", "JUBLFOOD", "KOTAKBANK", "L&TFH", "LICHSGFIN", "LT",
			"LUPIN", "MRF", "MGL", "M&MFIN", "M&M", "MANAPPURAM", "MARICO",
			"MARUTI", "MFSL", "MINDTREE", "MOTHERSUMI", "MPHASIS",
			"MUTHOOTFIN", "NATCOPHARM", "NMDC", "NTPC", "NATIONALUM",
			"NAVINFLUOR", "NESTLEIND", "OBEROIRLTY", "ONGC", "OIL", "OFSS",
			"PIIND", "PAGEIND", "PETRONET", "PFIZER", "PIDILITIND", "PEL",
			"PFC", "POWERGRID", "PRESTIGE", "PGHH", "PNB", "RBLBANK", "RECLTD",
			"RELIANCE", "SBICARD", "SBILIFE", "SRF", "SHREECEM", "SRTRANSFIN",
			"SIEMENS", "SBIN", "SAIL", "SUNPHARMA", "SUNTV", "SYNGENE",
			"TVSMOTOR", "TATACHEM", "TCS", "TATACONSUM", "TATAMOTORS",
			"TATAPOWER", "TATASTEEL", "TECHM", "RAMCOCEM", "TITAN",
			"TORNTPHARM", "TORNTPOWER", "TRENT", "UPL", "ULTRACEMCO",
			"UNIONBANK", "UBL", "MCDOWELL-N", "VGUARD", "VBL", "IDEA",
			"VOLTAS", "WIPRO", "YESBANK", "ZEEL"
		]
		for i in tickerlist:
			instrument = alice.get_instrument_by_symbol("NSE", i)
			alice.subscribe(instrument, LiveFeedType.MARKET_DATA)
		time.sleep(1000)


def gettingData(message):
	# print(message)
	script = message["instrument"].symbol
	lot_size = message["instrument"].lot_size
	ltp = message["ltp"]
	high = message["high"]
	low = message["low"]
	openL = message["open"]
	volume = message["volume"]
	ltt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(message["ltt"]))

	# if (ltp == low) and (script not in open_position):
	#     placeOrder("BUY", script, ltp)

	if (ltp == high) and (script not in open_position):
	    placeOrder("SELL", script, ltp)

	if (script in open_position) and (script not in close_position) and (ltt[-8:] < "13:30:00"):
	    orderManagement(ltp, script)

	if (script in open_position) and (script not in close_position) and (ltt[-8:] == "13:30:00"):
	    closingPosition(ltp, script)


def placeOrder(order, script, ltp):
	if order == "BUY":
		quantity = int(5)
		target_price = round(ltp + 2, 1)
		stoploss_price = round(ltp - 2, 1)
		open_position[script] = {
			"price": ltp,
			"quantity": quantity,
			"order": order,
			"target_price": target_price,
			"stoploss_price": stoploss_price
		}
		order = alice.place_order(transaction_type=TransactionType.Buy,
								  instrument=alice.get_instrument_by_symbol(
									  'NSE', script),
								  quantity=quantity,
								  order_type=OrderType.Limit,
								  product_type=ProductType.Intraday,
								  price=ltp,
								  trigger_price=None,
								  stop_loss=None,
								  square_off=None,
								  trailing_sl=None,
								  is_amo=False)
		print(
			f"Buy Order Placed for {script}, at Price: {ltp} for Quantity: {quantity}, with order_id: {order['data']['oms_order_id']} at time: {datetime.datetime.now()}"
		)
	else:
		quantity = int(5)
		target_price = round(ltp - 2, 1)
		stoploss_price = round(ltp + 2, 1)
		open_position[script] = {
			"price": ltp,
			"quantity": quantity,
			"order": order,
			"target_price": target_price,
			"stoploss_price": stoploss_price
		}
		order = alice.place_order(transaction_type=TransactionType.Sell,
								  instrument=alice.get_instrument_by_symbol(
									  'NSE', script),
								  quantity=quantity,
								  order_type=OrderType.Limit,
								  product_type=ProductType.Intraday,
								  price=ltp,
								  trigger_price=None,
								  stop_loss=None,
								  square_off=None,
								  trailing_sl=None,
								  is_amo=False)
		print(
			f"Sell Order Placed for {script}, at Price: {ltp} for Quantity: {quantity}, with order_id: {order['data']['oms_order_id']} at time: {datetime.datetime.now()}"
		)


def orderManagement(ltp, script):
	target = open_position[script]["target_price"]
	stoploss = open_position[script]["stoploss_price"]
	quantity = open_position[script]["quantity"]

	if (ltp == target) | (ltp == stoploss):
		close_position.append(script)

		if open_position[script]["order"] == "BUY":
			order = alice.place_order(
				transaction_type=TransactionType.Sell,
				instrument=alice.get_instrument_by_symbol('NSE', script),
				quantity=quantity,
				order_type=OrderType.Limit,
				product_type=ProductType.Intraday,
				price=ltp,
				trigger_price=None,
				stop_loss=None,
				square_off=None,
				trailing_sl=None,
				is_amo=False)
			print(
				f"Position Closed for {script}, at Price: {ltp} for Quantity: {quantity}, with order_id: {order['data']['oms_order_id']} at time: {datetime.datetime.now()}"
			)

		else:
			order = alice.place_order(
				transaction_type=TransactionType.Buy,
				instrument=alice.get_instrument_by_symbol('NSE', script),
				quantity=quantity,
				order_type=OrderType.Limit,
				product_type=ProductType.Intraday,
				price=ltp,
				trigger_price=None,
				stop_loss=None,
				square_off=None,
				trailing_sl=None,
				is_amo=False)
			print(
				f"Position Closed for {script}, at Price: {ltp} for Quantity: {quantity}, with order_id: {order['data']['oms_order_id']} at time: {datetime.datetime.now()}"
			)
	else:
		pass


def closingPosition(ltp, script):
	quantity = open_position[script]["quantity"]
	close_position.append(script)

	if open_position[script]["order"] == "BUY":
		order = alice.place_order(
			transaction_type=TransactionType.Sell,
			instrument=alice.get_instrument_by_symbol('NSE', script),
			quantity=quantity,
			order_type=OrderType.Limit,
			product_type=ProductType.Intraday,
			price=ltp,
			trigger_price=None,
			stop_loss=None,
			square_off=None,
			trailing_sl=None,
			is_amo=False)
		print(
			f"Position Closed for {script}, at Price: {ltp} for Quantity: {quantity}, with order_id: {order['data']['oms_order_id']} at time: {datetime.datetime.now()}"
		)

	else:
		order = alice.place_order(
			transaction_type=TransactionType.Buy,
			instrument=alice.get_instrument_by_symbol('NSE', script),
			quantity=quantity,
			order_type=OrderType.Limit,
			product_type=ProductType.Intraday,
			price=ltp,
			trigger_price=None,
			stop_loss=None,
			square_off=None,
			trailing_sl=None,
			is_amo=False)
		print(
			f"Position Closed for {script}, at Price: {ltp} for Quantity: {quantity}, with order_id: {order['data']['oms_order_id']} at time: {datetime.datetime.now()}"
		)

if __name__ == "__main__":
	main()
