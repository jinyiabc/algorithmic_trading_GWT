%% test
clearvars
stock_list = {'600519.SH', '601318.SH'}; %py.list({'600519.SH', '601318.SH'});
fields = {'time', 'low', 'close', 'open'}; % py.list({'time', 'low', 'close', 'open'});
period = '1d';
dividend_type = 'front';

% daily 
% matdata = gwtGetData(fields,stock_list, '20100217', '20100225','1d',dividend_type);
% 1m
matdata1 = gwtGetData(fields,stock_list, '20100217', '20100225', '1m',dividend_type);

% symbols = gwtDataMissing(matdata);
% disp(symbols);   % 600519.SH

symbols = gwtDataMissing(matdata1);
disp(symbols);
