import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
import yfinance as yf


def plot_candlestick_with_zones(candlestick_data, zone_list):
    fig, ax = plt.subplots()

    # Convert 'date' column to datetime type
    candlestick_data['date'] = pd.to_datetime(candlestick_data.index)

    # Plot candlestick chart
    candlestick_ohlc(ax, zip(mdates.date2num(candlestick_data.index),
                             candlestick_data['Open'], candlestick_data['High'],
                             candlestick_data['Low'], candlestick_data['Close']),
                     width=0.6, colorup='g', colordown='r')

    for zone in zone_list:
        start_time = zone["start_time"]
        price_high = zone["price_high"]
        price_low = zone["price_low"]

        # Plot zone as a rectangle
        rect = patches.Rectangle((mdates.date2num(start_time), price_low),
                                 width=1, height=price_high - price_low,
                                 linewidth=1, edgecolor='blue', facecolor='blue', alpha=0.3)
        ax.add_patch(rect)

    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Candlestick Chart with Price Zones')
    plt.grid(True)
    plt.show()

# Example usage with a dataframe for candlestick data
# candlestick_data = pd.DataFrame({
#     'date': ['2024-01-24', '2024-01-25', '2024-01-26'],
#     'Open': [50, 60, 55],
#     'High': [60, 70, 65],
#     'low': [40, 50, 45],
#     'close': [55, 65, 60],
#     'volume': [100, 120, 80]
# })
candlestick_data=yf.download("MSFT",period="1d",interval="5m")
print(candlestick_data)
# Example usage with a list of dictionaries for zones
zones = [
    # {"start_time": pd.to_datetime("2024-01-24 08:00:00"), "price_high": 350, "price_low": 325},
    # {"start_time": pd.to_datetime("2024-01-23 12:00:00"), "price_high": 400, "price_low": 370},
    {"start_time": pd.to_datetime("2024-01-23 18:00:00"), "price_high": 390, "price_low": 388}
]

plot_candlestick_with_zones(candlestick_data, zones)
