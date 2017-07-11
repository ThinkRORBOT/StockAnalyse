import bs4 as bs
import datetime as dt
import os
import fix_yahoo_finance
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import time

style.use('ggplot')

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []

    #saves list of companies in a pickle file
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        mapping = str.maketrans(".", "-")
        ticker = ticker.translate(mapping)
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers,f)

    print(tickers)
    return tickers

#save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False, reloat_data=False):
    if reload_sp500:
        tickers = save_sp500_tickers()

    #read from pickle file
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    #sets when the data should start and end
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2017, 6, 30)

    #save each company data in a csv file
    for ticker in tickers:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.get_data_yahoo(ticker, start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
            time.sleep(5.0)
        else:
            print('Already have {}'.format(ticker))

#get_data_from_yahoo()

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    #read each companies csv, choose only the adj close to combine into bigger file
    for count,ticker in enumerate(tickers):
        try:
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df.set_index('Date', inplace=True)

            df.rename(columns = {'Adj Close': ticker}, inplace=True)
            df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')

        except:
            print('stock_dfs/{}.csv'.format(ticker) + ' not found')

        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

#compile_data()


def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    #gets correlation between companies
    df_corr = df.corr()

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    #set the key of heat map to red(negative), yellow and green (positive)
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    #changes the format of the table so data makes more sense
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1) #sets maximum range of heatmap
    plt.tight_layout()
    plt.show()

visualize_data()