import pandas as pd
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
    sl1_val = mkt_sim.compute_portvals(learner1.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv), start_val=sv, commission=commission, impact=impact1)
    b1_val = benchmark(symbol, sd_in, ed_in, sv, commission, impact1)

    impact2 = 0.005
    learner2 = StrategyLearner.StrategyLearner(verbose=False, impact=impact2, commission=commission)
    learner2.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl2_val = mkt_sim.compute_portvals(learner2.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv), start_val=sv, commission=commission, impact=impact2)
    b2_val = benchmark(symbol, sd_in, ed_in, sv, commission, impact2)

    impact3 = 0.01
    learner3 = StrategyLearner.StrategyLearner(verbose=False, impact=impact3, commission=commission)
    learner3.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl3_val = mkt_sim.compute_portvals(learner3.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv), start_val=sv, commission=commission, impact=impact3)
    b3_val = benchmark(symbol, sd_in, ed_in, sv, commission, impact3)

    impact4 = 0.05
    learner4 = StrategyLearner.StrategyLearner(verbose=False, impact=impact4, commission=commission)
    learner4.add_evidence(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv)
    sl4_val = mkt_sim.compute_portvals(learner4.testPolicy(symbol=symbol, sd=sd_in, ed=ed_in, sv=sv), start_val=sv, commission=commission, impact=impact4)
    b4_val = benchmark(symbol, sd_in, ed_in, sv, commission, impact4)

    if gen_plots:
        gen_plot_impact(sl1_val, b1_val, sl2_val, b2_val, sl3_val, b3_val, sl4_val, b4_val, symbol)


def benchmark(symbol, sd, ed, sv, commission, impact):
    trades = get_data(['SPY'], pd.date_range(sd, ed)).rename(columns={'SPY': symbol})
    for col in trades.columns:
        trades[col].values[:] = 0
    trades.loc[trades.index[0]] = 1000
    val = mkt_sim.compute_portvals(trades, start_val=sv, commission=commission, impact=impact)
    return val

def gen_plot_impact(sl1_val, b1_val, sl2_val, b2_val, sl3_val, b3_val, sl4_val, b4_val, symbol):
    pd.plotting.register_matplotlib_converters()

    plt.figure(figsize=(14, 8))
    plt.title('Strategy Learner Impact Comparison ({})'.format(symbol))
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.xticks(rotation=25)
    plt.grid()
    plt.plot(sl1_val, label='Learner - Impact 0.0', color='green')
    plt.plot(b1_val, label='Benchmark - Impact 0.0', color='green', linestyle='dashed', alpha=0.2)
    plt.plot(sl2_val, label='Learner - Impact 0.005', color='red')
    plt.plot(b2_val, label='Benchmark - Impact 0.005', color='red', linestyle='dashed', alpha=0.2)
    plt.plot(sl3_val, label='Learner - Impact 0.01', color='blue')
    plt.plot(b3_val, label='Benchmark - Impact 0.01', color='blue', linestyle='dashed', alpha=0.2)
    plt.plot(sl4_val, label='Learner - Impact 0.05', color='purple')
    plt.plot(b4_val, label='Benchmark - Impact 0.05', color='purple', linestyle='dashed', alpha=0.2)
    plt.legend()
    plt.savefig('./images/experiment2_impacts.png')
    plt.clf()

if __name__ == "__main__":
    pass