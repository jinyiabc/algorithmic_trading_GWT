from datetime import datetime

from helper.utility import add_tick_data_db, add_minute_data_db, func2, get_current_time

if __name__ == "__main__":
    symbols = ['510350.SH', '510330.SH']
    count = 400
    tday = datetime.today().strftime("%Y%m%d")   #'20230520'
    start='20230517'
    end='20230517'
    func2(symbols, start, end, 'tick')
    add_tick_data_db(count,start,end)
    func2(symbols, start, end, '1m')
    add_minute_data_db(count, start, end)
