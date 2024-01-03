from xtquant.xtdata import get_stock_list_in_sector

# {'finished': 1, 'total': 50, 'stockcode': '000001.SZ', 'message': ''}

if __name__ == "__main__":
    stock_list = get_stock_list_in_sector("两融标的")
    # stock_list = stock_list[0:10]
    #
    # # download_history_data2(stock_list,
    # #                        start_time='20220318',
    # #                        end_time='20230318',
    # #                        period='1d',
    # #                        callback=on_progress)
    #
    # df = get_market_data(field_list=['time','open','close'],
    #                     stock_list=stock_list,
    #                     start_time='20220318093000', end_time='20230318093000',
    #                     period='1m',
    #                     dividend_type='none',
    #                     fill_data=None)
    # print(df['close']['20230216093000'].to_list())
    # df = func1('20170101', '20220101')
    # def tday_bar(x):
    #     return timetag_to_datetime(int(x), '%Y%m%d')
    # def hhmm_bar(x):
    #     return timetag_to_datetime(int(x), '%H%M')
    # df["tday"] = df['time'].applymap(tday_bar).iloc[0,:]
    # df["hhmm"] = df['time'].applymap(hhmm_bar).iloc[0,:]
    # idx = df["hhmm"] == '0930'
    # open0930 = df['open'][idx].dropna(axis=1, inplace=True)

    # dates = get_trading_dates('SH', start_time='20220217', end_time='20220225', count=-1)
    # dates = timetag_to_datetimeS(dates)
    # print(dates)
    print("Get data completed!")

