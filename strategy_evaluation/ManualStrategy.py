import pandas as pd
import matplotlib.pyplot as plt
import marketsimcode as mkt_sim
import datetime as dt
from util import get_data
from strategy_evaluation import indicators


class ManualStrategy(object):
    def __init__(self):
        pass

    def author(self):
        return 'mchiang30'

    def testPolicy(self, symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31)):
        prices = get_data([[symbol][0]], pd.date_range(sd, ed))[[[symbol][0]]].ffill().bfill()
        trades = get_data([[symbol][0]], pd.date_range(sd, ed))[['SPY']].rename(columns={'SPY':[symbol][0]})
        normalized_prices = (prices[symbol] / prices[symbol][0]).to_frame()

        for col in trades.columns:
            trades[col].values[:] = 0

        ema = indicators.exponential_moving_average(sd, ed, symbol, window_size=20, gen_plot=False)
        gx_s, gx_l = indicators.goldenx(sd, ed, symbol, window_size=20, gen_plot=False)
        macd_raw, macd_signal = indicators.macd(sd, ed, symbol, gen_plot=False)
        momentum = indicators.momentum(sd, ed, symbol, gen_plot=False)
        bb = indicators.bollinger_band(sd, ed, symbol, window_size=20, gen_plot=False)

        normalized_gx_s = gx_s[symbol] / gx_s[symbol][0]
        normalized_gx_l = gx_l[symbol] / gx_l[symbol][0]

        temp_action = 0
        temp_pos = 0

        for i in range(len(trades.index)):
            temp_action += 1

            if ema.loc[trades.index[i]].loc[symbol] < normalized_prices.loc[trades.index[i]].loc[symbol]:
                ema_action = 1
            elif ema.loc[trades.index[i]].loc[symbol] > normalized_prices.loc[trades.index[i]].loc[symbol]:
                ema_action = -1
            else:
                ema_action = 0

            if bb.loc[trades.index[i]].loc[symbol] < 0.0:
                bb_action = 1
            elif momentum.loc[trades.index[i]].loc[symbol] > 1:
                bb_action = -1
            else:
                bb_action = 0

            if momentum.loc[trades.index[i]].loc[symbol] < -0.5:
                momentum_action = 1
            elif momentum.loc[trades.index[i]].loc[symbol] > 0.5:
                momentum_action = -1
            else:
                momentum_action = 0

            if macd_signal.loc[trades.index[i]].loc[symbol] < macd_raw.loc[trades.index[i]].loc[symbol]:
                macd_action = 1
            elif macd_signal.loc[trades.index[i]].loc[symbol] > macd_raw.loc[trades.index[i]].loc[symbol]:
                macd_action = -1
            else:
                macd_action = 0

            if normalized_gx_l.loc[trades.index[i]] > normalized_gx_s.loc[trades.index[i]]:
                goldenx_action = -1
            elif normalized_gx_l.loc[trades.index[i]] < normalized_gx_s.loc[trades.index[i]]:
                goldenx_action = 1
            else:
                goldenx_action = 0

            if goldenx_action + macd_action + momentum_action + bb_action + ema_action < 0:
                sign = 1
            elif goldenx_action + macd_action + momentum_action + bb_action + ema_action > 0:
                sign = -1
            else:
                sign = 0

            if temp_action >= 5:
                trades.loc[trades.index[i]].loc[symbol] = (temp_pos - sign * 1000) * -1
                temp_pos += (temp_pos - sign * 1000) * -1
                temp_action = 0

        return trades


def benchmark(symbol, sd, ed, sv, commission, impact):
    trades = get_data(['SPY'], pd.date_range(sd, ed)).rename(columns={'SPY': symbol})
    for col in trades.columns:
        trades[col].values[:] = 0
    trades.loc[trades.index[0]] = 1000
    val = mkt_sim.compute_portvals(trades, start_val=sv, commission=commission, impact=impact)
    return val

def gen_plot(manual_val, benchmark_val, short_entries, long_entries, sample, symbol):
    pd.plotting.register_matplotlib_converters()

    plt.figure(figsize=(14, 8))
    plt.title('Manual Strategy vs Benchmark - {} ({})'.format(sample, symbol))
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=25)
    plt.grid()
    plt.plot(manual_val, label='Manual Strategy', color='red')
    plt.plot(benchmark_val, label='Benchmark', color='purple')
    for i in long_entries:
        plt.axvline(i, color="blue")
    for i in short_entries:
        plt.axvline(i, color="black")
    plt.legend()
    plt.savefig("./images/manual_{}.png".format(sample))
    plt.clf()

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

    return short_entries, long_entries

def report(symbol='JPM',
                sd_in=dt.datetime(2008,1,1),
                ed_in=dt.datetime(2009,12,31),
                sd_out=dt.datetime(2010, 1, 1),
                ed_out=dt.datetime(2011, 12, 31),
                sv=100000,
                commission=9.95,
                impact=0.005):

    benchmark_val = benchmark(symbol, sd_in, ed_in, sv, commission, impact)
    trades = ManualStrategy().testPolicy(symbol, sd=sd_in, ed=ed_in)
    manual_val = mkt_sim.compute_portvals(trades, sv, commission=commission, impact=impact)

    benchmark_val['value'] = benchmark_val['value'] / benchmark_val['value'][0]
    manual_val['value'] = manual_val['value'] / manual_val['value'][0]

    short_entries, long_entries = entries(trades, symbol)

    gen_plot(manual_val, benchmark_val, short_entries, long_entries, 'In Sample', symbol)

    benchmark_val = benchmark(symbol, sd_out, ed_out, sv, commission, impact)
    trades = ManualStrategy().testPolicy(symbol, sd=sd_out, ed=ed_out)
    manual_val = mkt_sim.compute_portvals(trades, sv, commission=commission, impact=impact)

    benchmark_val['value'] = benchmark_val['value'] / benchmark_val['value'][0]
    manual_val['value'] = manual_val['value'] / manual_val['value'][0]

    short_entries, long_entries = entries(trades, symbol)

    gen_plot(manual_val, benchmark_val, short_entries, long_entries, 'Out Sample', symbol)

if __name__ == "__main__":
    pass