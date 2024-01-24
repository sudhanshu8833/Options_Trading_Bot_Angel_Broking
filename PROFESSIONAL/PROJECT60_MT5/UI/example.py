#!/Users/sid/Desktop/algo-trading/PROFESSIONAL/PROJECT60_MT5/UI/env python3
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import pymongo
import json
import threading
import tkinter
import tkinter.messagebox
import customtkinter
import logging
# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("green")


logging.getLogger("pymongo").setLevel(logging.WARNING)

data = {}
with open("data.json", "r") as json_file:
    data = json.load(json_file)
database = data['database']
uri = data['mongo_uri']

client = MongoClient(uri, tlsCAFile=data['ca'], connect=False)
bot = client[database]
admin = bot['Admin']


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("MT5 BOT")
        self.geometry(f"{1400}x{900}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=4)
        # self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=2)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="MT5 BOT", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))


        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event,text="side button 1")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event,text="side button 2")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10,)
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event,text='side button 3')
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)



        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)

        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))



        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=500)
        self.tabview.grid(row=0, column=1, rowspan=3, padx=(
            20, 20), pady=(20, 20), sticky="nsew")
        
        self.tabview.add("Dashboard")
        self.tabview.add("Orders")
        self.tabview.add("Zones")
        self.tabview.add("Backtesting")
        self.tabview.add("Reports")
        self.tabview.add("Background")
        self.tabview.tab("Dashboard").grid_columnconfigure(
            (1,2,3), weight=3)  # configure grid of individual tabs
        self.tabview.tab("Dashboard").grid_columnconfigure(
            0, weight=1)
        # self.tabview.tab("Dashboard").grid_rowconfigure(
        #     (0,1,2,3,4,5), weight=1)
        
        self.switch = customtkinter.CTkSwitch(self.tabview.tab("Dashboard"),
             text="ON / OFF")
        self.switch.grid(row=0,column=0,columnspan=2,pady=(40,0), padx=20)


        self.lots_label=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="Lots")
        self.lots_label.grid(row=1, column=0,  padx=(20, 20), pady=(20, 0), sticky="nwes")
        self.lots = customtkinter.CTkEntry(self.tabview.tab("Dashboard"), placeholder_text="Lots")
        self.lots.grid(row=1, column=1,  padx=(20, 20), pady=(20, 0), sticky="nwes")

        self.symbol_label=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="Symbol")
        self.symbol_label.grid(row=2, column=0,  padx=(20, 20), pady=(20, 0), sticky="nwes")
        self.Symbol = customtkinter.CTkEntry(self.tabview.tab("Dashboard"), placeholder_text="Symbol")
        self.Symbol.grid(row=2, column=1,  padx=(20, 20), pady=(20, 0), sticky="nwes")

        self.submit = customtkinter.CTkButton(self.tabview.tab("Dashboard"),text="Submit", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.submit.grid(row=3, column=0,columnspan=2, padx=(20, 20), pady=(20, 0), sticky="n")


        self.Daily_Profits_label=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="Daily Profits",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.Daily_Profits_label.grid(row=0, column=2,  padx=(20, 20),pady=(40,0), sticky="e")
        self.Daily_profits=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="1.23",text_color="green",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.Daily_profits.grid(row=0, column=3,  padx=(20, 20),pady=(40,0), sticky="w")
        
        self.weekly_profit_label=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="Weekly Profits",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.weekly_profit_label.grid(row=1, column=2,  padx=(20, 20),pady=(20,0), sticky="e")
        self.weekly_profits=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="10.34",text_color="green",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.weekly_profits.grid(row=1, column=3,  padx=(20, 20),pady=(20,0), sticky="w")

        self.monthly_profit_label=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="Monthly Profits",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.monthly_profit_label.grid(row=2, column=2,  padx=(20, 20),pady=(20,0), sticky="e")
        self.monthly_profits=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="24.56",text_color="green",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.monthly_profits.grid(row=2, column=3,  padx=(20, 20),pady=(20,0), sticky="w")


        self.bid_label=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="BID",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.bid_label.grid(row=4, column=0,  padx=(20, 20),pady=(60,0), sticky="e")
        self.bid=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="24.56",text_color="yellow",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.bid.grid(row=4, column=1,  padx=(20, 20),pady=(60,0), sticky="w")

        self.ask_label=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="ASK",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.ask_label.grid(row=5, column=0,  padx=(20, 20), sticky="e")
        self.ask=customtkinter.CTkLabel(self.tabview.tab("Dashboard"),text="24.89",text_color="green",font=customtkinter.CTkFont(size=15, weight="bold"))
        self.ask.grid(row=5, column=1,  padx=(20, 20), sticky="w")




        self.patterns = customtkinter.CTkFrame(self.tabview.tab("Dashboard"))
        self.patterns.grid(row=6, column=0,columnspan=2, padx=(80, 20), pady=(20, 0), sticky="nsew")
        self.patter1 = customtkinter.CTkCheckBox(master=self.patterns,text="Pattern 1")
        self.patter1.grid(row=6, column=3,columnspan=3, pady=(20, 0), padx=20, sticky="w")
        self.pattern2 = customtkinter.CTkCheckBox(master=self.patterns,text="pattern 2")
        self.pattern2.grid(row=7, column=3, pady=(20, 0), padx=20, sticky="w")
        self.pattern3 = customtkinter.CTkCheckBox(master=self.patterns,text="pattern 3")
        self.pattern3.grid(row=8, column=3, pady=20, padx=20, sticky="w")


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
