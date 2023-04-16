import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import marketsimcode as mkt_sim
import StrategyLearner
import ManualStrategy
from util import get_data

def author():
    return 'mchiang30'

def output(symbol='JPM',
           sd_in=dt.datetime(2008, 1, 1),
           ed_in=dt.datetime(2009, 12, 31),
           sd_out=dt.datetime(2010, 1, 1),
           ed_out=dt.datetime(2011, 12, 31),
           sv=100000,
           commission=9.95,
           impact=0.005,
           gen_plots=True,
           stats=False):

    manual_val = mkt_sim.compute_portvals(ManualStrategy.ManualStrategy().testPolicy(symbol, sd=sd_in, ed=ed_in, sv=sv), start_val=sv, commission=commission, impact=impact)

    learner = StrategyLearner.StrategyLearner(verbose=False, impact=impact, commission=commission)
    learner.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    strategy_val = mkt_sim.compute_portvals(learner.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv), start_val=sv, commission=commission, impact=impact)

    benchmark_val = benchmark(symbol, sd_in, ed_in, sv, commission, impact)


    if stats:
        gen_stats(manual_val, 'Manual', 'In Sample')
        gen_stats(strategy_val, 'Strategy', 'In Sample')
        gen_stats(benchmark_val, 'Benchmark', 'In Sample')
        with open('report_stats/output_exp1.txt', 'a') as f:
            print('++++++++++++++++++++', file=f)
            print('\n', file=f)

    if gen_plots:
        gen_plot(manual_val, strategy_val, benchmark_val, 'In Sample', symbol)

    manual_val = mkt_sim.compute_portvals(ManualStrategy.ManualStrategy().testPolicy(symbol, sd=sd_out, ed=ed_out, sv=sv), start_val=sv, commission=commission, impact=impact)

    learner = StrategyLearner.StrategyLearner(verbose=False, impact=impact, commission=commission)
    learner.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    strategy_val = mkt_sim.compute_portvals(learner.testPolicy(symbol=symbol, sd=sd_out, ed=ed_out, sv=sv), start_val=sv, commission=commission, impact=impact)

    benchmark_val = benchmark(symbol, sd_out, ed_out, sv, commission, impact)


    if stats:
        gen_stats(manual_val, 'Manual', 'Out Sample')
        gen_stats(strategy_val, 'Strategy', 'Out Sample')
        gen_stats(benchmark_val, 'Benchmark', 'Out Sample')
        with open('report_stats/output_exp1.txt', 'a') as f:
            print('--------------------', file=f)
            print('\n', file=f)

    if gen_plots:
        manual_val['value'] = manual_val['value'] / manual_val['value'][0]
        strategy_val['value'] = strategy_val['value'] / strategy_val['value'][0]
        benchmark_val['value'] = benchmark_val['value'] / benchmark_val['value'][0]
        gen_plot(manual_val, strategy_val, benchmark_val, 'Out Sample', symbol)

def benchmark(symbol, sd, ed, sv, commission, impact):
    trades = get_data(['SPY'], pd.date_range(sd, ed)).rename(columns={'SPY': symbol})
    for col in trades.columns:
        trades[col].values[:] = 0
    trades.loc[trades.index[0]] = 1000
    val = mkt_sim.compute_portvals(trades, start_val=sv, commission=commission, impact=impact)
    return val

def gen_stats(val, strat, sample):
    cum_ret = val['value'][-1] / val['value'][0] - 1
    std_daily_ret = ((val['value'] / val['value'].shift(1) - 1).iloc[1:]).std()
    mean_daily_ret = ((val['value'] / val['value'].shift(1) - 1).iloc[1:]).mean()

    with open('report_stats/output_exp1.txt', 'a') as f:
        print('{} - {}'.format(strat, sample), file=f)
        print('Cumulative Return: {:.6f}'.format(cum_ret), file=f)
        print('Std Return: {:.6f}'.format(std_daily_ret), file=f)
        print('Mean Return: {:.6f}'.format(mean_daily_ret), file=f)
        print('\n', file=f)

def gen_plot(manual_val, strategy_val, benchmark_val, sample, symbol):
    pd.plotting.register_matplotlib_converters()

    plt.figure(figsize=(14, 8))
    plt.title('Manual Strategy vs Strategy Learner - {} ({})'.format(sample, symbol))
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.xticks(rotation=25)
    plt.grid()
    plt.plot(manual_val, label='Manual Strategy', color='red')
    plt.plot(strategy_val, label='Strategy Learner (Q Learning Bot)', color='green')
    plt.plot(benchmark_val, label='Benchmark', color='purple')
    plt.legend()
    plt.savefig('./images/experiment1_{}.png'.format(sample))
    plt.clf()

if __name__=="__main__":
    pass