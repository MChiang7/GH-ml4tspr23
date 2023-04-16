import pandas as pd
import datetime as dt
from util import get_data
import QLearner
import indicators
import marketsimcode as mkt_sim


class StrategyLearner(object):

    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        self.impact = impact
        self.commission = commission
        self.verbose = verbose
        self.learner = QLearner.QLearner(num_states=233344,
                                         num_actions=3,
                                         alpha=0.2,
                                         gamma=0.9,
                                         rar=0.5,
                                         radr=0.99,
                                         dyna=0,
                                         verbose=False)

    def author(self):
        return 'mchiang30'

    def add_evidence(self, symbol='JPM',
                     sd=dt.datetime(2008, 1, 1),
                     ed=dt.datetime(2009, 1, 1),
                     sv=10000):

        goldenx, macd, momentum, bb, ema = discretize(sd, ed, symbol)

        prices = get_data([[symbol][0]], pd.date_range(sd, ed))[[[symbol][0]]].ffill().bfill()
        trades = get_data([[symbol][0]], pd.date_range(sd, ed))[['SPY']].rename(columns={'SPY':[symbol][0]})
        normalized_prices = (prices[symbol] / prices[symbol][0]).to_frame()

        for col in trades.columns:
            trades[col].values[:] = 0

        temp_cash = sv
        temp_pos = 0

        for i in range(1, len(prices.index)):
            s_prime = get_state(temp_pos, goldenx.loc[prices.index[i]], macd.loc[prices.index[i]], momentum.loc[prices.index[i]], bb.loc[prices.index[i]], ema.loc[prices.index[i]])

            if temp_pos == 0:
                rsign = 0
            elif temp_pos > 0:
                rsign = 1
            else:
                rsign = -1

            r = (((prices.loc[prices.index[i]].loc[symbol] * (1 - self.impact * rsign)) / prices.loc[prices.index[i - 1]].loc[symbol]) - 1) * rsign

            temp_action = self.learner.query(s_prime, r)
            if temp_action == 1:
                asign = 0
            elif temp_action == 0:
                asign = -1
            else:
                asign = 1

            temp_trade = asign * 1000 - temp_pos
            temp_pos += temp_trade
            trades.loc[prices.index[i]].loc[symbol] = temp_trade

            if temp_trade > 0:
                isign = 1
            else:
                isign = -1

            temp_cash += -prices.loc[prices.index[i]].loc[symbol] * (1 + self.impact * isign) * temp_trade

    def testPolicy(self, symbol='JPM',
                   sd=dt.datetime(2009, 1, 1),
                   ed=dt.datetime(2010, 1, 1),
                   sv=10000):

        self.learner.rar = 0

        goldenx, macd, momentum, bb, ema = discretize(sd, ed, symbol)


        prices = get_data([[symbol][0]], pd.date_range(sd, ed))[[[symbol][0]]].ffill().bfill()
        trades = get_data([[symbol][0]], pd.date_range(sd, ed))[['SPY']].rename(columns={'SPY':[symbol][0]})
        normalized_prices = (prices[symbol] / prices[symbol][0]).to_frame()

        for col in trades.columns:
            trades[col].values[:] = 0

        temp_pos = 0

        for i in range(1, len(prices.index)):
            s_prime = get_state(temp_pos, goldenx.loc[prices.index[i]], macd.loc[prices.index[i]], momentum.loc[prices.index[i]], bb.loc[prices.index[i]], ema.loc[prices.index[i]])

            temp_action = self.learner.querysetstate(s_prime)
            if temp_action == 1:
                asign = 0
            elif temp_action == 0:
                asign = -1
            else:
                asign = 1

            temp_trade = asign * 1000 - temp_pos
            temp_pos += temp_trade
            trades.loc[prices.index[i]].loc[symbol] = temp_trade

        return trades


def discretize(sd, ed, symbol):
    prices = get_data([[symbol][0]], pd.date_range(sd, ed))[[[symbol][0]]].ffill().bfill()
    normalized_prices = prices[symbol] / prices[symbol][0]

    gx_s, gx_l = indicators.goldenx(sd, ed, symbol, window_size=20, gen_plot=False)
    discretized_goldenx = gx_s.copy()
    discretized_goldenx[gx_s > gx_l] = 0
    discretized_goldenx[gx_s < gx_l] = 1
    discretized_goldenx[gx_s == gx_l] = 2
    discretized_goldenx[gx_s.isnull() | gx_l.isnull()] = 3

    macd_raw, macd_signal = indicators.macd(sd, ed, symbol)
    discretized_macd = macd_raw.copy()
    discretized_macd[macd_raw > macd_signal] = 0
    discretized_macd[macd_raw < macd_signal] = 1
    discretized_macd[macd_raw == macd_signal] = 2
    discretized_macd[macd_raw.isnull() | macd_signal.isnull()] = 3

    momentum = indicators.momentum(sd, ed, symbol, gen_plot=False)
    discretized_momentum = momentum.copy()
    discretized_momentum[momentum < -0.5] = 0
    discretized_momentum[(momentum >= -0.5) & (momentum <= 0.0)] = 1
    discretized_momentum[(momentum > 0.0) & (momentum <= 0.5)] = 2
    discretized_momentum[momentum.isnull()] = 3

    bb = indicators.bollinger_band(sd, ed, symbol, window_size=20, gen_plot=False)
    discretized_bb = bb.copy()
    discretized_bb[bb < -1.0] = 0
    discretized_bb[(bb >= -1.0) & (bb <= 0.0)] = 1
    discretized_bb[(bb > 0.0) & (bb <= 1.0)] = 2
    discretized_bb[bb > 1.0] = 3
    discretized_bb[bb.isnull()] = 4

    ema = indicators.exponential_moving_average(sd, ed, symbol, window_size=20, gen_plot=False)
    discretized_ema = ema.copy()
    discretized_ema[ema < normalized_prices] = 0
    discretized_ema[ema > normalized_prices] = 1
    discretized_ema[ema == normalized_prices] = 2
    discretized_ema[ema.isnull()] = 3

    return discretized_goldenx, discretized_macd, discretized_momentum, discretized_bb, discretized_ema


def get_state(position, golden_x, macd, momentum, bb, ema):
    string_state = '0'
    if position == 0:
        string_state += '1'
    elif position == 1000:
        string_state += '2'
    string_state += golden_x.astype(int).astype(str) + macd.astype(int).astype(str) + momentum.astype(int).astype(str) + bb.astype(int).astype(str) + ema.astype(int).astype(str)
    #string_state += golden_x.astype(int).astype(str) + macd.astype(int).astype(str) + bb.astype(int).astype(str)
    return int(string_state)


def benchmark(symbol, sd, ed, sv, commission, impact):
    trades = get_data(['SPY'], pd.date_range(sd, ed)).rename(columns={'SPY': symbol})
    for col in trades.columns:
        trades[col].values[:] = 0
    trades.loc[trades.index[0]] = 1000
    val = mkt_sim.compute_portvals(trades, start_val=sv, commission=commission, impact=impact)
    return val

if __name__ == "__main__":
    pass