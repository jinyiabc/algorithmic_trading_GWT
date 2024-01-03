%% test
clearvars
stock_list = {'600519.SH', '601318.SH'}; %py.list({'600519.SH', '601318.SH'});
fields = {'time', 'low', 'close', 'open'}; % py.list({'time', 'low', 'close', 'open'});
period = '1d';
dividend_type = 'front';

% missing_symbols = {'600519.SH'};
% gwtDownload(missing_symbols, '20100217', '20100225','1d')
% % check for retrieved data.
% matdata = gwtGetData(fields, missing_symbols, '20100217', '20100225','1d',dividend_type);
% isempty(gwtDataMissing(matdata));

missing_symbols ={'600519.SH', '601318.SH'};
gwtDownload(missing_symbols, '20220217', '20220218','1m')
% check for retrieved data.
matdata = gwtGetData(fields, missing_symbols, '20220217', '20220218','1m',dividend_type);
gwtDataMissing(matdata);




