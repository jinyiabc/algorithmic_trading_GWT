function gwtDownload(stock_list, start_time, end_time, period)
    addpath(genpath('D:\qmt\matlab\code'))
    syspath = py.sys.path;
    syspath.append('D:\qmt');
    pylib = imp('helper.utility');
%     pylib = imp('myPreparedata');
    py_stock_list = py.list(stock_list);
    py2mat(pylib.func2(py_stock_list, start_time, end_time,period));
    return
end
