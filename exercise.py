import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = 'browser' 

prices = pd.read_csv(r'data/data.csv', sep=';')


# Logic


def smallest_difference(array):
    # Code a function that takes an array and returns the smallest
    # absolute difference between two elements of this array
    # Please note that the array can be large and that the more
    # computationally efficient the better
    #
    # I create a set in order to remove duplicated? Then i convert it into a
    # sorted list.
    sorted_unique_arr = np.sort(list(set(array)))

    # If there is any duplicates, the answer is 0.
    if len(sorted_unique_arr) < len(array):
        return 0
    # I return the smallest difference between each element
    else:
        return min([(abs(sorted_unique_arr[i] - sorted_unique_arr[i+1]))
                    for i in range(len(sorted_unique_arr)-1)])


# Finance and DataFrame manipulation


def macd(prices, window_short=12, window_long=26):
    # Code a function that takes a DataFrame named prices and
    # returns it's MACD (Moving Average Convergence Difference) as
    # a DataFrame with same shape
    # Assume simple moving average rather than exponential moving average
    # The expected output is in the output.csv file
    #
    # I changed the variable window_short in order to find the right results.

    prices['ma12'] = prices['SX5T Index'].rolling(window_short).mean()
    prices['ma26'] = prices['SX5T Index'].rolling(window_long).mean()
    prices['macd_12_26'] = prices['ma12'] - prices['ma26']

    del prices['ma12'], prices['ma26']
    return prices


def sortino_ratio(prices):
    # Code a function that takes a DataFrame named prices and
    # returns the Sortino ratio for each column
    # Assume risk-free rate = 0
    # On the given test set, it should yield 0.05457
    # 
    # I do not find the right results. It might be because of the log return 
    # or because the returns/volatility annualization. 
    
    # I compute log-returns
    prices['log_returns'] = np.log(prices['SX5T Index']) - \
                            np.log(prices['SX5T Index'].shift(1))
    # I compute the mean rof thoses returns
    mean_return = (prices['log_returns']).mean()
    risk_free_rate = 0
    # I compute the volatily for the negative returns
    vol = prices.loc[prices['log_returns'] < 0]['log_returns'].std()
    sortino_ratio = (mean_return - risk_free_rate) / vol
    sortino_ratio = sortino_ratio * np.sqrt(252)
    return sortino_ratio


def expected_shortfall(prices, level=0.95):
    # Code a function that takes a DataFrame named prices and
    # returns the expected shortfall at a given level
    # On the given test set, it should yield -0.03468
    prices['returns'] = prices['SX5T Index'].pct_change().dropna()
    # We compute the historical VaR
    # We sort returns and drop nan values
    returns = np.sort(prices['returns'])
    returns = returns[~np.isnan(returns)]
    # Then we compute the var at the right level
    number_of_values = int((1 - level) * len(returns))
    VaR = returns[number_of_values]
    # We compute the average returns under the Value at Risk
    expected_shortfall = returns[returns <= VaR].mean()
    # We return the expectation of all the returns below the var
    return expected_shortfall


# Plot


def visualize(prices):
    # Code a function that takes a DataFrame named prices and
    # saves the plot to the given path

    # I choose to use plotly rathen than matplotlib or any others librairies
    # because of the interactivity with the user and because of the potentials
    # uses (web dashboard with Dash, a lot of documentation (JS librairy))

    fig = go.Figure([go.Scatter(x=prices['date'], y=prices['SX5T Index'])])
    fig.update_layout(
        title="Time series graph on 'Price' DataFrame",
        xaxis_title="Date",
        yaxis_title="Price")
    # Uncomment this lign if you want to see it directly
    # fig.show()
    fig.write_html('prices.html')
    return ('Figure saved')
