function numUnits = entryzscore(labelN, bechmark, yport, lookback)
[sz1 sz2]=size(yport);
if sz1<sz2
    yport1=yport';
else
    yport1=yport;
end
% 04/02 Add line 32 to remove leverage effect. 
% entryZscore=1./labelN;
% MA=movingAvg(yport, lookback);
MA=movmean(yport1,[lookback-1,0]);
MA(1:lookback-1)=NaN;
% MSTD=movingStd(yport, lookback);
MSTD=movstd(yport1,[lookback-1,0]);
MSTD(1:lookback-1)=NaN;
zScore=(yport1-MA)./MSTD*(labelN*1.0/bechmark);
numUnits=NaN(size(yport1,1),1);
numUnits = complex(numUnits, zeros(size(numUnits), class(numUnits)) ); % For code gen.

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
    % Fill for NaN w
    % ith previous value.
    numUnits=fillMissingData(numUnits);
end
numUnits=numUnits/labelN;
end

% for t=2:length(yport)
%     if isnan(zScore(t))
%         continue
%     end
%     if t==2
%         numUnits(t)=fix(zScore(t));
%         continue
%     end
%     if sign(zScore(t))==1
%         if abs(zScore(t)) < 1 && abs(zScore(t-1))<1 && sign(zScore(t)*zScore(t-1))>0
%             numUnits(t)=NaN;
%         elseif abs(zScore(t)) < 1 && abs(zScore(t-1))>=1 && sign(zScore(t)*zScore(t-1))>0
%             numUnits(t)=-1;
%         else
%             numUnits(t)=-floor(zScore(t)) ; % a long position means we should buy EWC
%         end
%         if numUnits(t)<-labelN
%             numUnits(t)=-labelN;
%         end
%     else
%         if abs(zScore(t)) < 1 && abs(zScore(t-1))<1 && sign(zScore(t)*zScore(t-1))>0
%             numUnits(t)=NaN;
%         elseif abs(zScore(t)) < 1 && abs(zScore(t-1))>=1 && sign(zScore(t)*zScore(t-1))>0
%             numUnits(t)=1;        
%         else
%             numUnits(t)=-ceil(zScore(t)) ; 
%         end
%         if numUnits(t)>labelN
%             numUnits(t)=labelN;
%         end
%     end
% 
%     numUnits=fillMissingData(numUnits);
% %     if abs(zScore(t)) < 1 && abs(zScore(t-1))>=1 && sign(zScore(t)*zScore(t-1))>0
% %         numUnits(t)=1;
% %     end
% %     if abs(zScore(t)) < 1 && abs(zScore(t-1))>=1 && sign(zScore(t)*zScore(t-1))>0
% %         numUnits(t)=1;
% %     end
% end
