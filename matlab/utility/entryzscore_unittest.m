clear
yport = [
-83.2219854327952;
-83.3575250151873;
-83.1546338887586;
-83.3424472283969;
-83.7115566111236;
-83.4382082015220;
-83.6160740486976;
-83.9213621430629;
-83.9354778545088;
-84.1514183115253;
-84.2181421379810;
-83.9094008025519;
-83.8239158431132;
-83.9281791927029;
-83.8963861991882;
-84.1442267882075;
-83.9851863925871;
-84.1239676741578;   
];

%zScore
% NaN
% NaN
% NaN
% NaN
% -1.64527598347001
% -0.184466995890091
% -0.740641049365514
% -1.38222973327759
% -1.00234883751251
% -1.19726052426235
% -1.05661194590641
% 0.806021868512905
% 1.09040428694048
% 0.460824180577837
% 0.386453105035591
% -1.69015815340537
% -0.245761947164818
% -0.959178870928451

numUnits1 = entryzscore(1,1.6, yport, 5)
numUnits1 = entryzscore(2,1.6, yport, 5)
% ben=1	ben=1.11	zcore with ben=1
% 0	0	       NaN
% 0	0	       NaN
% 0	0	       NaN
% 0	0	       NaN
% 1	1	    -1.6453
% 1	1	    -0.1845
% 1	1	    -0.7406
% 1	1	    -1.3822
% 1	1	    -1.0023
% 1	1	    -1.1973
% 1	1	    -1.0566
% 0	0	    0.806
% -1	0	1.0904
% -1	0	0.4608
% -1	0	0.3865
% 1	1	    -1.6902
% 1	1	    -0.2458
% 1	1	    -0.9592


numUnits2 = entryzscore(2,1.6, yport, 5);

% 0
% 0
% 0
% 0
% 2
% 1
% 1
% 2
% 2
% 2
% 2
% -1
% -2
% -1
% -1
% 2
% 1
% 1
zScore = [
-1.64527598347001
-0.184466995890091
-0.740641049365514
-1.38222973327759
-1.00234883751251
-1.19726052426235
-1.05661194590641
0.806021868512905
1.09040428694048
0.460824180577837
0.386453105035591
-1.69015815340537
-0.245761947164818
 -0.019178870928451
 0.2
 0.3
 -0.1
 -0.2
 -0.49
 0.49
];
numUnits3 = entryzscoreS(2, zScore, 5);

% 0
% 1
% 1
% 2
% 2
% 2
% 2
% -1
% -2
% -1
% -1
% 2
% 1
% 1
% 0
% 0
% 0
% 0
% 0
% 0

% 04/02 Add line 32 to remove leverage effect. 
numUnits3 = entryzscoreS(2, zScore, 5);

%          0
%     0.5000
%     0.5000
%     1.0000
%     1.0000
%     1.0000
%     1.0000
%    -0.5000
%    -1.0000
%    -0.5000
%    -0.5000
%     1.0000
%     0.5000
%     0.5000
%          0
%          0
%          0
%          0
%          0
%          0