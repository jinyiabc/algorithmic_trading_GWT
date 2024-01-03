from datetime import timedelta

import numpy as np
from xtquant import xtdata
from xtquant.xtdata import subscribe_quote, get_market_data, subscribe_whole_quote, unsubscribe_quote, get_local_data, \
    download_history_data2, run, get_trading_dates, reconnect, get_client, CLIENT, get_client1, \
    get_stock_list_in_sector, get_divid_factors, timetag_to_datetime
import pandas as pd

from xtquant.xttrader import XtQuantTrader


def on_data(datas):
    for stock_code in datas:
        	print(stock_code, datas[stock_code])
def on_progress(data):
	print(data)
	# {'finished': 1, 'total': 50, 'stockcode': '000001.SZ', 'message': ''}
def timetag_to_datetimeS(list):
    times = []
    for item in list:
        times.append(timetag_to_datetime(int(item), '%Y%m%d'))   #  %H:%M:%S
    return times

if __name__ == "__main__":
    stock_list = get_stock_list_in_sector("两融标的")
    stock_list = stock_list[0:10]

    # download_history_data2(add_stock,
    #                        start_time='20220318',
    #                        end_time='20230318',
    #                        period='1m',
    #                        callback=on_progress)

    df = get_market_data(field_list=['time','open','close'],
                        stock_list=stock_list,
                        start_time='20230216093000', end_time='20230216093500',
                        period='1m',
                        dividend_type='none',
                        fill_data=None)
    # print(df)

    print("Get data completed!")

    divid_factor = get_divid_factors(stock_list[0], start_time='', end_time='')
    print(divid_factor.columns)
    print(divid_factor['time'])
    times = divid_factor['time'].tolist()
    print(times)
    # timetag_to_datetime()
    print(timetag_to_datetimeS(times))
    times = timetag_to_datetimeS(times)
    open_none = []
    open_front = []
    open_back = []
    for date in times:
        # download_history_data2([stock_list[0]],
        #                        start_time=date, #'20230216',
        #                        end_time=date,#'20230217',
        #                        period='1d',
        #                        callback=on_progress)
        df_none = get_market_data(field_list=['time','open'],
                                  stock_list=[stock_list[0]],
                                  start_time=date,  # '20230216',
                                  end_time=date,  # '20230217',
                                  count=-1,
                                  period='1d',
                                  dividend_type='none',
                                  fill_data=None)
        df_front = get_market_data(field_list=['time','open'],
                                  stock_list=[stock_list[0]],
                                  start_time=date,  # '20230216',
                                  end_time=date,  # '20230217',
                                  count=-1,
                                  period='1d',
                                  dividend_type='front',
                                  fill_data=None)
        df_back = get_market_data(field_list=['time','open'],
                                  stock_list=[stock_list[0]],
                                  start_time=date,  # '20230216',
                                  end_time=date,  # '20230217',
                                  count=-1,
                                  period='1d',
                                  dividend_type='back',
                                  fill_data=None)
        open_none.append(df_none['open'].values[0][0])
        open_front.append(df_front['open'].values[0][0])
        open_back.append(df_back['open'].values[0][0])
    divid_factor[['none','front','back']] = np.array([open_none,open_front,open_back]).T.tolist()
    divid_factor.to_csv("temp_data/divid_factor.csv")