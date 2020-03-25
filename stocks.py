########################IMPORTS###########################
from threading import Timer
import pandas as pd
from stockstats import StockDataFrame as sdf
from time import time, sleep
from os import system






##########################for refresh every 30 seconds######################
class RepeatedTimer(object):
    start = time()
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False





#############################function for alerting % change################
def alert(inc,dec,market  = True):
    global start
    system("clear")
    print(print('\x1b[3;31;43m' + "TIME REMAINING TILL THE PROGRAM ENDS: {} minutes".format((1800-(time()-start))/60) + '\x1b[0m'))
    if market:
        print("")
        print("______________________________________________________________________________")
        print('\x1b[3;31;43m' + '-----------------ALERT-------------------' + '\x1b[0m')
        print(len(inc)+len(dec)," Stocks have change of more than 2% in last 30 seconds")
        print("")
        if len(inc)>0:
            print("--------------------------Stocks Increased--------------------------------")
            print("Following",len(inc),"stocks prices jumped more than 2% in last 30 seconds")
            # print("Company Name                              %change")
            print(inc)
            print("")
            print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
        else:
            print("No Stocks have Increased more than 2% in last 30 seconds")
        if len(dec)>0:
            print("--------------------------Stocks Decreased--------------------------------")
            print("Following",len(dec),"stocks prices droped more than 2% in last 30 seconds")
            # print("Company Name                              %change")
            print(dec)
        else:
            print("No stocks have decreased more than 2% in the last 30 seconds")
    else:
        print("################## NO CHANGE IN PRICES IN LAST 30 SECONDS ##########################")

    print("______________________________________________________________________________")




####################################calculating %change########################
def change(data1=None):
    global start
    if data1 is None:
        data1 = sdf.retype(pd.read_html('https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9')[0])
        sleep(30)#Wait 30 second for the next dataset
        data2 = sdf.retype(pd.read_html('https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9')[0])
    else:
        data2 = sdf.retype(pd.read_html('https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9')[0])

    change  = sdf()
    try:
        change["Company Name"] = data1["company name"]
        change["Change"] = data2["%chg"] - data1["%chg"] #calculating diff. of %chg
        change['Company Name'] = change['Company Name'].apply(lambda x: x[:-36]) #removing extra text from name
        change.set_index('Company Name',inplace = True)
    except:
        print("Index error of scrapped dataframe line 76")

    inc = change[change['Change']>2] # stock jumped more than 2%
    dec = change[change['Change']<-2] # stock drops more than 2%
    market = True
    if len(change) == len(change[change['Change']==0]):
        market = False
    alert(inc,dec,market)
    return data2






###########################################running the program#########################

start = time()
system("clear")
print('\x1b[3;31;43m' + '-_-_-_-_-_-_-_-_-_-_-_-_-_WELCOME-_-_-_-_-_-_-_-_-_-_-_-_-_-_' + '\x1b[0m')
print('\x1b[3;31;43m' + 'Please Wait 30 seconds for the data to load' + '\x1b[0m')
data = change()
stock = RepeatedTimer(30,change,data)
try:
    sleep(1800)#Wait for timer to run for 30 mins i.e 18000 seconds
finally:
    stock.stop()#stop the process

###############################END of The program####################################
