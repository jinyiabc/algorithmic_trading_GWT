function matdata = gwtGetData(fields,stock_list, start_time, end_time,period,dividend_type,count)
    addpath(genpath('D:\qmt\matlab\code'))
    syspath = py.sys.path;
    syspath.append('D:\qmt');
%     pylib = imp('myPreparedata');
    pylib = imp('helper.utility');
    py_stock_list = py.list(stock_list);
    py_fields = py.list(fields);
    matdata = py2mat(pylib.get_stock_price(py_fields,py_stock_list, start_time, end_time,period,dividend_type,count=py.int(count)));
    time = [matdata.time{:}];
    symbols = [matdata.symbols{:}];
    matdata.fields = fields;
    if isempty(time)
        warning("The data is not retrievable in GWT cache, Please download data first.")
        return
    end
    if strlength(time(1)) == 8
        time = datetime(time, InputFormat="yyyyMMdd");
    elseif strlength(time(1)) == 14
        time = datetime(time, InputFormat="yyyyMMddHHmmss");
    end
    matdata.symbols = symbols;
    matdata.time = time;
    
%     if length(time) == size(matdata.close,  2)
%         for t=1:length(fields)
%             matdata.(fields{t})=matdata.(fields{t})';
%         end
%     end

end
