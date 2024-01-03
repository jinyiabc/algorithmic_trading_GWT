import sys
from datetime import datetime, timedelta, time
from math import copysign
from time import sleep

import numpy as np
import pandas as pd
from numpy import float64
from xtquant import xtconstant
from xtquant.xtdata import get_market_data, get_trading_calendar, timetag_to_datetime, download_history_data2
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback

from helper.mysql_dbconnection import mysql_dbconnection


class MyXtQuantTrader(XtQuantTrader):
    def __init__(self, session, callback=None):
        path='D:\\gwt\\userdata_mini'
        self.session = session
        super(MyXtQuantTrader, self).__init__(path, session, callback=None)


class MyXtQuantTraderCallback(XtQuantTraderCallback):
    def on_connected(self):
        """
        连接成功推送
        """
        print("connection succsessfully")
        pass

    def on_disconnected(self):
        """
        连接断开
        :return:
        """
        print("connection lost")
    def on_stock_order(self, order):
        """
        委托回报推送
        :param order: XtOrder对象
        :return:
        """
        print("on order callback:")
        print(order.stock_code, order_status_num2str(order.order_status), order.order_sysid)
    def on_stock_asset(self, asset):
        """
        资金变动推送
        :param asset: XtAsset对象
        :return:
        """
        print("on asset callback")
        print(asset.account_id, asset.cash, asset.total_asset)
    def on_stock_trade(self, trade):
        """
        成交变动推送
        :param trade: XtTrade对象
        :return:
        """
        print("on trade callback")
        print(trade.account_id, trade.stock_code, trade.order_id)
    def on_stock_position(self, position):
        """
        持仓变动推送
        :param position: XtPosition对象
        :return:
        """
        print("on position callback")
        print(position.stock_code, position.volume)
    def on_order_error(self, order_error):
        """
        委托失败推送
        :param order_error:XtOrderError 对象
        :return:
        """
        print("on order_error callback")
        print(order_error.order_id, order_error.error_id, order_error.error_msg)
    def on_cancel_error(self, cancel_error):
        """
        撤单失败推送
        :param cancel_error: XtCancelError 对象
        :return:
        """
        print("on cancel_error callback")
        print(cancel_error.order_id, cancel_error.error_id, cancel_error.error_msg)
    def on_order_stock_async_response(self, response):
        """
        异步下单回报推送
        :param response: XtOrderResponse 对象
        :return:
        """
        print("on_order_stock_async_response")
        print(response.account_id, response.order_id, response.seq)
    def on_account_status(self, status):
        """
        :param response: XtAccountStatus 对象
        :return:
        """
        print("on_account_status")
        print(status.account_id, status.account_type, status.status)

def on_data1(datas):
    database = 'market_research'
    table_name = 'etf1m'
    for stock_code in datas:
        #print(stock_code, datas[stock_code])
        stock_code = [stock_code for stock_code in datas][0]
        df = datas[stock_code][0]
        df['stock'] = stock_code
        df['time'] = datetime.fromtimestamp(df['time'] / 1000)
        df['time1'] = datetime.now()
        df['suspendFlag'] = [df['suspendFlag']]
        del df['settlementPrice']
        del df['dr']
        del df['totaldr']
        df = pd.DataFrame.from_dict(df)
        db_engine = mysql_dbconnection(database=database)
        try:
            # Save the data into the database
            df.to_sql(table_name, db_engine, if_exists='append', index=False)
        except Exception as e:
            print(": SQL Exception :%s" % e)
        else:
            print(f": SQL:{stock_code}: successfully updated.")

def on_data(datas):
    # print(datas[stock_code][0])
    stock_code=[stock_code for stock_code in datas][0]
    df=datas[stock_code][0]
    df['stock'] = stock_code
    df['time']=datetime.fromtimestamp(df['time'] / 1000)
    df['time1']=datetime.now()
    df['speed1Min']=[df['speed1Min']]
    # print(df)
    for i,item in enumerate(['askPrice1', 'askPrice2', 'askPrice3', 'askPrice4','askPrice5']):
        df[item]=df['askPrice'][i]
    for i,item in enumerate(['bidPrice1', 'bidPrice2', 'bidPrice3', 'bidPrice4','bidPrice5']):
        df[item]=df['bidPrice'][i]
    for i,item in enumerate(['askVol1', 'askVol2', 'askVol3', 'askVol4','askVol5']):
        df[item]=df['askVol'][i]
    for i,item in enumerate(['bidVol1', 'bidVol2', 'bidVol3', 'bidVol4','bidVol5']):
        df[item]=df['bidVol'][i]
    del df["askPrice"]
    del df["bidPrice"]
    del df["askVol"]
    del df["bidVol"]
    # print(f"{stock_code},{timetag_to_datetime(df['time'], '%Y%m%d %H:%M:%S')},{df['lastPrice']},{midquotePrice}")
    df = pd.DataFrame.from_dict(df)
    database = 'market_research'
    table_name = 'quote'
    db_engine = mysql_dbconnection(database=database)
    try:
        # Save the data into the database
        df.to_sql(table_name, db_engine, if_exists='append',index=False)
    except Exception as e:
        print(": SQL Exception :%s" % e)
    else:
        print(f": SQL:{stock_code}: successfully updated.")

