function symbols = gwtDataMissing(matdata)
    
    symbols = matdata.symbols;
    fields = matdata.fields;
    idx=true(1,length(symbols));
    for item=1:length(fields)
        if isempty(matdata.(fields{item}))
            return 
        end
        if fields{item} ~= "time"
            for n =1:length(symbols)
                idx(n) = idx(n) & allnan(matdata.(fields{item})(:,n));
            end
        end
    end 
    symbols = symbols(idx);
    if isempty(symbols)
        warning("The data is complete.")
    else
        warning("Mising %s \n", symbols{:})
    end
    
end

% matdata.fields = {'close','open'}

function tf = allnan(X)
%ANYNAN True if at least one element of an array is Not-a-Number.
%   ANYNAN(X) returns true if at least one of the elements of X is NaN and
%   false otherwise.
%   For example, ANYNAN([pi NaN Inf -Inf]) is true.
%
%   See also ISNAN, ISMISSING, ANY, ANYMISSING.

%   Copyright 2021 The MathWorks, Inc.

tf = all(isnan(X), "all");
end