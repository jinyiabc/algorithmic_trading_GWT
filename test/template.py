#coding=utf-8
import numpy as np
import pandas as pd
from xtquant.xtdata import subscribe_quote, get_market_data, unsubscribe_quote
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant

from myPreparedata import func1, func3
from helper.utility import order_status_num2str, account_type_num2str, account_status_num2str, list2csv


class MyXtQuantTrader(XtQuantTrader):
    def __init__(self, path, session, callback=None):
        self.session = session
        super(MyXtQuantTrader, self).__init__(path, session, callback=None)

class MyXtQuantTraderCallback(XtQuantTraderCallback):
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
def on_data(datas):
    for stock_code in datas:
        	print(stock_code, datas[stock_code])

if __name__ == "__main__":
    print("demo test")
    # path为mini qmt客户端安装目录下userdata_mini路径
    path = 'D:\\gwt\\userdata_mini'
    # session_id为会话编号，策略使用方对于不同的Python策略需要使用不同的会话编号
    session_id = 123457
    xt_trader = MyXtQuantTrader(path, session_id)
    # 创建资金账号为1000000365的证券账号对象
    acc = StockAccount('140080060269','STOCK')
    # acc = StockAccount('10000000325', 'STOCK')
    # 创建交易回调类对象，并声明接收回调
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    # 启动交易线程
    xt_trader.start()
    # 建立交易连接，返回0表示连接成功
    connect_result = xt_trader.connect()
    if connect_result != 0:
        import sys
        sys.exit('链接失败，程序即将退出 %d'%connect_result)
    # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
    status = xt_trader.subscribe(acc)
    print(f"账号订阅:{status}")
    # 反订阅账号信息
    status = xt_trader.unsubscribe(acc)
    print(f"账号反订阅:{status}")
    # 同步查询账号状态
    accounts = xt_trader.query_account_status()
    for account in accounts:
        print(account.account_id, account_type_num2str(account.account_type), account_status_num2str(account.status))
    # 异步查询账号状态
    def callback(accounts):
        for account in accounts:
            print(account.account_id, account_type_num2str(account.account_type),
                  account_status_num2str(account.status))
    xt_trader.query_account_status_async(callback)

    # 订阅单股行情
    stock_code = '512800.SH'
    seq=subscribe_quote(stock_code, period='1m', start_time='', end_time='', count=0, callback=on_data)
    if seq>0:
        print(f"订阅{stock_code}成功。")
    else:
        print(f"订阅{stock_code}失败。seq:{seq}")
    # 反订阅行情数据
    unsubscribe_quote(seq)

    # 获取最新单股价格get_market_data
    df = func3(['time','close'],[stock_code], '', '','1m','none',10)
    print(df['close'][0][-1])
    latest_price=df['close'][0][-1]
    print(f"最新价格:{latest_price}")

    # # 使用指定价下单，接口返回订单编号，后续可以用于撤单操作以及查询委托状态
    # print("order using sync api:")
    # fix_result_order_id = xt_trader.order_stock(acc, stock_code, xtconstant.STOCK_BUY, 100, xtconstant.FIX_PRICE, buy_price, 'strategy1', 'test order')
    # print(fix_result_order_id)

    # # 使用异步下单接口，接口返回下单请求序号seq，seq可以和on_order_stock_async_response的委托反馈response对应起来
    # print("order using async api:")
    # async_seq = xt_trader.order_stock_async(acc, stock_code, xtconstant.CREDIT_SELL, 100, xtconstant.FIX_PRICE, latest_price,  'strategy1', 'test async order')
    # print(async_seq)


    # 根据订单编号查询委托
    print("query order:")
    orders  = xt_trader.query_stock_orders(acc,  cancelable_only = False)
    if orders :
        for order in orders:
            print(order.stock_code, order_status_num2str(order.order_status), order.order_sysid)
    # 查询当日所有的成交
    print("query trade:")
    trades = xt_trader.query_stock_trades(acc)
    if trades:
        for trade in trades:
            print(f"{trade.stock_code}, {trade.traded_volume}, {trade.traded_price}")
    # 查询证券资产
    print("query asset:")
    asset = xt_trader.query_stock_asset(acc)
    if asset:
        print(f"asset:{asset.cash}")
    # 查询当日所有的持仓
    print("query positions:")
    positions = xt_trader.query_stock_positions(acc)
    if len(positions) != 0:
        for position in positions:
            print(f"{position.account_id}, {position.stock_code}, {position.volume}")

    # 信用查询接口
    datas = xt_trader.query_credit_detail(acc)
    if datas:
        for credit_detail in datas:
            print(credit_detail.account_id, account_type_num2str(credit_detail.account_type),
                  credit_detail.m_nStatus)
    datas = xt_trader.query_stk_compacts(acc)
    datas = xt_trader.query_credit_subjects(acc)
    datas = xt_trader.query_credit_slo_code(acc)
    if datas:
        for credit_code in datas:
            print(credit_code)
    datas = xt_trader.query_credit_assure(acc)

    # 阻塞线程，接收交易推送
    # xt_trader.run_forever()
