function order_id=gwtEnterPosition(symbols)
    syspath = py.sys.path;
    syspath.append('D:\qmt');
    pylib = imp('helper.utility');
    
    order_id=py2mat(pylib.enter_position1(symbols,strategyFlag='s1'));

end
