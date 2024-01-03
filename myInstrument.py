from datetime import timedelta

from xtquant import xtdata
from xtquant.xtdata import subscribe_quote, get_market_data, subscribe_whole_quote, unsubscribe_quote, get_local_data, \
    download_history_data2, run, get_trading_dates, reconnect, get_client, CLIENT, get_client1, get_instrument_type, \
    get_sector_list, add_sector, get_stock_list_in_sector, remove_sector, download_sector_data
import pandas as pd

from xtquant.xttrader import XtQuantTrader


if __name__ == "__main__":

    stock_list0 = pd.read_csv(f'S:\\A_STOCK\\LONGSHORT_ALL.CSV')['Symbol'].tolist()

    # add_sector("我的融资融券", stock_list0)
    # stock_list = get_stock_list_in_sector("我的融资融券")
    # print(stock_list)
    # download_sector_data()


    stock_list1 = get_stock_list_in_sector("两融标的")
    # print(stock_list1)
    # print(len(stock_list1))

    mySet0 = set(stock_list0)
    mySet1 = set(stock_list1)

    # Set Difference - print(mySet1.difference(mySet0))
    print(mySet1 - mySet0)
    print(len(mySet1 - mySet0))

    add_stock = list(mySet1 - mySet0)
    # open file in write mode
    with open(r'temp_data/add_stock.txt', 'w') as fp:
        for item in add_stock:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')