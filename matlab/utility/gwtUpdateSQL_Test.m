%% Upload data to MYSQL.
% start_time=datestr(datetime('today'),'yyyymmdd');
symbols={'510300.SH','510330.SH'};
start_time='20230701';
end_time='20230731';
count=py.int(-1);
gwtUpdateSQL(symbols,start_time,end_time,count);
