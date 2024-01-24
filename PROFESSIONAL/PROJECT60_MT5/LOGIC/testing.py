import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
import yfinance as yf

def plot_candlestick_with_zones(candlestick_data, zone_list):
    fig, ax = plt.subplots()

    # Convert 'Date' column to datetime type
    candlestick_data['Date'] = pd.to_datetime(candlestick_data['Date'])
    
    # Resample to 5-minute intervals
    candlestick_data = candlestick_data.set_index('Date').resample('5T').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }).dropna().reset_index()

    candlestick_data['Date'] = candlestick_data['Date'].apply(mdates.date2num)

    # Plot candlestick chart
    candlestick_ohlc(ax, zip(candlestick_data['Date'],
                             candlestick_data['Open'], candlestick_data['High'],
                             candlestick_data['Low'], candlestick_data['Close']),
                     width=0.004, colorup='g', colordown='r')

    for zone in zone_list:
        start_time = zone["start_time"]
        price_high = zone["price_high"]
        price_low = zone["price_low"]

        # Plot zone as a rectangle
        rect = patches.Rectangle((start_time, price_low),
                                 width=candlestick_data['Date'].iloc[-1] - start_time, height=price_high - price_low,
                                 linewidth=1, edgecolor='blue', facecolor='blue', alpha=0.3)
        ax.add_patch(rect)

    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('5-Minute Candlestick Chart with Price Zones')
    plt.grid(True)
    plt.show()

# Example usage with a dataframe for candlestick data
candlestick_data=yf.download("MSFT",period="5d",interval="5m")
print(candlestick_data)
candlestick_data['Date']=candlestick_data.index
# Example usage with a list of dictionaries for zones
zones = [
    {"start_time": mdates.date2num(pd.to_datetime("2024-01-24 09:00:00")), "price_high": 60, "price_low": 40},
    {"start_time": mdates.date2num(pd.to_datetime("2024-01-23 12:05:00")), "price_high": 80, "price_low": 50},
    {"start_time": mdates.date2num(pd.to_datetime("2024-01-23 15:10:00")), "price_high": 396, "price_low": 395}
]

plot_candlestick_with_zones(candlestick_data, zones)
