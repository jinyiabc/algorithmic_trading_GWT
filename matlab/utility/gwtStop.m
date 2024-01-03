function gwtStop(xtrade, acc, seq)
    syspath = py.sys.path;
    syspath.append('D:\qmt');
    pylib = imp('helper.utility');
    pylib1 = imp('xtquant.xttype');
    pylib2 = imp('xtquant.xtdata');
    % pylib3 = imp('myPreparedata');

%     xt_trader.unsubscribe(acc);
    for k=1:2
        pylib2.unsubscribe_quote(py.int(seq(k)));
    end
    xtrade.stop()

end