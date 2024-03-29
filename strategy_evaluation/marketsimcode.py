import datetime as dt
import os

import numpy as np

import pandas as pd
from util import get_data, plot_data


def author():
    return 'mchiang30'


def compute_portvals(
        orders_file,
        start_val=1000000,
        commission=9.95,
        impact=0.005,
):
    """
    Computes the portfolio values.

    :param orders_file: Name of the dataframe object
    :type orders_df: dataframe object
    :param start_val: The starting value of the portfolio
    :type start_val: int
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)
    :type commission: float
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction
    :type impact: float
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.
    :rtype: pandas.DataFrame
    """
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    data = orders_file
    stock_df = get_data(['SPY'], pd.date_range(data.index.sort_values()[0], data.index.sort_values()[-1]), addSPY=True, colname='Adj Close').rename(columns={'SPY': 'value'})
    # print(stock_df.index)

    symbol_list = {}
    share_list = {}
    temp_val = start_val

    for i in stock_df.index:
        if data.columns[0] not in symbol_list:
            symbol_list[data.columns[0]] = get_data([data.columns[0]], pd.date_range(i, data.index.sort_values()[-1]), addSPY=True, colname='Adj Close').ffill().bfill()
        if data.loc[i].loc[data.columns[0]] != 0:
            if data.loc[i].loc[data.columns[0]] > 0:
                sign = 1
                share_list[data.columns[0]] = data.loc[i].loc[data.columns[0]] * sign + share_list.get(data.columns[0], 0)
                temp_val -= (commission * -1 + (impact + sign) * symbol_list[data.columns[0]].loc[i].loc[data.columns[0]] * data.loc[i].loc[data.columns[0]] * -1) * -1
            else:
                sign = -1
                share_list[data.columns[0]] = abs(data.loc[i].loc[data.columns[0]]) * sign + share_list.get(data.columns[0], 0)
                temp_val -= (commission * -1 + (impact + sign) * symbol_list[data.columns[0]].loc[i].loc[data.columns[0]] * abs(data.loc[i].loc[data.columns[0]]) * -1) * -1

        temp = 0
        for j in share_list:
            temp -= share_list[j] * symbol_list[j].loc[i].loc[j] * -1
        stock_df.loc[i].loc['value'] = temp + temp_val
    return stock_df


def test_code():
    """
    Helper function to test code
    """
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-13.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

        # Get portfolio stats
        # Here we just fake the data. you should use your code from previous assignments.
        start_date = dt.datetime(2011, 1, 1)
        end_date = dt.datetime(2013, 6, 1)
        cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [
            0.2,
            0.01,
            0.02,
            1.5,
        ]
        cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [
            0.2,
            0.01,
            0.02,
            1.5,
        ]

    # Compare portfolio against $SPX
    print(f"Date Range: {start_date} to {end_date}")
    print()
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")
    print()
    print(f"Cumulative Return of Fund: {cum_ret}")
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")
    print()
    print(f"Standard Deviation of Fund: {std_daily_ret}")
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")
    print()
    print(f"Average Daily Return of Fund: {avg_daily_ret}")
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")
    print()
    print(f"Final Portfolio Value: {portvals[-1]}")


if __name__ == "__main__":
    pass
