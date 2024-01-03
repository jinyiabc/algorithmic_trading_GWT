from xtquant.xtdata import get_etf_info, get_instrument_type, get_stock_list_in_sector, download_sector_data, \
    get_index_weight, get_sector_list

download_sector_data()
stock_list = get_stock_list_in_sector("ETF跨境型")
tmp = get_index_weight("513500.SH")
# get_instrument_type("512700.SH")
sectors = get_sector_list()

print("completed.")