def fetchall_data(database,table_name,field):
    # database = 'market_research'
    # table_name = 'quote'
    # field = "stock,time,lastPrice,askPrice1,bidPrice1"
    # field = field.upper()
    db_engine = mysql_dbconnection(database=database)
    query = ("SELECT " + field + " FROM " + table_name + " ")
    data = pd.read_sql(query, db_engine)
    data.drop_duplicates(inplace=True)
    data.sort_values(by=['time'],inplace=True)
    pd.set_option('display.expand_frame_repr', False)
    if len(data) > 0:
        print("Data found!")
    else:
        print("No data found!")
    # db_engine.close()
    return data


def get_recent_trade_price(xt_trader, acc, stock_code):
    trades = xt_trader.query_stock_trades(acc)
    if trades:
        time=[]
        price=[]
        for trade in trades:
            if trade.stock_code==stock_code and (trade.order_type==xtconstant.CREDIT_FIN_BUY or trade.order_type==xtconstant.CREDIT_BUY) :
                time.append(datetime.fromtimestamp(trade.traded_time))
                price.append(trade.traded_price)
        if len(price) >= 1:
            # print(f"{stock_code} Latest Trade Price: {time[-1]}, {price[-1]}")
            return price[-1]
        else:
            print(f"{stock_code} has not been traded today.")
            return -1
    else:
        print(f"{stock_code} has not been traded today")
        return -1


def get_account_status(xt_trader,syncFlag=True):
    def callback(accounts):
        for account in accounts:
            print(account.account_id, account_type_num2str(account.account_type),
                  account_status_num2str(account.status))
    if not syncFlag:
        # 异步查询账号状态
        xt_trader.query_account_status_async(callback)
    else:
        # 同步查询账号状态
        accounts = xt_trader.query_account_status()
        for account in accounts:
            print(account.account_id, account_type_num2str(account.account_type), account_status_num2str(account.status))


def check_order_cancel_if_not_executed(stock_code,syncFlag=False):
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

    sleep(0.1)
    orders = xt_trader.query_stock_orders(acc, cancelable_only=False)
    if not orders:
        sys.exit('链接失败，程序即将退出')
    # take order_time for sort
    def ascendingOrderTime(elem):
        return elem.order_time
    orders.sort(key=ascendingOrderTime)
    stock_codes = [order.stock_code for order in orders]
    index0=[index for (index, item) in enumerate(stock_codes) if item == stock_code]
    if isinstance(index0, list) and len(index0)>0:
        index = index0[-1]
    else:
        print(f"There is no order for {stock_code}.")
        return
    order_status = order_status_num2str(orders[index].order_status)
    price = orders[index].price
    order_id = orders[index].m_nOrderID
    order_time = datetime.fromtimestamp(orders[index].order_time)
    wait_time = 0
    print(f"Check order step:{wait_time}")
    while True:
        # df = get_market_data(['time', 'close'], [stock_code], '', '', '1m', 'none', 0)
        # latest_price = df['close'][0][-1]
        if (order_status=='ORDER_SUCCEEDED') or (order_status=='ORDER_JUNK'):
            print(f"Check order step:{wait_time}")
            print(f"{order_time}, {orders[index].stock_code}, {order_status_num2str(orders[index].order_status)}")
            break
        elif order_status=='ORDER_REPORTED':
            sleep(1)
            print(f"Check order step:{wait_time}")
            wait_time+=1
        elif order_status == 'ORDER_CANCELED':
            print(f"Check order step:{wait_time}")
            print(f"{order_time}, {orders[index].stock_code}, {order_status_num2str(orders[index].order_status)}")
            break
        if wait_time==5:
            print(f"Check order step:{wait_time}")
            print(f"The order {order_id} not excuted for 5 sec.")
            # print(f"{order_time}, {orders[index].stock_code}, {order_status_num2str(orders[index].order_status)}")
            print(f"cancel the order:{order_id}")
            xt_trader.cancel_order_stock(acc, order_id)
            break

    status = xt_trader.unsubscribe(acc)
    xt_trader.stop()
    return


