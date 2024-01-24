import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json

import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import logging
logging.getLogger("pymongo").setLevel(logging.WARNING)

data = {}
with open("data.json", "r") as json_file:
    data = json.load(json_file)
database = data['database']
uri = data['mongo_uri']

client = MongoClient(uri, tlsCAFile=data['ca'], connect=False)
bot = client[database]
admin = bot['Admin']


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("ARBITRAGE BOT")
        self.root.state("zoomed")

        # self.admin = admin.find_one()
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)

        self.tab1.columnconfigure(0, weight=1)
        self.tab1.columnconfigure(1, weight=1)
        self.tab1.columnconfigure(2, weight=1)
        # self.tab1.columnconfigure(3, weight=1)

        self.notebook.add(self.tab1, text="Input Data")
        self.notebook.add(self.tab2, text="Present positions")
        self.notebook.add(self.tab3, text="Market Snapshot")

        # T1=threading.Thread(target=self.tab1_fun)
        # T2=threading.Thread(target=self.tab2_fun)
        # T3=threading.Thread(target=self.tab3_fun)
        # T1.start()
        # T2.start()
        # T3.start()

        self.tab1_fun()
        # self.tab2_fun()
        # self.tab3_fun()

        # self.root.after(0, self.update_page)

    def update_page(self):
        # print(self.present_position)

        T1 = threading.Thread(target=self.populate_snapshot)
        T2 = threading.Thread(target=self.populate_treeview)

        T1.start()
        T2.start()
        self.root.after(1000, self.update_page)

    def populate_treeview(self):
        # Query the database to fetch data from the Position table
        positions = list(trades.find().sort("time", -1).limit(50))

        # positions.reverse()
        # print(len(positions))
        # Update the existing list with the new positions
        existing_items = self.present_position.get_children()
        for i, position in enumerate(positions):
            if 'Live' not in position:
                position['Live'] = False
            values = (position['time'], position['base'], position['script1'], position['script_price1'], position['script2'], position['script_price2'], position['script3'], position['script_price3'],
                      position['initial base account'], position['final base quantity'], position['profits'], position['Live'])

            if i < len(existing_items):
                # Update existing item
                # self.present_position.item(existing_items[i], values=values, tags=("even_row" if i % 2 == 0 else "odd_row"))
                self.present_position.item(existing_items[i], values=values)
            else:
                # Insert new item at the end of the list
                # self.present_position.insert("", "end", values=values, tags=("even_row" if i % 2 == 0 else "odd_row"))
                self.present_position.insert("", "end", values=values)

    def tab2_fun(self):
        self.present_position = ttk.Treeview(self.tab2, columns=("Time", "Base", "script1", "script_price1", "script2",
                                             "script_price2", "script3", "script_price3", "initial quantity", "final quantity", "profits", "Live"), show="headings")
        self.present_position.tag_configure("even_row", background="black")
        self.present_position.tag_configure("odd_row", background="green")

        # self.present_position.heading("Time",text="Time")
        # self.present_position.heading("Base",text="Base")
        self.present_position.heading("script1", text="script1")
        self.present_position.heading("script_price1", text="script_price1")
        self.present_position.heading("script2", text="script2")
        self.present_position.heading("script_price2", text="script_price2")
        self.present_position.heading("script3", text="script3")
        self.present_position.heading("script_price3", text="script_price3")
        self.present_position.heading(
            "initial quantity", text="initial quantity")
        self.present_position.heading("final quantity", text="final quantity")
        self.present_position.heading("profits", text="profits")
        self.present_position.heading("Live", text="Live")
        self.present_position.pack(fill="both", expand=True)
        T1 = threading.Thread(target=self.populate_treeview)
        T1.start()

    def populate_snapshot(self):
        positions = list(screenshot.find({}))
        # positions.reverse()

        # Get the existing items in the Treeview
        existing_items = self.snapshot.get_children()

        # Iterate through the results and either update existing items or insert new ones

        for i, position in enumerate(positions):

            values = (position['time'], position['base'], position['script1'], position['script_price1'], position['script2'], position['script_price2'], position['script3'], position['script_price3'],
                      position['initial base quantity'], position['final base quantity'], position['profit'])

            if i < len(existing_items):
                # Update existing item
                # self.snapshot.item(existing_items[i], values=values, tags=("even_row" if i % 2 == 0 else "odd_row"))
                self.snapshot.item(existing_items[i], values=values)

            else:
                # Insert new item at the end of the list
                # self.snapshot.insert("", "end", values=values, tags=("even_row" if i % 2 == 0 else "odd_row"))
                self.snapshot.insert("", "end", values=values)

        # for j in range(len(positions),len(existing_items)):
        #     # Check if the list is not empty before attempting to delete

        #     self.snapshot.delete(existing_items[j])   # Delete the last item

    def tab3_fun(self):
        self.snapshot = ttk.Treeview(self.tab3, columns=("Time", "Base", "script1", "script_price1", "script2",
                                     "script_price2", "script3", "script_price3", "initial quantity", "final quantity", "profits"), show="headings")
        # self.snapshot.tag_configure("even_row", background="black")
        # self.snapshot.tag_configure("odd_row", background="green")

        self.snapshot.heading("Time", text="Time")
        self.snapshot.heading("Base", text="Base")
        self.snapshot.heading("script1", text="script1")
        self.snapshot.heading("script_price1", text="script_price1")
        self.snapshot.heading("script2", text="script2")
        self.snapshot.heading("script_price2", text="script_price2")
        self.snapshot.heading("script3", text="script3")
        self.snapshot.heading("script_price3", text="script_price3")
        self.snapshot.heading("initial quantity", text="initial quantity")
        self.snapshot.heading("final quantity", text="final quantity")
        self.snapshot.heading("profits", text="profits")
        self.snapshot.pack(fill="both", expand=True)
        T1 = threading.Thread(target=self.populate_snapshot)
        T1.start()

    def tab1_fun(self):

        self.admin = admin.find_one()

        self.label_EXCHANGE = tk.Label(self.tab1, text="EXCHANGE")
        self.entry_EXCHANGE = tk.Entry(self.tab1)
        self.entry_EXCHANGE.insert(0, self.admin['exchange'])
        self.label_EXCHANGE.grid(column=1, row=0, padx=5, pady=5, sticky='W')
        self.entry_EXCHANGE.grid(column=1, row=0, padx=5, pady=5, sticky='E')

        self.label_BASE = tk.Label(self.tab1, text="BASE")
        self.entry_BASE = tk.Entry(self.tab1)
        self.entry_BASE.insert(0, self.admin['tradable_base_coins'])
        self.label_BASE.grid(column=1, row=1, padx=5, pady=5, sticky='W')
        self.entry_BASE.grid(column=1, row=1, padx=5, pady=5, sticky='E')

        self.invest_by_per = tk.BooleanVar(value=self.admin['invest_by_per'])
        self.label_INVESTMENT = tk.Label(
            self.tab1, text="INVESTMENT % OF PORTFOLIO")
        self.entry_INVESTMENT = tk.Entry(self.tab1)
        self.entry_INVESTMENT.insert(0, self.admin['investment'])
        self.check_button2 = tk.Checkbutton(
            self.tab1, variable=self.invest_by_per)
        self.label_INVESTMENT.grid(column=1, row=2, padx=5, pady=5, sticky='W')
        self.entry_INVESTMENT.grid(column=1, row=2, padx=5, pady=5, sticky='E')
        self.check_button2.grid(column=2, row=2, padx=5, pady=5, sticky='W')

        self.label_min_profit = tk.Label(self.tab1, text="MINIMUM PROFIT")
        self.entry_min_profit = tk.Entry(self.tab1)
        self.entry_min_profit.insert(0, self.admin['minimum_profit'])
        self.label_min_profit.grid(column=1, row=3, padx=5, pady=5, sticky='W')
        self.entry_min_profit.grid(column=1, row=3, padx=5, pady=5, sticky='E')

        self.paper = tk.Label(self.tab1, text="PAPER TRADING")
        self.paper_trading_var = tk.BooleanVar(
            value=self.admin['paper_trading'])
        self.check_button1 = tk.Checkbutton(
            self.tab1, variable=self.paper_trading_var)
        self.paper.grid(column=1, row=4, padx=5, pady=5, sticky='w')
        self.check_button1.grid(column=2, row=4, pady=5, sticky='w')

        self.submit = tk.Button(self.tab1, text="Submit",
                                command=self.get_form_data)
        self.submit.grid(column=1, row=5, padx=5, pady=40, sticky='N')

        self.start = tk.Button(
            self.tab1, text="Start/Stop Strategy", command=self.start_strategy)
        self.dot = tk.Label(self.tab1, text="●", font=("Helvetica", 36))
        self.start.grid(column=1, row=6, padx=5, pady=20, sticky='N')
        self.dot.grid(column=1, row=7, padx=5, pady=20, sticky='N')

    def update(self, thread):
        self.admin = admin.find_one()
        self.admin['thread'] = thread
        admin.update_one({}, {'$set': self.admin})

    def start_strategy(self):
        global is_running, my_thread

        if not is_running:
            is_running = True
            self.update(True)
            self.dot.config(foreground="light green")
            my_thread = threading.Thread(target=run)
            my_thread.start()

        else:
            is_running = False
            self.update(False)
            self.dot.config(foreground="white")

    def get_form_data(self):

        exchange = self.entry_EXCHANGE.get()
        base = self.entry_BASE.get()
        investment = self.entry_INVESTMENT.get()
        min_profit = self.entry_min_profit.get()
        paper = self.paper_trading_var.get()
        invest = self.invest_by_per.get()

        self.admin = admin.find_one()
        self.admin['exchange'] = exchange
        self.admin['tradable_base_coins'] = base
        self.admin['investment'] = float(investment)
        self.admin['minimum_profit'] = float(min_profit)
        self.admin['paper_trading'] = paper
        self.admin['invest_by_per'] = invest

        admin.update_one({}, {'$set': self.admin})
        messagebox.showinfo("Information Updated",
                            "The information has been updated")


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
