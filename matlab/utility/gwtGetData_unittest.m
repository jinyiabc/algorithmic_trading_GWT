%% test
clearvars
stock_list = {'600519.SH', '601318.SH'}; %py.list({'600519.SH', '601318.SH'});
fields = {'time', 'low', 'close', 'open'}; % py.list({'time', 'low', 'close', 'open'});
field_tick={'time','lastPrice','open','high','low','lastClose','amount','volume','pvolume',...
                'stockStatus','openInt','lastSettlementPrice','askPrice','bidPrice','askVol','bidVol'};
period = 'tick';
dividend_type = 'front';
start_time = '20230317';
end_time = '20230318';
% daily 
matdata = gwtGetData(fields,stock_list, '20100217', '20100225','1d',dividend_type,250);
% 1m
symbols={'510350.SH','510330.SH'};
matdata1 = gwtGetData(field_tick,symbols, start_time, end_time, 'tick','none',250);


test = cell(1,2);
test{1} = 'test'
test{2} = 'test'

test = num2cell(stock_list)
test{1,1}


test1 = num2cell(['ab', 'bdde']);
 % {'a'}    {'b'}
test1={cat(1, test1{:})};

C{1} = rand(50, 17);
C{2} = rand(10, 17);
C{3} = rand(40, 17);
C{4} = rand(30, 17);
C{5} = rand(20, 17);
AllC = {cat(1, C{:})};