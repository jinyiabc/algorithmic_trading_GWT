clear;
addpath(genpath('D:\work\books\Algorithmic_Trading_Chan\jplv7'))
addpath('D:\work\books\Algorithmic_Trading_Chan')
addpath('D:\qmt\matlab\utility')
addpath(genpath('D:\qmt\matlab\code'))
addpath(genpath('D:\qmt\matlab\indexArb'))

% etf=load('inputdata300M_ETF', 'matdata');
% stks=load("inputdata300M_Stocks.mat");
% stks = stks.matdata;
% etf = etf.matdata;
% 
% % Ensure data have same dates
% [tday idx1 idx2]=intersect(stks.time, etf.time);
% stks.cl=stks.close(idx1, :);
% stks.tday=tday;
% etf.cl=etf.close(idx2, :);
% etf.tday=tday;
% 
% % Convert minutes to hours data.
% TT1 = array2timetable(stks.cl,'RowTimes',stks.tday);
% dt = minutes(5);
% TT2 = retime(TT1,'regular','firstvalue','TimeStep',dt);
% stks.cl = table2array(TT2);stks.tday=TT2.Time;
% badData=all(isnan(stks.cl), 2);
% stks.cl(badData, :)=[];stks.tday(badData)=[];
% TT3 = array2timetable(etf.cl,'RowTimes',etf.tday);
% TT4 = retime(TT3,'regular','firstvalue','TimeStep',dt);
% etf.cl = table2array(TT4);etf.tday=TT4.Time;
% etf.cl(badData, :)=[];etf.tday(badData)=[];
% save test5m etf

% load('test5m','etf');
load('test10m','etf');
% load('test20m','etf');

dailyFreq=240/10;
z=[250 250 251];
[trainDataIdx,testDataIdx]=convertToRange(z);
ytrain=log(etf.cl(trainDataIdx,1:2));
results=johansen(ytrain, 0, 1);
eigVec=selectEvecFromJohansen(results);
% testDataIdx=251:500;
ytest=log(etf.cl(testDataIdx,1:2));
weights=repmat([eigVec(1)/eigVec(2),1], z(2),1); % Array of log market value of stocks and ETF's
logMktVal=smartsum(weights.*ytest,2);

labelN=1.0;bechmark=1.0;lookback=5;
numUnits = entryzscore(labelN, bechmark, logMktVal,lookback);
numUnits0 = entryzscore_cost(labelN, bechmark, logMktVal,lookback);

MA=movingAvg(logMktVal, lookback);
MSTD=movingStd(logMktVal, lookback);
zScore=(logMktVal-MA)./MSTD;

% convert longshort to longonly.
numUnits1=NaN(size(logMktVal,1),1);
idx1=numUnits==1;idx2=numUnits==-1;
numUnits1(idx1)=1;numUnits1(idx2)=0;numUnits1=fillMissingData(numUnits1);
% convert longshort to shortonly.
numUnits2=NaN(size(logMktVal,1),1);
idx1=numUnits==1;idx2=numUnits==-1;
numUnits2(idx1)=0;numUnits2(idx2)=-1;numUnits2=fillMissingData(numUnits2);
numUnits3=numUnits1+numUnits2;
% [numUnits0 numUnits3 zScore]


positions=repmat(numUnits0, [1 size(weights, 2)]).*weights; 
pnl=smartsum(lag(positions, 1).*(ytest-lag(ytest, 1)), 2); 

ret=pnl./smartsum(abs(lag(positions, 1)), 2); % return is P&L divided by gross market value of portfolio
ret(isnan(ret))=0;
sharpe_ratio = sqrt(252*dailyFreq)*mean(ret,'omitnan')/std(ret);
y = -sharpe_ratio;

figure(1);
plot(testDataIdx,cumprod(1+ret)-1);
hold on;


onewaytcost=0.00017;
pnlminustcost=pnl - smartsum(abs(positions-lag(positions,1)), 2).*onewaytcost;
retminustcost=pnlminustcost./smartsum(abs(lag(positions, 1)), 2);
% Zero divisor from previous position,
idxx=find(isinf(retminustcost));
for i=1:length(idxx)
    if smartsum(abs(positions(idxx(i)-1,:)), 2)==0  % previous day zero postion.
        retminustcost(idxx(i))=-onewaytcost;
    end
end
retminustcost(isnan(retminustcost))=0;
sharpeMinustCost=sqrt(252*dailyFreq)*mean(retminustcost,'omitnan')/smartstd(retminustcost, 1);
y1 = -sharpeMinustCost;
plot(testDataIdx,cumprod(1+retminustcost)-1);

fprintf(1, 'APR=%4.7f    Sharpe=%4.7f\n',prod(1+ret).^(252*dailyFreq/length(ret))-1, y);
fprintf(1, 'APR=%4.7f    Sharpe=%4.7f\n',prod(1+retminustcost).^(252*dailyFreq/length(retminustcost))-1, y1);

figure(2);
plot(testDataIdx,zScore,'g',testDataIdx,numUnits0,'b--o');
legend('numUnits1','numUnits2','numUnits3')

y3=zeros(1,20);ret3=zeros(20,250);apr=zeros(1,20);
for l=1:20
    benmark=1+0.1*(l-1);costFlag=true;
    [~, ~,ret3(l,:)] =indexArbitrageSharpe(labelN,benmark, etf.cl(:,1), etf.cl(:,2), [250,250,251], 1, costFlag);
    y3(l)=-sqrt(252*dailyFreq)*mean(ret3(l,:)','omitnan')/smartstd(ret3(l,:)', 1);
    apr(l)=prod(1+ret3(l,:)').^(252*dailyFreq/length(ret3(l,:)'))-1;
end
