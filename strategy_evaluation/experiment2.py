import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import marketsimcode as mkt_sim
import StrategyLearner
from util import get_data

def author():
    return 'mchiang30'

def output(symbol='JPM',
                sd_in=dt.datetime(2008,1,1),
                ed_in=dt.datetime(2009,12,31),
                sd_out=dt.datetime(2010, 1, 1),
                ed_out=dt.datetime(2011, 12, 31),
                sv=100000,
                commission=0,
                impact=0,
                gen_plots=True,
                stats=False):

    impact1 = 0.0
    learner1 = StrategyLearner.StrategyLearner(verbose=False, impact=impact1, commission=commission)
    learner1.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl1_trades = learner1.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl1_val = mkt_sim.compute_portvals(sl1_trades, start_val=sv, commission=commission, impact=impact1)
    b1_val = benchmark(symbol, sd_in, ed_in, sv, commission, impact1)
    short_entries1, long_entries1 = entries(sl1_trades, symbol)

    impact2 = 0.005
    learner2 = StrategyLearner.StrategyLearner(verbose=False, impact=impact2, commission=commission)
    learner2.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl2_trades = learner2.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl2_val = mkt_sim.compute_portvals(sl2_trades, start_val=sv, commission=commission, impact=impact2)
    b2_val = benchmark(symbol, sd_in, ed_in, sv, commission, impact2)
    short_entries2, long_entries2 = entries(sl2_trades, symbol)

    impact3 = 0.015
    learner3 = StrategyLearner.StrategyLearner(verbose=False, impact=impact3, commission=commission)
    learner3.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl3_trades = learner3.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl3_val = mkt_sim.compute_portvals(sl3_trades, start_val=sv, commission=commission, impact=impact3)
    b3_val = benchmark(symbol, sd_in, ed_in, sv, commission, impact3)
    short_entries3, long_entries3 = entries(sl3_trades, symbol)

    impact4 = 0.045
    learner4 = StrategyLearner.StrategyLearner(verbose=False, impact=impact4, commission=commission)
    learner4.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl4_trades = learner4.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl4_val = mkt_sim.compute_portvals(sl4_trades, start_val=sv, commission=commission, impact=impact4)
    b4_val = benchmark(symbol, sd_in, ed_in, sv, commission, impact4)
    short_entries4, long_entries4 = entries(sl4_trades, symbol)

    if gen_plots:
        gen_plot_impact(sl1_val, b1_val, sl2_val, b2_val, sl3_val, b3_val, sl4_val, b4_val, impact1, impact2, impact3, impact4, symbol)
        gen_plot_trades(sl1_val, b1_val, short_entries1, long_entries1, impact1, symbol)
        gen_plot_trades(sl2_val, b2_val, short_entries2, long_entries2, impact2, symbol)
        gen_plot_trades(sl3_val, b3_val, short_entries3, long_entries3, impact3, symbol)
        gen_plot_trades(sl4_val, b4_val, short_entries4, long_entries4, impact4, symbol)

    if stats:
        gen_stats(sl1_val, b1_val, short_entries1, long_entries1, impact1)
        gen_stats(sl2_val, b2_val, short_entries2, long_entries2, impact2)
        gen_stats(sl3_val, b3_val, short_entries3, long_entries3, impact3)
        gen_stats(sl4_val, b4_val, short_entries4, long_entries4, impact4)

        with open('report_stats/output_exp2.txt', 'a') as f:
            print('--------------------', file=f)
            print('\n', file=f)



def benchmark(symbol, sd, ed, sv, commission, impact):
    trades = get_data(['SPY'], pd.date_range(sd, ed)).rename(columns={'SPY': symbol})
    for col in trades.columns:
        trades[col].values[:] = 0
    trades.loc[trades.index[0]] = 1000
    val = mkt_sim.compute_portvals(trades, start_val=sv, commission=commission, impact=impact)
    return val

def gen_plot_impact(sl1_val, b1_val, sl2_val, b2_val, sl3_val, b3_val, sl4_val, b4_val, impact1, impact2, impact3, impact4, symbol):
    pd.plotting.register_matplotlib_converters()

    plt.figure(figsize=(14, 8))
    plt.title('Strategy Learner Impact Comparison ({})'.format(symbol))
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.xticks(rotation=25)
    plt.grid()
    plt.plot(sl1_val, label='Learner - Impact {}'.format(impact1), color='green')
    plt.plot(b1_val, label='Benchmark - Impact {}'.format(impact1), color='green', linestyle='dashed', alpha=0.2)
    plt.plot(sl2_val, label='Learner - Impact {}'.format(impact2), color='red')
    plt.plot(b2_val, label='Benchmark - Impact {}'.format(impact2), color='red', linestyle='dashed', alpha=0.2)
    plt.plot(sl3_val, label='Learner - Impact {}'.format(impact3), color='blue')
    plt.plot(b3_val, label='Benchmark - Impact {}'.format(impact3), color='blue', linestyle='dashed', alpha=0.2)
    plt.plot(sl4_val, label='Learner - Impact {}'.format(impact4), color='purple')
    plt.plot(b4_val, label='Benchmark - Impact {}'.format(impact4), color='purple', linestyle='dashed', alpha=0.2)
    plt.legend()
    plt.savefig('./images/experiment2_impacts.png')
    plt.clf()

def gen_plot_trades(sl_val, b_val, short, long, impact, symbol):
    pd.plotting.register_matplotlib_converters()

    plt.figure(figsize=(14, 8))
    plt.title('Trades & Impact Comparison ({})'.format(symbol))
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.xticks(rotation=25)
    plt.grid()
    plt.plot(sl_val, label='Learner - Impact {}'.format(impact), color='red')
    plt.plot(b_val, label='Benchmark - Impact {}'.format(impact), color='purple')
    for i in long:
        plt.axvline(i, color='black')
    for i in short:
        plt.axvline(i, color='blue')
    plt.legend()
    plt.savefig('./images/experiment2_trades{}.png'.format(impact))
    plt.clf()

def gen_stats(val, bench, short, long, impact):
    cum_ret = val['value'][-1] / val['value'][0] - 1
    bench_cum_ret = bench['value'][-1] / bench['value'][0] - 1

    shorts = len(short)
    longs = len(long)
    total = shorts + longs

    with open('report_stats/output_exp2.txt', 'a') as f:
        print('Impact {}'.format(impact), file=f)
        print('Cumulative Return Strategy: {:.6f}'.format(cum_ret), file=f)
        print('Cumulative Return Benchmark: {:.6f}'.format(bench_cum_ret), file=f)
        print('% Change in Cumulative Returns: {:.6f}'.format((cum_ret - bench_cum_ret) / np.abs(bench_cum_ret) * 100), file=f)
        print('{} total number of entries: {} SHORT, {} LONG'.format(total, shorts, longs), file=f)
        print('\n', file=f)

def entries(trades, symbol):
    short_entries = []
    long_entries = []

    temp = 0
    action = 'init'
    for i in trades.index:
        temp += trades.loc[i].loc[symbol]
        if temp > 0:
            if action == -1 or action == 'init':
                long_entries.append(i)
                action = 1
        elif temp < 0:
            if action == 1 or action == 'init':
                short_entries.append(i)
                action = -1
        else:
            action = 'init'

    return short_entries, long_entries

if __name__ == "__main__":
    pass