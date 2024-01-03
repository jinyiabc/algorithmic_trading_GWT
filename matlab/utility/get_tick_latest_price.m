function latest_price=get_tick_latest_price(symbols)
    syspath = py.sys.path;
    syspath.append('D:\qmt');
    pylib = imp('helper.utility');
    latest_price=py2mat(pylib.get_symbols_price(symbols));
    long_port = timetable(latest_price.longPrice{1},latest_price.longPrice{2},'RowTimes',datetime(latest_price.time), 'VariableNames',symbols);
    short_port = timetable(latest_price.shortPrice{1},latest_price.shortPrice{2},'RowTimes',datetime(latest_price.time), 'VariableNames',symbols);
    mid_port = timetable(latest_price.midPrice{1},latest_price.midPrice{2},'RowTimes',datetime(latest_price.time), 'VariableNames',symbols);
    latest_price.longPrice=long_port;
    latest_price.shortPrice=short_port;
    latest_price.midPrice=mid_port;
end