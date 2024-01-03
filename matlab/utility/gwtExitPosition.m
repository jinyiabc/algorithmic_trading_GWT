function order_id=gwtExitPosition(symbols)
    syspath = py.sys.path;
    syspath.append('D:\qmt');
    pylib = imp('helper.utility');
    
    order_id=py2mat(pylib.clear_position1(symbols,strategyFlag='s1'));

end