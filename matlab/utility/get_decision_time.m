function time=get_decision_time(now,options)
    arguments
        now (1,1) {mustBeNonempty}
        options.fixTimeFlag (1,1) {mustBeNumericOrLogical} = true 
    end
    if options.fixTimeFlag
        tday = dateshift(datetime('today'),'start','day');
        T0=tday+duration('09:30:00');
        T1=tday+duration('14:50:00');
        T2=tday+duration('15:00:00');
        if abs(now-T0)<minutes(5)
            time=T0;
        elseif abs(now-T1)<minutes(5)
            time=T1;
        elseif abs(now-T2)<minutes(5)
            time=T2;
        else
            fprintf(1, '%s :It is not trading time or decesion time.\n',now);
            time=NaT;
            return
        end
        fprintf(1, 'decision time: %s now: %s.\n',time,now);
    else
        time0=now-minutes(mod(now.Minute,10))-seconds(now.Second);
        time1=now-minutes(mod(now.Minute,10))-seconds(now.Second)+minutes(10);
        if abs(time1-now)<minutes(5)
            time=time1;
        elseif abs(time0-now)<minutes(5)
            time=time0;
        end
        fprintf(1, 'decision time: %s now: %s.\n',time,now);
    end

end