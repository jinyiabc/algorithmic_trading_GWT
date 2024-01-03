from time import sleep

import numpy as np
import pandas as pd
from xtquant.xtdata import get_market_data
from datetime import datetime
from helper.mysql_dbconnection import mysql_dbconnection
from helper.utility import get_long_price, get_short_price, get_current_time, MyXtQuantTrader, MyXtQuantTraderCallback, \
    get_order_details, get_trade_details, get_asset_details, get_position_details, \
    get_credit_account_details, get_compact_details, get_stock_price, func2, align_df, \
    timetag_to_datetimeS, add_tick_data_db, add_minute_data_db, fetchall_data, get_qty, clear_position, enter_position, \
    enter_position1, clear_position1, check_order_cancel_if_not_executed, decide_short_price, enter_position2, \
    get_short_price1, get_symbols_price, get_recent_trade_price


def test_func1():
    stock_list = ['600519.SH', '601318.SH']
    period = '1d'
    dividend_type = 'front'
    fields = ['time', 'low', 'close', 'open']
    start_time = '20230317'
    end_time = '20230318'
    df = get_stock_price(fields,stock_list, start_time, end_time,period,dividend_type)
    # test for time
    assert df['time'][0] == '20230317'
    assert df['time'][-1] == '20230317'
    # test for symbols
    for i in range(len(stock_list)):
        assert df['symbols'][i] == stock_list[i]

    # test for fields
    np.testing.assert_array_equal(df['open'],[[1770.], [45.81]])
    np.testing.assert_array_equal(df['close'],[[1742. ],[  46.2]])
    np.testing.assert_array_equal(df['low'], [[1736.  ],[  45.81]])

"""Tick"""
def test_get_skock_price():
    symbols = ['510350.SH', '510330.SH']
    field_list = ['time', 'lastPrice', 'open', 'high', 'low', 'lastClose', 'amount', 'volume', 'pvolume', 'stockStatus',
                  'openInt', 'lastSettlementPrice', \
                  'askPrice', 'bidPrice', 'askVol', 'bidVol']
    start_time = '20230517093000'
    end_time = '20230517150000'
    func2(symbols, start_time, end_time, 'tick')
    df = get_stock_price(field_list, symbols, start_time, end_time, 'tick', 'none', -1)
    print(df)
    df1 = align_df(symbols, df,field_list)
    print(df1)
    # df = pd.DataFrame.from_dict(df)
    # database = 'market_research'
    # table_name = 'portfolio'
    # db_engine = mysql_dbconnection(database=database)
    # try:
    #     # Save the data into the database
    #     df.to_sql(table_name, db_engine, if_exists='append',index=False)
    # except Exception as e:
    #     print(": SQL Exception :%s" % e)
"""1m"""
def test_get_stock_price1():
    stock_list = ['600519.SH', '601318.SH']
    period = '1m'
    start_time = '20220217'
    end_time = '20220218'
    dividend_type = 'front'
    fields = ['time', 'low', 'close', 'open']
    df = get_stock_price(fields,stock_list, start_time, end_time,period,dividend_type)
    print(df)

"""Fetch data from MYSQL"""
def test_get_port_price():
    symbols = ['510300.SH', '510330.SH']
    # prices=get_long_price(symbols)
    # print(prices)
    long1, short1 = get_long_price(symbols)
    short2, long2 = get_short_price(symbols)
    print(long1,short1)
    print(short2,long2)

def test_get_short_pirce1():
    stock_code='510330.SH'
    price = get_short_price1(stock_code)
    print(price)

def test_add_minute_data_db():
    symbols = ['510350.SH', '510330.SH']
    count = -1
    start_time,end_time=get_current_time()
    start='20230522'
    end='20230522'
    func2(symbols, start, end, '1m')
    add_minute_data_db(count,start,end)


def test_add_tick_data_db():
    symbols = ['510350.SH', '510330.SH']
    count = -1
    start_time,end_time=get_current_time()
    start='20230522'
    end='20230522'
    func2(symbols, start, end, 'tick')
    add_tick_data_db(count,start,end)


"""Get current time"""
def test_get_current_time():
    start_time, end_time = get_current_time(duration=1)
    print(start_time,end_time)

"""Cancel Orders"""
def test_cancel_order_stock():
    import random
    from xtquant.xttype import StockAccount
    session_id = random.randint(0, 10000)
    xt_trader = MyXtQuantTrader(session_id)
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    acc = StockAccount('140080060269','CREDIT')
    xt_trader.start()
    connect_result = xt_trader.connect()
    status = xt_trader.subscribe(acc)

    order_ids=[1745879054, 1745879055]
    for order in order_ids:
        cancel_result = xt_trader.cancel_order_stock(acc, order)
        if cancel_result == -1:
            print("Failed to cancel order.")
        else:
            print("Cancel order sucessfully.")
    xt_trader.stop()