def get_order_details(orders):
    df = {}
    keys=['m_nOrderID','m_strOrderSysID','m_strStockCode','m_dPrice','m_dTradedPrice','m_nOrderTime','order_status','m_nOrderVolume','m_nTradedVolume']
    for item in keys:
        df[item] = [getattr(o, item) for o in orders]
    df = pd.DataFrame.from_dict(df)
    df['m_nCancelVolume']=df['m_nOrderVolume']-df['m_nTradedVolume']
    df['m_nOrderTime'] = [datetime.fromtimestamp(time) for time in df.m_nOrderTime]
    df['order_status'] = [order_status_num2str(x) for x in df.order_status]
    names=['订单编号','合同编号','证券代码','委托价格','成交价格','委托时间','委托状态','委托量','成交数量','已撤数量']
    df.columns = names
    return df


def get_asset_details(assets):
    df = {}
    keys=['account_type','account_id','cash','frozen_cash','market_value','total_asset']
    for item in keys:
        df[item] = [getattr(o, item) for o in [assets]]
    df = pd.DataFrame.from_dict(df)
    names=['账号类型','资金账号','可用金额','冻结金额','持仓市值','总资产']
    df.columns = names
    return df


def get_position_details(positions):
    df = {}
    keys=['account_type','account_id','stock_code','volume','can_use_volume','open_price','market_value']
    for item in keys:
        df[item] = [getattr(o, item) for o in positions]
    df = pd.DataFrame.from_dict(df)
    names=['账号类型','资金账号','证券代码','持仓数量','可用数量','平均建仓成本','市值']
    df.columns = names
    return df


def get_trade_details(trades):
    df = {}
    keys = ['account_type', 'account_id', 'stock_code', 'order_type', 'traded_id', 'traded_time', \
            'traded_price','traded_volume','traded_amount','order_id','order_sysid','strategy_name','order_remark']
    for item in keys:
        df[item] = [getattr(o, item) for o in trades]
    df = pd.DataFrame.from_dict(df)
    df['traded_time'] = [datetime.fromtimestamp(time) for time in df.traded_time]
    names=['账号类型','资金账号','证券代码','委托类型','成交编号','成交时间', \
           '成交均价','成交数量','成交金额','订单编号','柜台合同编号','策略名称','委托备注']
    df.columns = names
    return df


def get_latest_trading_date(tday):
    start_time = tday.date()-timedelta(days=7)
    start_time=start_time.strftime("%Y%m%d")
    end_time=tday.date().strftime("%Y%m%d")
    trading_dates=get_trading_calendar('SH', start_time=start_time, end_time=end_time, tradetimes=False)
    temp=datetime.strptime(trading_dates[-1], "%Y%m%d")
    return temp.date()


def get_long_price(symbols):
    database = 'market_research'
    table_name = 'quote'
    field = "stock,time,lastPrice,askPrice1,bidPrice1"
    data=fetchall_data(database,table_name,field)
    lastPrice=[data[data['stock'] == stock].iloc[-1]['lastPrice'] for stock in symbols]
    askPrice1=[data[data['stock'] == stock].iloc[-1]['askPrice1'] for stock in symbols]
    bidPrice1=[data[data['stock'] == stock].iloc[-1]['bidPrice1'] for stock in symbols]
    midquotePrice=[(askPrice1[i]+bidPrice1[i])/2 for i,stock in enumerate(symbols)]
    # long portfolid, 1st long->ask, 2nd short->bid
    short_price1=decide_short_price(symbols[1], bidPrice1[1], lastPrice[1])
    longPrice=[askPrice1[0],short_price1]
    # Short portfolid, 1st short->bid, 2nd long->ask
    short_price0 = decide_short_price(symbols[0], bidPrice1[0], lastPrice[0])
    shortPrice=[short_price0,askPrice1[1]]
    price=longPrice
    return price

def get_long_price1(stock_code):
    database = 'market_research'
    table_name = 'quote'
    field = "stock,time,lastPrice,askPrice1,bidPrice1"
    data=fetchall_data(database,table_name,field)
    lastPrice=data[data['stock'] == stock_code].iloc[-1]['lastPrice']
    askPrice1=data[data['stock'] == stock_code].iloc[-1]['askPrice1']
    bidPrice1=data[data['stock'] == stock_code].iloc[-1]['bidPrice1']
    midquotePrice=(askPrice1+bidPrice1)/2
    short_price1=decide_short_price(stock_code, bidPrice1, lastPrice)
    longPrice=askPrice1
    price=longPrice
    return price

def get_short_price1(stock_code):
    database = 'market_research'
    table_name = 'quote'
    field = "stock,time,lastPrice,askPrice1,bidPrice1"
    data=fetchall_data(database,table_name,field)
    lastPrice=data[data['stock'] == stock_code].iloc[-1]['lastPrice']
    askPrice1=data[data['stock'] == stock_code].iloc[-1]['askPrice1']
    bidPrice1=data[data['stock'] == stock_code].iloc[-1]['bidPrice1']
    midquotePrice=(askPrice1+bidPrice1)/2
    short_price1=decide_short_price(stock_code, bidPrice1, lastPrice)
    longPrice=askPrice1
    price=short_price1
    return price

