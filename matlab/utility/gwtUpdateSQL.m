function gwtUpdateSQL(symbols,start_time,end_time,count)
%     start_time=date;
%     end_time=date;
    syspath = py.sys.path;
    syspath.append('D:\qmt');
    pylib = imp('helper.utility');
    gwtDownload(symbols, start_time, end_time, 'tick');
    pylib.add_tick_data_db(symbols,count,start_time,end_time);
    gwtDownload(symbols, start_time, end_time, '1m');
    pylib.add_minute_data_db(symbols,count,start_time,end_time);
end
