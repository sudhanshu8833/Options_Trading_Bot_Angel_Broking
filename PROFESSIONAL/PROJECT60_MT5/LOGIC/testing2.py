import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

def plot_candlestick_with_zones(candlestick_data, zone_list):
    root = tk.Tk()
    root.title('Candlestick Chart with Price Zones')

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

    # Enable navigation toolbar for zooming
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def on_key(event):
        xlim = ax.get_xlim()
        x_range = xlim[1] - xlim[0]

        if event.keysym == 'Up':
            ax.set_xlim(xlim[0] + 0.1 * x_range, xlim[1] - 0.1 * x_range)
        elif event.keysym == 'Down':
            ax.set_xlim(xlim[0] - 0.1 * x_range, xlim[1] + 0.1 * x_range)
        canvas.draw()

    def on_button_press(event):
        if event.button == 1:  # Left mouse button
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            ax._xypress = [(event.x, event.y, xlim, ylim)]

    def on_mouse_move(event):
        if hasattr(ax, '_xypress') and event.xdata is not None:
            lastx, lasty, last_xlim, last_ylim = ax._xypress[0]
            x_range = last_xlim[1] - last_xlim[0]
            
            new_xlim = (last_xlim[0] - (event.x - lastx) / lastx * x_range,
                        last_xlim[1] - (event.x - lastx) / lastx * x_range)
            
            ax.set_xlim(new_xlim)
            canvas.draw()

    def on_button_release(event):
        if event.button == 1 and hasattr(ax, '_xypress'):
            del ax._xypress

    root.bind("<Key>", on_key)
    canvas.mpl_connect('button_press_event', on_button_press)
    canvas.mpl_connect('motion_notify_event', on_mouse_move)
    canvas.mpl_connect('button_release_event', on_button_release)
    root.mainloop()


# Example usage with a dataframe for candlestick data
candlestick_data = yf.download("MSFT", period="5d", interval="5m")
candlestick_data['Date'] = candlestick_data.index

# Example usage with a list of dictionaries for zones
zones = [
    {"start_time": mdates.date2num(pd.to_datetime("2024-01-24 09:00:00")), "price_high": 60, "price_low": 40},
    {"start_time": mdates.date2num(pd.to_datetime("2024-01-23 12:05:00")), "price_high": 80, "price_low": 50},
    {"start_time": mdates.date2num(pd.to_datetime("2024-01-23 15:10:00")), "price_high": 396, "price_low": 395}
]

plot_candlestick_with_zones(candlestick_data, zones)