def get_short_price(symbols):
    database = 'market_research'
    table_name = 'quote'
    field = "stock,time,lastPrice,askPrice1,bidPrice1"
    data=fetchall_data(database,table_name,field)
    lastPrice=[data[data['stock'] == stock].iloc[-1]['lastPrice'] for stock in symbols]
    askPrice1=[data[data['stock'] == stock].iloc[-1]['askPrice1'] for stock in symbols]
    bidPrice1=[data[data['stock'] == stock].iloc[-1]['bidPrice1'] for stock in symbols]
    midquotePrice=[(askPrice1[i]+bidPrice1[i])/2 for i,stock in enumerate(symbols)]
    # long portfolid, 1st long->ask, 2nd short->bid
    short_price1=decide_short_price(symbols[1], bidPrice1[1], lastPrice[1])
    longPrice=[askPrice1[0],short_price1]
    # Short portfolid, 1st short->bid, 2nd long->ask
    short_price0 = decide_short_price(symbols[0], bidPrice1[0], lastPrice[0])
    shortPrice=[short_price0,askPrice1[1]]
    price=shortPrice
    return price

def get_symbols_price(symbols):
    database = 'market_research'
    table_name = 'quote'
    field = "stock,time,lastPrice,askPrice1,bidPrice1"
    data = fetchall_data(database, table_name, field)
    lastPrice = [data[data['stock'] == stock].iloc[-1]['lastPrice'] for stock in symbols]
    askPrice1 = [data[data['stock'] == stock].iloc[-1]['askPrice1'] for stock in symbols]
    bidPrice1 = [data[data['stock'] == stock].iloc[-1]['bidPrice1'] for stock in symbols]
    midquotePrice = [(askPrice1[i] + bidPrice1[i]) / 2 for i, stock in enumerate(symbols)]
    # long portfolid, 1st long->ask, 2nd short->bid
    short_price1 = decide_short_price(symbols[1], bidPrice1[1], lastPrice[1])
    longPrice = [askPrice1[0], short_price1]
    # Short portfolid, 1st short->bid, 2nd long->ask
    short_price0 = decide_short_price(symbols[0], bidPrice1[0], lastPrice[0])
    shortPrice = [short_price0, askPrice1[1]]
    df={}
    df['longPrice']=longPrice
    df['shortPrice']=shortPrice
    df['midPrice']=midquotePrice
    df['time']=data['time'].iloc[-1].strftime("%Y-%m-%d %H:%M:%S")
    return df

def decide_short_price(stock_code, bid_price, last_price):
    """
    1) 投资者通过其所有或控制的证券账户持有与其融券卖出标的相同证券的， 卖出该证券的价格应当满足不低于最新成交价的要求。
    2) 投资者融券卖出的申报价格不得低于该证券的最新成交价。
    """
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
    traded_price=get_recent_trade_price(xt_trader, acc, stock_code)
    status = xt_trader.unsubscribe(acc)
    xt_trader.stop()
    # if max(traded_price,last_price) >bid_price:
    #     return max(traded_price,last_price)
    # else:
    #     return bid_price
    price=max(traded_price,last_price,bid_price)
    return price

def get_current_time(duration=1):
    end_time = datetime.now()
    # end_time=datetime.combine(get_latest_trading_date(end_time),end_time.time())
    if end_time.time()>time(15, 30):
        print("It's not trading time.")
        end_time=datetime.combine(end_time.date(), time(15,00,00))
    elif end_time.time()<time(9, 30):
        print("It's not trading time.")
        end_time=datetime.combine(end_time.date()-timedelta(days=1), time(15,00,00))
    elif end_time.time()>time(11, 30) and end_time.time()<time(13, 30):
        print("It's not trading time.")
        end_time = datetime.combine(end_time.date(), time(11, 30, 00))
    start_time = end_time-timedelta(minutes=duration)
    start_time=start_time.strftime("%Y%m%d%H%M%S")
    end_time=end_time.strftime("%Y%m%d%H%M%S")
    return start_time,end_time


def enter_position(xt_trader,acc,symbols,price,qty,strategyFlag='s1'):
    if strategyFlag=="s1":
        directions=[xtconstant.CREDIT_FIN_BUY if copysign(1,x)>0 else xtconstant.CREDIT_SLO_SELL for x in qty] # 融资买入 / 融券卖出
    elif strategyFlag=="s2":
        directions=[xtconstant.CREDIT_BUY if copysign(1,x)>0 else xtconstant.CREDIT_SLO_SELL for x in qty] # 担保品买入 / 融券卖出

    order_id=[]
    for i, (direction,stock_code) in enumerate(zip(directions,symbols)):
        order_id.append(xt_trader.order_stock(acc, stock_code, direction, qty[i], xtconstant.FIX_PRICE,
                                                    price[i], strategyFlag, 'test order'))
    return order_id

