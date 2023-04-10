import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import marketsimcode as mkt_sim
import datetime as dt
from util import plot_data, get_data

class TheoreticallyOptimalStrategy(object):
    def __init__(self):
        pass

    def testPolicy(self, symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv=100000):
        prices = get_data([[symbol][0]], pd.date_range(sd, ed))[[[symbol][0]]].ffill().bfill()
        trades = get_data([[symbol][0]], pd.date_range(sd, ed))[['SPY']].rename(columns={'SPY':[symbol][0]})
        temp = 0

        for col in trades.columns:
            trades[col].values[:] = 0

        for i in range(len(trades.index) - 1):
            if prices.loc[trades.index[i]].loc[[symbol][0]] >= prices.loc[trades.index[i + 1]].loc[[symbol][0]]:
                sign = -1
            else:
                sign = 1
            trades.loc[trades.index[i]].loc[[symbol][0]] = sign * 1000 - temp
            temp -= (sign * 1000 - temp) * -1
        return trades

def author(self):
    return 'mchiang30'

def output(sv, sd, ed, symbol, gen_stats=False, gen_plot=False):
    trades = get_data(['SPY'], pd.date_range(sd, ed)).rename(columns={'SPY':'JPM'})
    for col in trades.columns:
        trades[col].values[:] = 0
    trades.loc[trades.index[0]] = 1000

    benchmark_val = mkt_sim.compute_portvals(trades, sv, commission=0.00, impact=0.00)
    theoretical_val = mkt_sim.compute_portvals(TheoreticallyOptimalStrategy().testPolicy(symbol, sd=sd, ed=ed, sv=sv), sv, commission=0.00, impact=0.00)

    if gen_plot:
        plt.figure(figsize=(12, 9))
        plt.title('Theoretically Optimal Strategy vs Benchmark for JPM')
        plt.xlabel('Dates')
        plt.xticks(rotation=25)
        plt.ylabel('Normalized value')

        plt.plot(theoretical_val['value'] / theoretical_val['value'][0], label='theoretical', color='red')
        plt.plot(benchmark_val['value'] / benchmark_val['value'][0], label='benchmark', color='purple')

        plt.legend()
        plt.grid()

        plt.savefig('./images/tos_b_comp.png')
        #plt.show()
        plt.clf()

    if gen_stats:
        benchmark_cum_ret = benchmark_val['value'][-1] / benchmark_val['value'][0] - 1
        benchmark_std_daily_ret = ((benchmark_val['value'] / benchmark_val['value'].shift(1) - 1).iloc[1:]).std()
        benchmark_mean_daily_ret = ((benchmark_val['value'] / benchmark_val['value'].shift(1) - 1).iloc[1:]).mean()

        theoretical_cum_ret = theoretical_val['value'][-1] / theoretical_val['value'][0] - 1
        theoretical_std_daily_ret = ((theoretical_val['value'] / theoretical_val['value'].shift(1) - 1).iloc[1:]).std()
        theoretical_mean_daily_ret = ((theoretical_val['value'] / theoretical_val['value'].shift(1) - 1).iloc[1:]).mean()

        d = [['{:.6f}'.format(theoretical_cum_ret), '{:.6f}'.format(benchmark_cum_ret)],
                 ['{:.6f}'.format(theoretical_std_daily_ret), '{:.6f}'.format(benchmark_std_daily_ret)],
                 ['{:.6f}'.format(theoretical_mean_daily_ret), '{:.6f}'.format(benchmark_mean_daily_ret)]]
        strats = ['TOS', 'Benchmark']
        metric = ['Cumulative Return', 'Stdev of daily returns', 'Mean of daily returns']
        df_tb_stats = pd.DataFrame(d, metric, strats)
        print(df_tb_stats.to_string())


if __name__ == '__main__':
    pass