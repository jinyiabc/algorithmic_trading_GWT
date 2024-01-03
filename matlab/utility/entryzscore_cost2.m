function zScore = entryzscore_cost2(longShortFlag, bechmark, yport, lookback)
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

end