def enter_position1(symbols,longShortFlag='long',strategyFlag='s1'):
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
    if longShortFlag=='long':
        hedge_ratio=[1, -1]
        price = get_long_price(symbols)
    else:
        hedge_ratio=[-1, 1]
        price = get_short_price(symbols)
    captital=1000
    qty = get_qty(hedge_ratio, price, captital)
    if strategyFlag=="s1":
        directions=[xtconstant.CREDIT_FIN_BUY if copysign(1,x)>0 else xtconstant.CREDIT_SLO_SELL for x in qty] # 融资买入 / 融券卖出
    elif strategyFlag=="s2":
        directions=[xtconstant.CREDIT_BUY if copysign(1,x)>0 else xtconstant.CREDIT_SLO_SELL for x in qty] # 担保品买入 / 融券卖出
    # print(directions)
    # print(strategyFlag)
    order_id=[]
    for i, (direction,stock_code) in enumerate(zip(directions,symbols)):
        order_id.append(xt_trader.order_stock(acc, stock_code, direction, abs(qty[i]), xtconstant.FIX_PRICE, \
                                                    price[i], strategyFlag, 'test order'))
    status = xt_trader.unsubscribe(acc)
    xt_trader.stop()
    return order_id

def enter_position2(stock_code,captital,longShortFlag='long',strategyFlag='s1'):
    import random
    import math
    from xtquant.xttype import StockAccount
    session_id = random.randint(0, 10000)
    xt_trader = MyXtQuantTrader(session_id)
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    acc = StockAccount('140080060269','CREDIT')
    xt_trader.start()
    connect_result = xt_trader.connect()
    status = xt_trader.subscribe(acc)
    # captital = 500
    if longShortFlag=='long':
        price = get_long_price1(stock_code)
        qty=captital/100/price
        qty=math.trunc(qty)*100
        if strategyFlag=="s1":
            direction=xtconstant.CREDIT_FIN_BUY  # 融资买入
        else:
            direction=xtconstant.CREDIT_BUY  # 担保品买入
    elif longShortFlag=='short':
        price = get_short_price1(stock_code)
        qty=captital/100/price*(-1)
        qty=math.trunc(qty)*100
        direction = xtconstant.CREDIT_SLO_SELL # 融券卖出

    order_id=xt_trader.order_stock(acc, stock_code, direction, abs(qty), xtconstant.FIX_PRICE, \
                                                price, strategyFlag, 'test order')
    status = xt_trader.unsubscribe(acc)
    xt_trader.stop()
    return order_id


def clear_position(xt_trader,acc,symbols,price,qty,strategyFlag='s1'):
    # if strategyFlag=="s1":
    directions=[xtconstant.CREDIT_BUY_SECU_REPAY if copysign(1,x)>0 else xtconstant.CREDIT_SELL_SECU_REPAY for x in qty] #   买券还券 / 卖券还款
    # elif strategyFlag=="s2":
    #     directions=[xtconstant.CREDIT_BUY_SECU_REPAY if copysign(1,x)>0 else xtconstant.CREDIT_SELL_SECU_REPAY for x in qty] #   买券还券 / 担保品卖出

    order_id=[]
    for i, (direction,stock_code) in enumerate(zip(directions,symbols)):
        order_id.append(xt_trader.order_stock(acc, stock_code, direction, qty[i], xtconstant.FIX_PRICE,
                                                    price[i], strategyFlag, 'test order'))
        # if strategyFlag=="s2" and direction==xtconstant.CREDIT_SELL:
        #     xt_trader.order_stock(acc, stock_code, xtconstant.CREDIT_DIRECT_CASH_REPAY, qty[i], xtconstant.FIX_PRICE,
        #                           price[i], 'strategy1', 'test order')
    return order_id
def clear_position1(symbols,strategyFlag='s1'):
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
    hedge_ratio=[-1, 1]
    captital=1000
    price = get_short_price(symbols)
    qty = get_qty(hedge_ratio, price, captital)
    if strategyFlag=="s1":
        directions=[xtconstant.CREDIT_BUY_SECU_REPAY if copysign(1,x)>0 else xtconstant.CREDIT_SELL_SECU_REPAY for x in qty] #   买券还券 / 卖券还款
    elif strategyFlag=="s2":
        directions=[xtconstant.CREDIT_BUY_SECU_REPAY if copysign(1,x)>0 else xtconstant.CREDIT_SELL_SECU_REPAY for x in qty] #   买券还券 / 担保品卖出

    order_id=[]
    for i, (direction,stock_code) in enumerate(zip(directions,symbols)):
        order_id.append(xt_trader.order_stock(acc, stock_code, direction, abs(qty[i]), xtconstant.FIX_PRICE,
                                                    price[i], strategyFlag, 'test order'))
    status = xt_trader.unsubscribe(acc)
    xt_trader.stop()
    return order_id

