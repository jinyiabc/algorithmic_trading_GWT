function numUnits = entryzscore_cost(longShortFlag, bechmark, yport, lookback)
[sz1 sz2]=size(yport);
if sz1<sz2
    yport1=yport';
else
    yport1=yport;
end

entryZscore=bechmark;
exitZscore=-bechmark;

MA=movingAvg(yport1, lookback);
MSTD=movingStd(yport1, lookback);
zScore=(yport1-MA)./MSTD;

longsEntry=zScore < -entryZscore; % a long position means we should buy EWC
longsExit=zScore > -exitZscore;

shortsEntry=zScore > entryZscore;
shortsExit=zScore < exitZscore;

numUnitsLong=NaN(length(yport1), 1);
numUnitsShort=NaN(length(yport1), 1);

numUnitsLong(1)=0;
numUnitsLong(longsEntry)=1; 
numUnitsLong(longsExit)=0;
numUnitsLong=fillMissingData(numUnitsLong); % fillMissingData can be downloaded from epchan.com/book2. It simply carry forward an existing position from previous day if today's positio is an indeterminate NaN.

numUnitsShort(1)=0;
numUnitsShort(shortsEntry)=-1; 
numUnitsShort(shortsExit)=0;
numUnitsShort=fillMissingData(numUnitsShort);
if longShortFlag=='longShort'
    numUnits=numUnitsLong+numUnitsShort;
elseif longShortFlag=='long'
    numUnits=numUnitsLong;
else
    numUnits=numUnitsShort;
end
numUnits(end)=0; % clear the position.
end

