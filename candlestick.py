#This file was based on Sentdex's tutorial on youtube

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib import style
import pandas as pd
import pandas_datareader as web

style.use('ggplot') #look for other styles

start = dt.datetime(2005, 1, 1)
end = dt.datetime(2017, 6, 30)

dataframe = web.DataReader('TSLA', 'google', start, end)

dataframe.to_csv('tsla.csv')

df = pd.read_csv('tsla.csv', parse_dates = True, index_col=0)

#df['100ma'] = df['Close'].rolling(window=100, min_periods=0).mean()

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