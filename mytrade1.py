#coding=utf-8
import random
from xtquant.xtdata import subscribe_quote
from xtquant.xttype import StockAccount
from helper.utility import MyXtQuantTrader, MyXtQuantTraderCallback, on_data, get_account_status, on_data1, \
    get_trade_details, get_order_details, get_asset_details, get_position_details

if __name__ == "__main__":
    # Constant Parameter.
    session_id = random.randint(0, 10000)
    symbols = ['510300.SH', '510330.SH']

    xt_trader = MyXtQuantTrader(session_id)
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    acc = StockAccount('140080060269','CREDIT')
    xt_trader.start()
    connect_result = xt_trader.connect()
    if connect_result != 0:
        import sys
        sys.exit('链接失败，程序即将退出 %d'%connect_result)
    status = xt_trader.subscribe(acc)
    print("=" * 40)
    print(f"账号订阅:{status}")
    get_account_status(xt_trader, syncFlag=False)
    # 订阅单股行情
    for stock_code in symbols:
        seq1=subscribe_quote(stock_code, period='tick', start_time='', end_time='', count=-1, callback=on_data)
        seq2=subscribe_quote(stock_code, period='1m', start_time='', end_time='', count=-1, callback=on_data1)

        if seq1>0 and seq2>0:
            print(f"订阅{stock_code}成功。\n")
        else:
            print(f"订阅{stock_code}失败。seq:{seq1}{seq2}")

    """反订阅行情数据 """
    # unsubscribe_quote(seq)


    # 阻塞线程，接收交易推送
    xt_trader.run_forever()
