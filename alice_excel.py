# pip install xlwings
# xlwings addin install

from alice_blue import *
import csv
import datetime
import time
import document_details
import xlwings as xw
import pandas as pd

username = document_details.username
password = document_details.password
twoFA = document_details.twoFA
api_secret = document_details.api_secret
app_id = document_details.app_id

alice = None
socket_opened = False

sheet = xw.Book("F:/alice/new.xlsx").sheets[0]
tickerlist = []
sheet.range("B1:M300").clear_contents()
buy_traded_stocks = []
sell_traded_stocks = []


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

	with open('access_token.txt','w') as wr1:
		wr=csv.writer(wr1)
		wr.writerow([access_token])
	access_token=open('access_token.txt','r').read().strip()
	# access_token = "9eK6Qq00-gcPMa2_MU_1fAvB7c--E-A-1KkV-b_LXDA.zZunZn0y8K2wdJpQngUhR17NKgnpJrqD54Ef6_uoZrY"
	alice = AliceBlue(username=username,
					  password=password,
					  access_token=access_token)

	if socket_opened == False:
		open_socket_now()

	while True:
		tickerlist = sheet.range("A2").expand("down").value
		for i in tickerlist:
			if i != None:
				instrument = alice.get_instrument_by_symbol("NSE", i.upper())
				alice.subscribe(instrument, LiveFeedType.MARKET_DATA)
		orderPlacement(tickerlist)


def gettingData(message):
	sheet = xw.Book("F:/alice/new.xlsx").sheets[0]
	
	cell_no = 0
	for i in tickerlist:
		if i != None:
			if i.upper() == message["instrument"].symbol:
				cell_no = tickerlist.index(i) + 2

	sheet.range("A1").value = [
		"Script", "Lot_Size", "Ltp", "High", "Low", "Open", "Volume",
		"Condition", "Order_Type", "Quantity", "Order_Status"
	]
	sheet.range(f"B{cell_no}").value = message["instrument"].lot_size
	sheet.range(f"C{cell_no}").value = message["ltp"]
	sheet.range(f"D{cell_no}").value = message["high"]
	sheet.range(f"E{cell_no}").value = message["low"]
	sheet.range(f"F{cell_no}").value = message["open"]
	sheet.range(f"G{cell_no}").value = message["volume"]


def orderPlacement(tickerlist):
	sheet = xw.Book("F:/alice/new.xlsx").sheets[0]
	for i in range(2, (len(tickerlist)+2)):
		Status = sheet.range('I' + str(i)).value
		quantity = sheet.range('J' + str(i)).value
		if (Status != None) & (type(Status) != float) & (type(Status) != int) & (quantity != None) & (type(quantity) != str):
			if (quantity > 0):
				Status = Status.upper()
				quantity = int(quantity)
				Script = sheet.range('A' + str(i)).value
				Script = Script.upper()
				price = sheet.range('C' + str(i)).value
				if (Script not in buy_traded_stocks) and (Status == "BUY"):
					order = alice.place_order(
						transaction_type=TransactionType.Buy,
						instrument=alice.get_instrument_by_symbol('NSE', Script),
						quantity=int(quantity),
						order_type=OrderType.Limit,
						product_type=ProductType.Intraday,
						price=price,
						trigger_price=None,
						stop_loss=None,
						square_off=None,
						trailing_sl=None,
						is_amo=False)
					print(
						f"Buy Order  Placed for {Script}, at Price: {price} for Quantity: {quantity}, with order_id: {order['data']['oms_order_id']} at time: {datetime.datetime.now()}"
					)
					buy_traded_stocks.append(Script)
					sheet.range(f"K{i}").value = "Order Placed"
					sheet.range(f"K{i}").autofit()

				if (Script not in sell_traded_stocks) and (Status == "SELL"):
					order = alice.place_order(
						transaction_type=TransactionType.Sell,
						instrument=alice.get_instrument_by_symbol('NSE', Script),
						quantity=int(quantity),
						order_type=OrderType.Limit,
						product_type=ProductType.Intraday,
						price=price,
						trigger_price=None,
						stop_loss=None,
						square_off=None,
						trailing_sl=None,
						is_amo=False)
					print(
						f"Sell Order  Placed for {Script}, at Price: {price} for Quantity: {quantity}, with order_id: {order['data']['oms_order_id']} at time: {datetime.datetime.now()}"
					)
					sell_traded_stocks.append(Script)
					sheet.range(f"K{i}").value = "Order Placed"
					sheet.range(f"K{i}").autofit()
				else:
					# print(f"Order Already Placed for {Script}")
					pass

if __name__ == "__main__":
	main()