def get_compact_details(compacts):
    df = {}
    keys=['account_type','account_id','compact_type','cashgroup_prop','exchange_id','open_date','business_vol','real_compact_vol', \
          'ret_end_date','business_balance','businessFare','real_compact_balance','real_compact_fare','repaid_fare',\
          'repaid_balance','instrument_id','compact_id','position_str']
    for item in keys:
        df[item] = [getattr(o, item) for o in compacts]
    df = pd.DataFrame.from_dict(df)
    df['compact_type'] = [compact_status_num2str(x) for x in df.compact_type]
    names=['账号类型','资金账号','合约类型','头寸来源','证券市场','开仓日期','合约证券数量','未还合约数量','到期日','合约金额','合约息费','未还合约金额',\
           '未还合约息费','已还息费','已还金额','证券代码','合约编号','定位串']
    df.columns = names
    return df


def get_credit_account_details(credit_account):
    df = {}
    keys=['account_type','account_id','m_nStatus','m_nUpdateTime','m_nCalcConfig','m_dFrozenCash','m_dBalance','m_dAvailable', \
          'm_dPositionProfit','m_dMarketValue','m_dFetchBalance','m_dStockValue','m_dFundValue','m_dTotalDebt',\
          'm_dEnableBailBalance','m_dPerAssurescaleValue','m_dAssureAsset','m_dFinDebt','m_dFinDealAvl','m_dFinFee','m_dSloDebt',\
          'm_dSloMarketValue','m_dSloFee','m_dOtherFare','m_dFinMaxQuota','m_dFinEnableQuota','m_dFinUsedQuota','m_dSloMaxQuota',\
          'm_dSloEnableQuota','m_dSloUsedQuota','m_dSloSellBalance','m_dUsedSloSellBalance','m_dSurplusSloSellBalance']
    for item in keys:
        df[item] = [getattr(o, item) for o in credit_account]
    df = pd.DataFrame.from_dict(df)
    # df['compact_type'] = [compact_status_num2str(x) for x in df.compact_type]
    names=['账号类型','资金账号','账号状态','更新时间','计算参数','冻结金额','总资产','可用金额','持仓盈亏','总市值','可取金额','股票市值', \
           '基金市值', '总负债', '可用保证金', '维持担保比例', '净资产', '融资负债', '融资本金', '融资息费', '融券负债', '融券市值', '融券息费', '其它费用', \
           '融资授信额度', '融资可用额度', '融资冻结额度', '融券授信额度', '融券可用额度', '融券冻结额度', '融券卖出资金', '已用融券卖出资金', '剩余融券卖出资金']
    df.columns = names
    return df


def get_qty(hedge_ratio,price,captital):
    # hedge_ratio=[1, -1.1]
    # captital=10000
    # price=[4.2, 3.9]
    long,short=hedge_ratio
    long,short=[long/(abs(long)+abs(short)), short/(abs(long)+abs(short))]
    qty=[captital/100*long/price[0],captital/100*short/price[1]]
    import math
    qty=[math.trunc(x)*100 for x in qty]
    # positions_real=[ x*y for x, y in zip(price, qty)]
    return qty


def on_progress(data):
	print(data)


def timetag_to_datetimeS(list):
    times = []
    for item in list:
        times.append(timetag_to_datetime(int(item), "%Y%m%d%H%M%S"))   #  %H:%M:%S
    return times

def get_stock_price(fields,stock_list, start_time, end_time,period,dividend_type,count):
    # stock_list = get_stock_list_in_sector("两融标的")
    # stock_list = stock_list[0:10]
    df = get_market_data(field_list=fields,
                        stock_list=stock_list,
                        start_time=start_time,
                        end_time=end_time,
                        period=period,
                        dividend_type=dividend_type,
                        fill_data=True,
                        count=count)
    if period !='tick':
        df1 = {}
        for item in fields:
            if item != ('symbols' and 'time'):
                df1[item]=df[item].to_numpy()
        df1['symbols'] = stock_list
        df1['time'] = df['time'].columns.tolist()
        return df1
    else:
        df2={}
        symbols=[k for k in df.keys()]
        for stock_code in symbols:
            df1 = pd.DataFrame(df[stock_code])
            df1['stock'] = stock_code
            temp = []
            for k in range(len(df1)):
                temp.append(datetime.fromtimestamp(df1['time'].iloc[k] / 1000))
            df1['time'] = temp
            df1['time1'] = datetime.now()
            # print(df)
            for i, item in enumerate(['askPrice1', 'askPrice2', 'askPrice3', 'askPrice4', 'askPrice5']):
                temp=np.zeros((len(df1),1))
                for k in range(len(df1)):
                    temp[k]=df1['askPrice'].iloc[k][i]
                df1[item]=temp
            for i, item in enumerate(['bidPrice1', 'bidPrice2', 'bidPrice3', 'bidPrice4', 'bidPrice5']):
                temp = np.zeros((len(df1), 1))
                for k in range(len(df1)):
                    temp[k] = df1['bidPrice'].iloc[k][i]
                df1[item] = temp
            for i, item in enumerate(['askVol1', 'askVol2', 'askVol3', 'askVol4', 'askVol5']):
                temp = np.zeros((len(df1), 1))
                for k in range(len(df1)):
                    temp[k] = df1['askVol'].iloc[k][i]
                df1[item] = temp
            for i, item in enumerate(['bidVol1', 'bidVol2', 'bidVol3', 'bidVol4', 'bidVol5']):
                temp = np.zeros((len(df1), 1))
                for k in range(len(df1)):
                    temp[k] = df1['bidVol'].iloc[k][i]
                df1[item] = temp
            del df1["askPrice"]
            del df1["bidPrice"]
            del df1["askVol"]
            del df1["bidVol"]
            df2[stock_code]=df1
        return df2

