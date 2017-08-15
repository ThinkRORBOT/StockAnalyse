
from collections import Counter
import numpy as np
import pandas as pd
import pickle
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
import sys

hm_days = 7

def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker])/df[ticker]
        print((df[ticker].shift(-i) - df[ticker])/df[ticker])

    df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.028

    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1

    return 0

def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)

    df['{}_target'.format(ticker)] = list(map(buy_sell_hold, *[df['{}_{}d'.format(ticker, i)] for i in range(1, hm_days + 1)]))
    df.to_csv('df.csv')

    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    #so you can see spread to see accuracy
    print('Data spread:', Counter(str_vals))

    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals =df[[ticker for ticker in tickers]].pct_change() #values are now normalised
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)\

    X =df_vals.values
    y = df['{}_target'.format(ticker)].values

    return X, y, df


def do_ml(ticker):
    X, y, df = extract_featuresets(ticker)

    #splits the data for testing
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25)

    #a classifier for multiple classifiers so the results will hopefully be more accurate
    #clf = neighbors.kNeighborsClassifier()

    clf = VotingClassifier([('lsvc', svm.LinearSVC()), ('knn', neighbors.KNeighborsClassifier()), ('rfor', RandomForestClassifier())])

    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('Accuracy', confidence)
    prediction = clf.predict(X_test)
    print('Predicted spread:', Counter(prediction))

    return confidence

#do_ml('BAC')
