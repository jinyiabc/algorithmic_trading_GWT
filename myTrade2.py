#coding=utf-8
from datetime import datetime, time, timedelta
import random
from math import copysign
from time import sleep
from IPython.display import display
import sys
import numpy as np
import pandas as pd
from xtquant.xtdata import subscribe_quote, get_market_data, unsubscribe_quote, timetag_to_datetime, get_trade_times, \
    get_full_tick, download_history_data, get_trading_calendar, get_l2_quote
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant

from helper.utility import timetag_to_datetimeS, get_stock_price, func2, order_status_num2str, account_type_num2str, \
    compact_status_num2str, account_status_num2str, list2csv
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

if __name__ == "__main__":
    print("demo test")
    # path为mini qmt客户端安装目录下userdata_mini路径
    # path = 'D:\\长城策略交易系统\\userdata_mini'
    # session_id为会话编号，策略使用方对于不同的Python策略需要使用不同的会话编号
    session_id = random.randint(0, 10000)
    xt_trader = MyXtQuantTrader(session_id)
    # 创建交易回调类对象，并声明接收回调
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    # 创建资金账号为1000000365的证券账号对象
    acc = StockAccount('140080060269','CREDIT')
    # acc = StockAccount('10000000325', 'STOCK')

    # 启动交易线程
    xt_trader.start()
    # 建立交易连接，返回0表示连接成功
    connect_result = xt_trader.connect()
    if connect_result != 0:
        import sys
        sys.exit('链接失败，程序即将退出 %d'%connect_result)
    # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
    status = xt_trader.subscribe(acc)
    print("=" * 40)
    print(f"账号订阅:{status}")

    # 订阅单股行情
    stock_code='000001.SZ'
    seq = subscribe_quote(stock_code, 'l2quote')
    if seq > 0:
        print(f"订阅{stock_code}成功。\n")
    else:
        print(f"订阅{stock_code}失败。seq:{seq}")
    data=get_l2_quote(field_list=[], stock_code=stock_code, start_time='', end_time='', count=-1)
    print(data)
    # 阻塞线程，接收交易推送
    xt_trader.run_forever()
