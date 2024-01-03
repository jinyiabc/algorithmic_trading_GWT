function data=get_sql_price_10minutes(symbols,date)
% symbols={'510350.SH','510330.SH'};
conn = database('china_stock','root','Hangzhou123');

%Set query to execute on the database
query1 = ['SELECT time, time1, lastPrice, stock, askPrice1, bidPrice1 ' ...
    'FROM market_research.quote ' ...
    'WHERE time <= "%s" ' ...
    'ORDER BY time ASC'];
query2 = ['SELECT DISTINCT time, stock, close ' ...
    'FROM market_research.etf1m ' ...
    'WHERE time <= "%s" ' ...    
    'ORDER BY time ASC'];
query1=sprintf(query1, date);
query2=sprintf(query2, date);
%% Set Database Import Options
opts1 = databaseImportOptions(conn,query1);
opts2 = databaseImportOptions(conn,query2);
%Update Variable Types
opts1 = setoptions(opts1,{'time'},'Type',{'datetime'});
opts2 = setoptions(opts2,{'time'},'Type',{'datetime'});
%% Execute query and fetch results
data_quote = fetch(conn,query1,opts1);
data_etf1m = fetch(conn,query2,opts2);
data_quote=data_quote(end-3600:end,:);
data_etf1m=data_etf1m(end-3600:end,:);
%% Close connection to database
close(conn)

%% Clear variables
clear conn query1 query2

%% Retime frequency.
lastPrice= unstack(data_quote, 'lastPrice', 'stock', 'VariableNamingRule','preserve');
askPrice1= unstack(data_quote, 'askPrice1', 'stock', 'VariableNamingRule','preserve');
bidPrice1= unstack(data_quote, 'bidPrice1', 'stock', 'VariableNamingRule','preserve');
close0= unstack(data_etf1m, 'close', 'stock', 'VariableNamingRule','preserve');
dt = minutes(10);
lastPrice=modifyFrequency(lastPrice, dt);
close0=modifyFrequency(close0, dt);
askPrice1=modifyFrequency(askPrice1, dt);
bidPrice1=modifyFrequency(bidPrice1, dt);
lastPrice=lastPrice(:,symbols);
close0=close0(:,symbols);
midPrice=(askPrice1{:,symbols}+bidPrice1{:,symbols})/2;
midPrice=array2timetable(midPrice,"RowTimes",bidPrice1.Time,"VariableNames",symbols);
longPrice=array2timetable([askPrice1{:,symbols{1}},bidPrice1{:,symbols{2}}],"RowTimes",bidPrice1.Time,"VariableNames",symbols); 
shortPrice=array2timetable([bidPrice1{:,symbols{1}},askPrice1{:,symbols{2}}],"RowTimes",bidPrice1.Time,"VariableNames",symbols); 
data.lastPrice=lastPrice;
data.longPrice=longPrice;
data.shortPrice=shortPrice;
data.close=close0;
data.midPrice=midPrice;
%% implement lastPrice/midPrice with close price.
idx1=all(isnan(table2array(data.lastPrice)),2);
% data.lastPrice(idx1,:)
idx1_time=data.lastPrice.Time(idx1);
data.lastPrice(idx1,:)=data.close(idx1_time,:);
data.midPrice(idx1,:)=data.close(idx1_time,:);
[row, col]=find(table2array(data.lastPrice)==0);
data.lastPrice(row,col)=data.midPrice(row,col);

end