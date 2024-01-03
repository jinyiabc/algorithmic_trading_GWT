function orders=gwtOrders(symbols)
    syspath = py.sys.path;
    syspath.append('D:\qmt');
    pylib = imp('helper.utility');
    pylib1 = imp('xtquant.xttype');
    pylib2 = imp('xtquant.xtdata');
    % pylib3 = imp('myPreparedata');
    
    session_id = py.int(randi(10000));
    xtrade = pylib.MyXtQuantTrader(session=session_id);
    acc = pylib1.StockAccount('140080060269','CREDIT');
    callback = pylib.MyXtQuantTraderCallback();
    xtrade.register_callback(callback);
    xtrade.start();
    connect_result = xtrade.connect();
    if connect_result~=0
        warning("链接失败，程序即将退出 %d\n",connect_result)
    end
    status = xtrade.subscribe(acc);

    orders=xt_trader.query_stock_orders(acc);

    % fprintf(1,"账号订阅 %d \n",status);
    %     syncFlag=false;
    %     pylib.get_account_status(xtrade,syncFlag);

end