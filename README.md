# Options-Trading-Bot-Angel-Broking-

This is trading App Based on Options. This is fullstack project based on Django, you can host it on your own cloud server so that you can monitor your trades through any device during the day. The description of the strategy is at the end of the Page.
It is given the strategy has been updated according to the new API changes in **Angel Broking**
Procedure To install this on your PC -

 - Make Virtual env `virtualenv env`
 - Activate virtual enviroment `source env/bin/activate`
 - Install requirements. `pip3 install -r requirements.txt` or `pip install -r requirements.txt`
 - complete migrations through `python3 manage.py makemigrations` and `python3 manage.py migrate`
 - Run command to start the project `python3 manage.py runserver`

This should start your project. 

Description of different Pages on the APP.

1. Settings page (main page)






## Strategy Explanation

Strategy is strangle stratgy, similar to Iron condor strategy (calender strategy). Have a basic Idea of this options strategy before getting on the actual strtagy itself.

- selling at 9:20 strike price at entry time. (sell PE / CE current expiry) (recieved preimum is rounded off by 50) (lets call it **max pain**)
- Buy at same time (max pain + (recieved premium + difference)) → CE (Monthly expiry)
- Buy at same time (max pain - (recieved premium + difference)) → PE (monthly expiry)
- Exit at exit time (**3:20** in our case)/or/
- strike price reaches (Buyed CE strike + stop loss)
- strike price reaches (Buyed PE strike - stop loss)
- stoploss is set through dashboard.