"""购买 portfolio"""
def test_enter_position():
    import random
    from xtquant.xttype import StockAccount
    session_id = random.randint(0, 10000)
    xt_trader = MyXtQuantTrader(session_id)
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    acc = StockAccount('140080060269','CREDIT')
    xt_trader.start()
    connect_result = xt_trader.connect()
    status = xt_trader.subscribe(acc)

    symbols=['510350.SH','510330.SH']
    hedge_ratio=[1, -1]
    captital=1000

    price = get_long_price(symbols)
    qty = get_qty(hedge_ratio, price, captital)
    order_id=enter_position(xt_trader,acc,symbols,price,qty,strategyFlag='s1')
    print(order_id[0],order_id[1])
    xt_trader.stop()

"""卖出 portfolio"""
def test_clear_position():
    import random
    from xtquant.xttype import StockAccount
    session_id = random.randint(0, 10000)
    xt_trader = MyXtQuantTrader(session_id)
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    acc = StockAccount('140080060269', 'CREDIT')
    xt_trader.start()
    connect_result = xt_trader.connect()
    status = xt_trader.subscribe(acc)

    symbols = ['510350.SH', '510330.SH']
    hedge_ratio = [-1, 1]
    captital = 1000
    price = get_short_price(symbols)
    qty = get_qty(hedge_ratio, price, captital)

    order_id=clear_position(xt_trader,acc,symbols,price,qty,strategyFlag='s1')
    print(order_id[0], order_id[1])
    xt_trader.stop()

def test_enter_position1_long():
    symbols=['510300.SH','510330.SH']
    order_id=enter_position1(symbols,longShortFlag='long', strategyFlag='s1')
    print(order_id)

def test_enter_position1_short():
    symbols=['510300.SH','510330.SH']
    order_id=enter_position1(symbols,longShortFlag='short', strategyFlag='s1')
    print(order_id)

def test_enter_position2_long():
    stock_code='510300.SH'
    captital = 500
    order_id=enter_position2(stock_code,captital,longShortFlag='long', strategyFlag='s1')
    print(order_id)
    check_order_cancel_if_not_executed(stock_code)

def test_enter_position2_short():
    stock_code='510330.SH'
    captital = 500
    order_id=enter_position2(stock_code,captital,longShortFlag='short', strategyFlag='s1')
    print(order_id)
    # sleep(2)
    # check_order_cancel_if_not_executed(stock_code)

def test_clear_position1():
    symbols=['510350.SH','510330.SH']
    order_id=clear_position1(symbols, strategyFlag='s1')
    print(order_id)

def test_get_smbols_price():
    symbols = ['510300.SH', '510330.SH']
    df=get_symbols_price(symbols)
    print(df)

def test_get_recent_trade_price():
    import random
    from xtquant.xttype import StockAccount
    session_id = random.randint(0, 10000)
    xt_trader = MyXtQuantTrader(session_id)
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    acc = StockAccount('140080060269', 'CREDIT')
    xt_trader.start()
    connect_result = xt_trader.connect()
    status = xt_trader.subscribe(acc)
    symbols = ['510300.SH', '510330.SH']
    for stock_code in symbols:
        traded_price=get_recent_trade_price(xt_trader, acc, stock_code)
        print(traded_price)
    status = xt_trader.unsubscribe(acc)
    xt_trader.stop()


"""根据订单编号查询委托"""
def test_query_stock_orders():
    import random
    from xtquant.xttype import StockAccount
    session_id = random.randint(0, 10000)
    xt_trader = MyXtQuantTrader(session_id)
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    acc = StockAccount('140080060269', 'CREDIT')
    xt_trader.start()
    connect_result = xt_trader.connect()
    status = xt_trader.subscribe(acc)
    print("="*40)
    print("ORDER:")
    orders  = xt_trader.query_stock_orders(acc,  cancelable_only = False)
    if orders :
        order_details=get_order_details(orders)
        print(order_details)
    status = xt_trader.unsubscribe(acc)
    xt_trader.stop()

