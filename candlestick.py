#This file was based on Sentdex's tutorial on youtube

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib import style
import pandas as pd
import pandas_datareader as web
import googlefinance
import json
import tty
import sys
import termios
import os

def candlestick(companycode):
    market_list = ["ASX", "SP"]
    market = input("Enter the market you want to enter: ")
    s_date = input("Enter the beginning of the data set: (yyyy/m/d): ").split('/') #TODO: add default values
    e_date = input("Enter the end of the data set: (yyyy/m/d): ").split('/')

    s_date = list(map(int, s_date))
    e_date = list(map(int, e_date))

    file = companycode + ".csv"

    if market in market_list:
        style.use('ggplot') #look for other styles

        start = dt.datetime(s_date[0], s_date[1], s_date[2])
        end = dt.datetime(e_date[0], e_date[1], e_date[2])

        dataframe = pd.DataFrame()

        try:
            data = json.dumps(googlefinance.getQuotes('market'+":" + companycode))
        except:
            print("Company cannot be found")

        dataframe = pd.DataFrame.from_dict(data, orient='index')
        dataframe.to_csv(file)

        df = pd.read_csv(file, parse_dates = True, index_col=0)

        df_ohlc = df['Close'].resample('10D').ohlc()
        df_volume = df['Volume'].resample('10D').sum()

        df_ohlc.reset_index(inplace=True)
        df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

        ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
        ax1.xaxis_date()

        candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

        plt.show()

        while True:
            orig_settings = termios.tcgetattr(sys.stdin)

            tty.setraw(sys.stdin)
            x = sys.stdin.read(1)[0]

            if x == 27:
                os.remove(file)

if __name__ == "__main__":
    candlestick(companycode)
