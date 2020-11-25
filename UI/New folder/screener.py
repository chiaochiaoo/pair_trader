from finviz.screener import Screener

filters = ['exch_amex','sh_relvol_o0.5']  # Shows companies in NASDAQ which are in the S&P500
signal = 'ta_mostactive'
stock_list = Screener(filters=filters, table='Performance', signal=signal,order='-relativevolume')  # Get the performance table and sort it by price ascending
print(stock_list)
# Export the screener results to .csv
stock_list.to_csv("AMEX_stock.csv")


filters = ['exch_nasd','sh_relvol_o5']  # Shows companies in NASDAQ which are in the S&P500
signal = 'ta_mostactive'
stock_list = Screener(filters=filters, table='Performance', signal=signal,order='-relativevolume')  # Get the performance table and sort it by price ascending
print(stock_list)
# Export the screener results to .csv
stock_list.to_csv("NASDAQ_stock.csv")

filters = ['exch_nyse','sh_relvol_o2']  # Shows companies in NASDAQ which are in the S&P500
signal = 'ta_mostactive'
stock_list = Screener(filters=filters, table='Performance', signal=signal,order='-relativevolume')  # Get the performance table and sort it by price ascending
print(stock_list)
# Export the screener results to .csv
stock_list.to_csv("NYSE_stock.csv")

# Create a SQLite database
# stock_list.to_sqlite("stock.sqlite3")

# for stock in stock_list[9:19]:  # Loop through 10th - 20th stocks
#     print(stock['Ticker'], stock['Price']) # Print symbol and price

# # Add more filters
# stock_list.add(filters=['fa_div_high'])  # Show stocks with high dividend yield
# or just stock_list(filters=['fa_div_high'])

# Print the table into the console
