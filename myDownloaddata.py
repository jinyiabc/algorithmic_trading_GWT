from datetime import timedelta

from xtquant import xtdata
from xtquant.xtdata import subscribe_quote, get_market_data, subscribe_whole_quote, unsubscribe_quote, get_local_data, \
    download_history_data2, run, get_trading_dates, reconnect, get_client, CLIENT
import pandas as pd

from xtquant.xttrader import XtQuantTrader

from helper.utility import get_stock_price


def on_data(datas):
    for stock_code in datas:
        	print(stock_code, datas[stock_code])
def on_progress(data):
	print(data)
	# {'finished': 1, 'total': 50, 'stockcode': '000001.SZ', 'message': ''}

if __name__ == "__main__":
    # path = 'D:\\长城策略交易系统\\userdata_mini'
    # # session_id为会话编号，策略使用方对于不同的Python策略需要使用不同的会话编号
    # session_id = 123457
    # xt_trader = XtQuantTrader(path, session_id)


    # seq = subscribe_quote('510810.SH', period='1d', start_time = '20230317',end_time = '20230318', callback=on_data)
    # print(seq)
    # unsubscribe_quote(seq)
    # seq1 = subscribe_whole_quote(['510810.SH'], callback=None)
    # print(seq1)

    # stock_code = pd.read_csv(f'S:\\A_STOCK\\LONGSHORT_ALL.CSV')['Symbol'].tolist()

    # # empty list to read list from a file
    # add_stock = []
    #
    # # open file and read the content in a list
    # with open(r'temp_data\add_stock.txt', 'r') as fp:
    #     for line in fp:
    #         # remove linebreak from a current name
    #         # linebreak is the last character of each line
    #         x = line[:-1]
    #
    #         # add current item to the list
    #         add_stock.append(x)
    #
    # # display list
    # print(add_stock)
    #
    #

    stock_list = ['510350.SH','510330.SH']
    start_time='20230517'
    end_time='20230517'
    download_history_data2(stock_list,
                           start_time=start_time,
                           end_time=end_time,
                           period='tick',
                           callback=on_progress)
    fields=['time','lastPrice','open','high','low','lastClose','amount','volume','pvolume',\
                'stockStatus','openInt','lastSettlementPrice','askPrice','bidPrice','askVol','bidVol']
    df = get_market_data(field_list=fields,
                        stock_list=stock_list,
                        start_time=start_time, end_time=end_time,
                        period='tick',
                        dividend_type='none',
                        fill_data=None)
    print(df[stock_list[0]]['open'])
    print(df[stock_list[1]]['open'])
    df1=get_stock_price(fields, stock_list, start_time, end_time, 'tick', 'none', -1)
    print(df1['lastPrice'])
    print("download completed!")