def align_df(stock_list, df,fields):
    """df is dict lick dataframes"""
    df2=pd.DataFrame(df[stock_list[0]]) #.set_index('time')  #1684286103000-1684306803000
    df3=pd.DataFrame(df[stock_list[1]]) #.set_index('time') #1684286102000-1684306802000
    temp1=np.zeros((len(df2),1))
    temp2=np.zeros((len(df3),1))
    for i in range(len(df2)):
        temp1[i]=int(df2['time'].iloc[i].timestamp())*1000
    for i in range(len(df3)):
        temp2[i] = int(df3['time'].iloc[i].timestamp()) * 1000
    df2['time']=temp1
    df3['time']=temp2
    start=int(min(min(df2['time']),min(df3['time'])))
    end = int(max(max(df2['time']), max(df3['time'])))
    df0=pd.DataFrame(range(start,end,1000),columns=['time'])
    df2=df0.set_index('time').join(df2.set_index('time'))
    df3=df0.set_index('time').join(df3.set_index('time'))
    df2 = df2.ffill(axis=0)
    df3 = df3.ffill(axis=0)
    df1={}
    df1[stock_list[0]]=df2
    df1[stock_list[1]]=df3
    # df1['time'] = timetag_to_datetimeS(df4.index)
    return df1


def func2(stock_list, start_time, end_time,period):
    download_history_data2(stock_list,
                       start_time=start_time, end_time=end_time,
                       period=period,
                       callback=on_progress)
    return


def order_status_num2str(argument):
    match argument:

        case 48:
            return "ORDER_UNREPORTED"
        case 49:
            return "ORDER_WAIT_REPORTING"
        case 50:
            return "ORDER_REPORTED"
        case 51:
            return "ORDER_REPORTED_CANCEL"
        case 52:
            return "ORDER_PARTSUCC_CANCEL"
        case 53:
            return "ORDER_PART_CANCEL"
        case 54:
            return "ORDER_CANCELED"
        case 55:
            return "ORDER_PART_SUCC"
        case 56:
            return "ORDER_SUCCEEDED"
        case 57:
            return "ORDER_JUNK"
        case 255:
            return "ORDER_UNKNOWN"


def account_type_num2str(argument):
    match argument:
        case 1:
            return "FUTURE_ACCOUNT"
        case 2:
            return "SECURITY_ACCOUNT"
        case 3:
            return "CREDIT_ACCOUNT"
        case 7:
            return "HUGANGTONG_ACCOUNT"
        case 11:
            return "SHENGANGTONG_ACCOUNT"


def compact_status_num2str(argument):
    match argument:
        case 49:
            return "融券"
        case 48:
            return "融资"
        case 3:
            return "CREDIT_ACCOUNT"
        case 7:
            return "HUGANGTONG_ACCOUNT"
        case 11:
            return "SHENGANGTONG_ACCOUNT"


def account_status_num2str(argument):
    match argument:
        case -1:
            return "ACCOUNT_STATUS_INVALID"
        case 0:
            return "ACCOUNT_STATUS_OK"
        case 1:
            return "ACCOUNT_STATUS_WAITING_LOGIN"
        case 2:
            return "ACCOUNT_STATUSING"
        case 3:
            return "ACCOUNT_STATUS_FAIL"
        case 4:
            return "ACCOUNT_STATUS_INITING"
        case 5:
            return "ACCOUNT_STATUS_CORRECTING"
        case 6:
            return "ACCOUNT_STATUS_CLOSED"
        case 7:
            return "ACCOUNT_STATUS_ASSIS_FAIL"
        case 8:
            return "ACCOUNT_STATUS_DISABLEBYSYS"
        case 9:
            return "ACCOUNT_STATUS_DISABLEBYUSER"


