function position=check_longShort(symbols,lastPrice, midPrice,time)
    hhmm=time.Hour*100 + time.Minute;
    if hhmm==930
        index=find(lastPrice.Time==time-hours(18.5));
    else
        index=find(lastPrice.Time==time-minutes(10));
    end
    if isempty(index)
        fprintf(1, '%s :It is empty.\n',time);
        return
    end
    lookback=5;benchmark=1.0;longShortFlag="longShort";
    eigVec=[1, -1];
    hedge_ratio=repmat([1, eigVec(2)/eigVec(1)],[5,1]); 
    ynew=[lastPrice(index-3:index,symbols);midPrice];
    ynew=ynew{:,:};
%     ynew(4,:)=[3.855,3.859];
    logMktVal=smartsum(log(ynew).*hedge_ratio,2);
    numUnits = entryzscore_cost1(longShortFlag, benchmark, logMktVal,lookback);
    lastNumUnit=numUnits(end);
    if lastNumUnit==1
        fprintf(1, '%s :Long the Portfolio.\n',time);
    elseif lastNumUnit == -1
        fprintf(1, '%s :Short the Portfolio.\n',time);
    else
        fprintf(1, '%s :Clear the position.\n',time);
        lastNumUnit=0;
    end
    position=lastNumUnit;

end