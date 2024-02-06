class run():

    def __init__(self):
        self.positions={}

    def update(self,instrument):
        self.positions[instrument]=1

    def get(self):
        print(self.positions)
    
    def r(self):
        print(self.positions)

e=run()
e.get()
e.update("BTCUSDT")
e.r()