def list2csv(list, name, keys):
    df = {}
    for item in keys:
        df[item] = [getattr(o, item) for o in list]
    #
    # df['account_type']=[o.account_type for o in datas]
    # df['account_id'] = [o.account_id for o in datas]
    # df['cashgroup_prop'] = [o.cashgroup_prop for o in datas]
    # df['exchange_id'] = [o.exchange_id for o in datas]
    # df['enable_amount'] = [o.enable_amount for o in datas]
    # df['instrument_id'] = [o.instrument_id for o in datas]
    df = pd.DataFrame.from_dict(df)
    df.to_csv(f'data/{name}.csv')
    return

def add_tick_data_db(symbols,count,start,end):
    # symbols = ['510350.SH', '510330.SH']
    # count=2
    # df = get_stock_price(['time', 'close'], symbols, '', '', '1m', 'none', count)
    # func2(symbols, '', '', 'tick')
    fields=['time','lastPrice','open', 'high', 'low', 'lastClose', 'volume', 'amount', 'pvolume',\
            'stockStatus', 'openInterest','openInt','lastSettlementPrice','askPrice','bidPrice','askVol','bidVol']
    for stock in symbols:
        df = get_market_data(field_list=fields,
                            stock_list=[stock],
                            start_time=start,
                            end_time=end,
                            period='tick',
                            dividend_type='none',
                            fill_data=True,
                            count=count)
        df1=pd.DataFrame(df[stock])
        df1['stock'] = stock
        df1['time1'] = datetime.now()
        # for item in df.keys():
        #     df1[item] = df[item].transpose(copy=True)
        temp = []
        for k in range(len(df1)):
            temp.append(datetime.fromtimestamp(df1['time'].iloc[k] / 1000))
        df1['time'] = temp
        for i, item in enumerate(['askPrice1', 'askPrice2', 'askPrice3', 'askPrice4', 'askPrice5']):
            temp = []
            for k in range(len(df1)):
                temp.append(df1['askPrice'].iloc[k][i])
            df1[item] = temp
        for i, item in enumerate(['bidPrice1', 'bidPrice2', 'bidPrice3', 'bidPrice4', 'bidPrice5']):
            temp = []
            for k in range(len(df1)):
                temp.append(df1['bidPrice'].iloc[k][i])
            df1[item] = temp
        for i, item in enumerate(['askVol1', 'askVol2', 'askVol3', 'askVol4', 'askVol5']):
            temp = []
            for k in range(len(df1)):
                temp.append(df1['askVol'].iloc[k][i])
            df1[item] = temp
        for i, item in enumerate(['bidVol1', 'bidVol2', 'bidVol3', 'bidVol4', 'bidVol5']):
            temp = []
            for k in range(len(df1)):
                temp.append(df1['bidVol'].iloc[k][i])
            df1[item] = temp
        del df1["askPrice"]
        del df1["bidPrice"]
        del df1["askVol"]
        del df1["bidVol"]

        database = 'market_research'
        table_name = 'quote'
        db_engine = mysql_dbconnection(database=database)
        try:
            # Save the data into the database
            df1.to_sql(table_name, db_engine, if_exists='append',index=False)
        except Exception as e:
            print(": SQL Exception :%s" % e)
        else:
            print(f": SQL:{stock}: successfully updated.")

def add_minute_data_db(symbols,count,start,end):
    # symbols = ['510350.SH', '510330.SH']
    # count=410
    # df = get_stock_price(['time', 'close'], symbols, '', '', '1m', 'none', count)
    # func2(symbols, '', '', '1m')
    fields=['time','open', 'high', 'low', 'close', 'volume', 'amount', 'settlementPrice', \
            'openInterest', 'dr','totaldr', 'preClose', 'suspendFlag']
    for stock in symbols:
        df = get_market_data(field_list=fields,
                            stock_list=[stock],
                            start_time=start,
                            end_time=end,
                            period='1m',
                            dividend_type='none',
                            fill_data=True,
                            count=count)

        df1=pd.DataFrame()
        for item in df.keys():
            df1[item] = df[item].transpose(copy=True)
        temp = []
        for k in range(len(df1)):
            temp.append(datetime.fromtimestamp(df1['time'].iloc[k] / 1000))
        df1['time'] = temp
        df1['time1']=datetime.now()
        df1['stock']=stock

        database = 'market_research'
        table_name = 'etf1m'
        db_engine = mysql_dbconnection(database=database)
        try:
            # Save the data into the database
            df1.to_sql(table_name, db_engine, if_exists='append',index=False)
        except Exception as e:
            print(": SQL Exception :%s" % e)
        else:
            print(f": SQL:{stock}: successfully updated.")