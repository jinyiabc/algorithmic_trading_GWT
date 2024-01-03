function numUnits = entryzscoreS(labelN, zScore, lookback)
entryZscore=1/labelN;
zScore=zScore*(1/entryZscore);

numUnits=NaN(size(zScore,1),1);
numUnits(1)=0;
for t=2:length(zScore)
    if isnan(zScore(t))
        continue
    end
    % if same sign within range (-1 1), get from previous value.
    if abs(zScore(t)) < 1 && abs(zScore(t-1))<1 && sign(zScore(t)*zScore(t-1))>0
        numUnits(t)=NaN;
    % if Penetrate +-1 without zero, get one with opposite direction.
    elseif abs(zScore(t)) < 1 && abs(zScore(t-1))>=1 && sign(zScore(t)*zScore(t-1))>0
        numUnits(t)=-sign(zScore(t));
    % if >1 or <-1, get integer near to zero. 
    else
        numUnits(t)=-fix(zScore(t)) ; % a long position means we should buy EWC
    end
    % truncate for <-labelN and >labelN.
    if numUnits(t)<-labelN || numUnits(t)>labelN
        numUnits(t)=-labelN*sign(zScore(t));
    end
    % Fill for NaN with previous value.
    numUnits=fillMissingData(numUnits);
end
numUnits=numUnits/labelN;
end