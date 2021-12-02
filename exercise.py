import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statistics import stdev

# Logic


def check_uniqueness(lst):
    """
    Check if a list contains only unique values.
    Returns True only if all values in the list are unique, False otherwise
    """
    return True if len(set(lst))==len(lst) else False



def smallest_difference(array):
    """
    Code a function that takes an array and returns the smallest
    absolute difference between two elements of this array
    Please note that the array can be large and that the more
    computationally efficient the better
    """
    array = sorted(array) #sort array
    #create arbitarily large number to compare
    diff = 10**20
    #compare adjacent pairs in list
    for i in range((len(array)-1)):
        curr = abs(array[i+1] - array[i])
        if curr < diff:
            diff = curr
    return diff


# Finance and DataFrame manipulation


def macd(prices, window_short=12, window_long=26):
    """
    Code a function that takes a DataFrame named prices and
    returns it's MACD (Moving Average Convergence Difference) as
    a DataFrame with same shape
    Assume simple moving average rather than exponential moving average
    The expected output is in the output.csv file
    """
    # # Get the 26-day SMA of prices
    k = prices['SX5T Index'].rolling(window=window_short).mean()
    # Get the 12-day SMA of prices
    d = prices['SX5T Index'].rolling(window=window_long).mean()
    prices['macd'] = k - d
    return prices


def sortino_ratio(prices):
    """
    Code a function that takes a DataFrame named prices and
    returns the Sortino ratio for each column
    Assume risk-free rate = 0
    On the given test set, it should yield 0.05457
    """
    #get daily returns of sx5t index
    daily_return = prices['SX5T Index'].pct_change().dropna(axis=0)
    #get rate of return
    start = prices['SX5T Index'][0]
    end = prices['SX5T Index'][-1]
    # r =  (end - start) / start #actual rate of return
    r = ((end / start) ** (1/21)) -1 #anualized rate of return
    # r = daily_return.mean() # 2mean rate of return
    #get downside deviation/risk
    #not sure if daily_return-r or daily_return-stdev or just daily_return, no explicit MAR
    negative_excess_return = [i for i in daily_return-stdev(daily_return) if i < 0] 
    sq_excess = [i**2 for i in negative_excess_return]
    downside_dev = np.sqrt(sum(sq_excess) / len(daily_return))
    return r / downside_dev

def expected_shortfall(prices, level=0.95):
    """
    Code a function that takes a DataFrame named prices and
    returns the expected shortfall at a given level
    On the given test set, it should yield -0.03468
    """
    #get daily returns of sx5t index
    daily_returns = prices.copy().pct_change().dropna(axis=0).rename(columns={'SX5T Index': 'dr1'})
    #modify returns with a constant value
    daily_returns['dr2'] = daily_returns['dr1'].copy()
    daily_returns.loc[daily_returns['dr1'] < daily_returns['dr1'].quantile(level), 'dr2'] -= 0.02
    #calc value at risk of daily returns
    var = daily_returns.quantile(1-level, axis=0, interpolation='higher')
    #get ES: average of worst losses (under var)
    return daily_returns[daily_returns.lt(var, axis=1)]['dr1'].mean()


# Plot


def visualize(prices, path):
    """
    Code a function that takes a DataFrame named prices and
    saves the plot to the given path
    """
    plt.figure()
    prices.plot()
    plt.savefig(path)


if __name__=="__main__":
    df = pd.read_csv('data/data.csv').set_index('date')
    df.index = pd.to_datetime(df.index)
    print("MACD")
    print(macd(df).tail())
    print("Sortino ratio is not correct, couldn't work out which combination \nof rate or return and downside risk was the right answer")
    print(sortino_ratio(df))
    visualize(df, "data/plot.jpg")