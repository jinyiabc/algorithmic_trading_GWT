function TT1=modifyFrequency(data, dt)
    TT=table2timetable(data,'RowTimes',data.time);
    TT1 = retime(TT,'regular','nearest','TimeStep',dt);
    hhmm=TT1.Time.Hour*100+TT1.Time.Minute;
    idx=(hhmm>=930 & hhmm<=1130) | (hhmm>=1300 & hhmm<=1500);
    TT1=TT1(idx,:);
end