def test_get_qty():
    symbols = ['510350.SH', '510330.SH']
    database = 'market_research'
    table_name = 'quote'
    field = "stock,time,lastPrice,askPrice1,bidPrice1"
    data=fetchall_data(database,table_name,field)
    lastPrice=[data[data['stock'] == stock].iloc[-1]['lastPrice'] for stock in symbols]
    askPrice1=[data[data['stock'] == stock].iloc[-1]['askPrice1'] for stock in symbols]
    bidPrice1=[data[data['stock'] == stock].iloc[-1]['bidPrice1'] for stock in symbols]
    midquotePrice=[(askPrice1[i]+bidPrice1[i])/2 for i,stock in enumerate(symbols)]
    # long portfolid, 1st long->ask, 2nd short->bid
    longPrice=[askPrice1[0],bidPrice1[1]]
    # Short portfolid, 1st short->bid, 2nd long->ask
    shortPrice=[bidPrice1[0],askPrice1[1]]
    price=longPrice
    captital=10000
    hedge_ratio=[1,-1]
    long_qty=get_qty(hedge_ratio, longPrice, captital)
    hedge_ratio = [-1, 1]
    short_qty = get_qty(hedge_ratio, shortPrice, captital)
    print(long_qty,short_qty)

"""查询当日所有的成交"""
def test_get_trade_details():
    import random
    from xtquant.xttype import StockAccount
    session_id = random.randint(0, 10000)
    xt_trader = MyXtQuantTrader(session_id)
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    acc = StockAccount('140080060269', 'CREDIT')
    xt_trader.start()
    connect_result = xt_trader.connect()
    status = xt_trader.subscribe(acc)
    trades = xt_trader.query_stock_trades(acc)
    if trades:
        trade_details=get_trade_details(trades)
        print(trade_details)
    status = xt_trader.unsubscribe(acc)
    xt_trader.stop()

"""查询证券资产"""
def test_get_asset_details():
    import random
    from xtquant.xttype import StockAccount
    session_id = random.randint(0, 10000)
    xt_trader = MyXtQuantTrader(session_id)
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    acc = StockAccount('140080060269', 'CREDIT')
    xt_trader.start()
    connect_result = xt_trader.connect()
    status = xt_trader.subscribe(acc)
    # 查询证券资产
    print("=" * 40)
    print("ASSET:")
    assets = xt_trader.query_stock_asset(acc)
    if assets:
        asset_detail=get_asset_details(assets)
        print(asset_detail)
    status = xt_trader.unsubscribe(acc)
    xt_trader.stop()

"""查询当日所有的持仓"""
def test_get_position_details():
    import random
    from xtquant.xttype import StockAccount
    session_id = random.randint(0, 10000)
    xt_trader = MyXtQuantTrader(session_id)
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    acc = StockAccount('140080060269', 'CREDIT')
    xt_trader.start()
    connect_result = xt_trader.connect()
    status = xt_trader.subscribe(acc)
    # 查询当日所有的持仓
    print("=" * 40)
    print("POSITIONS:")
    positions = xt_trader.query_stock_positions(acc)
    if len(positions) != 0:
        position_details=get_position_details(positions)
        print(position_details)
    status = xt_trader.unsubscribe(acc)
    xt_trader.stop()

"""信用查询接口"""
def test(xt_trader,acc):
    # 信用查询接口
    print("=" * 40)
    print("CREDIT ACCOUNT:")
    credit_account = xt_trader.query_credit_detail(acc)
    if credit_account:
        credit_account_details=get_credit_account_details(credit_account)
        print(credit_account_details)
        # for credit_detail in datas:
        #     print(credit_detail.account_id, account_type_num2str(credit_detail.account_type),
        #           credit_detail.m_nStatus)

"""compacts"""
def test(xt_trader,acc):
    print("COMPACTS:")
    compacts = xt_trader.query_stk_compacts(acc)
    if compacts:
        compact_details=get_compact_details(compacts)
        print(compact_details)

"""Monitor Order Execution"""
def test_order_status():
    """Monitor Order Execution"""
    stock_code='510330.SH'
    check_order_cancel_if_not_executed(stock_code, syncFlag=True)

def test_func2():
    symbols=['510350.SH','510330.SH']
    period = 'tick'
    start_time = '20230522'
    end_time = '20230522'
    func2(symbols, start_time, end_time, period)

def test_func3():
    stock_list = ['600519.SH', '601318.SH']
    period = '1m'
    start_time = '20230522'
    end_time = '20230522'
    func2(stock_list, start_time, end_time, period)

def test_decide_short_price():
    stock_code='510330.SH'
    bid_price=3.7
    last_price=3.6
    price=decide_short_price(stock_code, bid_price, last_price)
    print(price)