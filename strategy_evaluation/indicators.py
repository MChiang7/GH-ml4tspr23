import pandas as pd
import datetime as dt
from util import get_data
import matplotlib.pyplot as plt

def author():
    return 'mchiang30'

def exponential_moving_average(sd, ed, symbol, window_size, gen_plot = False):
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(window_size * 2), ed))[[symbol]].ffill().bfill()

    normalized_prices = prices.truncate(before=sd)[symbol] / prices.truncate(before=sd)[symbol][0]
    normalized_ema = prices.ewm(span=window_size, adjust=False).mean().truncate(before=sd)[symbol] / prices.ewm(span=window_size, adjust=False).mean().truncate(before=sd)[symbol][0]

    if gen_plot:
        plt.figure(figsize=(12, 9))
        plt.title('Exponential Moving Average ({} days) for JMP'.format(window_size))
        plt.xlabel('Date')
        plt.xticks(rotation=25)
        plt.xlim([sd, ed])
        plt.ylabel('Normalized Values')

        plt.plot(normalized_prices, label='Price', color='blue')
        plt.plot(normalized_ema, label='EMA ({})'.format(window_size), color='red')

        plt.legend()
        plt.grid()
        plt.savefig('./images/ema.png')
        #plt.show()
        plt.clf()

    return normalized_ema.to_frame()

def bollinger_band(sd, ed, symbol, window_size, gen_plot=False):
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(window_size * 2), ed))[[symbol]].ffill().bfill()
    normalized_prices = prices[symbol] / prices[symbol][0]

    bb_df = pd.DataFrame(index=normalized_prices.index)
    bb_df['Price'] = normalized_prices
    bb_df['Sma ({})'.format(window_size)] = normalized_prices.rolling(window=window_size, center=False).mean()
    bb_df['Upper Band'] = -1 * (-normalized_prices.rolling(window=window_size, center=False).mean() - normalized_prices.rolling(window=window_size, center=False).std() * 2)
    bb_df['Lower Band'] = -1 * (-normalized_prices.rolling(window=window_size, center=False).mean() + normalized_prices.rolling(window=window_size, center=False).std() * 2)
    bb_df['BB%({})'.format(window_size)] = (normalized_prices - bb_df['Lower Band']) / (bb_df['Upper Band'] - bb_df['Lower Band'])


    if gen_plot:
        bb_df[['Price', 'Sma ({})'.format(window_size), 'Upper Band', 'Lower Band']].plot(figsize=(12, 9))

        plt.title('Bollinger Band ({} Days) for JPM'.format(window_size))
        plt.xlabel('Dates')
        plt.xticks(rotation=25)
        plt.xlim([sd, ed])
        plt.ylabel('Normalized Values')

        plt.legend()
        plt.grid()
        plt.savefig('./images/bb.png')
        #plt.show()
        plt.clf()

        bb_df[['BB%({})'.format(window_size)]].plot(figsize=(12, 9))
        plt.axhline(y=1, color='red', linestyle='dashed')
        plt.axhline(y=-0, color='green', linestyle='dashed')

        plt.title('Bollinger Band % ({} Days) for JPM'.format(window_size))
        plt.xlabel('Dates')
        plt.xticks(rotation=25)
        plt.xlim([sd, ed])
        plt.ylabel('Bollinger Band %')

        plt.legend()
        plt.grid()
        plt.savefig('./images/bb%.png')
        #plt.show()
        plt.clf()
    bollinger_df = bb_df['BB%({})'.format(window_size)].to_frame()
    bollinger_df.rename(columns={'BB%({})'.format(window_size): symbol}, inplace=True)
    return bollinger_df

def momentum(sd, ed, symbol, window_size=30, gen_plot=False):
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(window_size * 2), ed))[[symbol]].ffill().bfill()
    normalized_prices = prices[symbol] / prices[symbol][0]

    momentum = pd.DataFrame(0, index=normalized_prices.index, columns=[symbol])
    momentum[symbol] = normalized_prices.diff(window_size) / normalized_prices.shift(window_size)

    if gen_plot:
        momentum.plot(figsize=(12, 9))
        plt.axhline(y=0.1, color='red', linestyle='dashed')
        plt.axhline(y=-0.1, color='green', linestyle='dashed')

        plt.title('Momentum ({} Days) for JPM'.format(window_size))
        plt.xlabel('Dates')
        plt.xticks(rotation=25)
        plt.xlim([sd, ed])
        plt.ylabel('Momentum')

        plt.legend()
        plt.grid()
        plt.savefig('./images/momentum.png')
        # plt.show()
        plt.clf()

    return momentum

def macd(sd, ed, symbol, gen_plot=False):
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(26 * 2), ed))[[symbol]].ffill().bfill()
    normalized_prices = prices[symbol] / prices[symbol][0]

    macd_r = (normalized_prices.ewm(span=12, adjust=False).mean() - normalized_prices.ewm(span=26, adjust=False).mean()).truncate(before=sd)
    macd_s = (normalized_prices.ewm(span=12, adjust=False).mean() - normalized_prices.ewm(span=26, adjust=False).mean()).ewm(span=9,adjust=False).mean().truncate(before=sd)

    if gen_plot:
        plt.figure(figsize=(12, 9))
        plt.title('EMA (12 and 26 days)')
        plt.xlabel('Dates')
        plt.xticks(rotation=25)
        plt.xlim([sd, ed])
        plt.ylabel('Normalized Price')

        plt.plot(prices.ewm(span=12, adjust=False).mean().truncate(before=sd)[symbol] /
                 prices.ewm(span=12, adjust=False).mean().truncate(before=sd)[symbol][0], label='EMA (12)',
                 color='green')
        plt.plot(prices.ewm(span=26, adjust=False).mean().truncate(before=sd)[symbol] /
                 prices.ewm(span=26, adjust=False).mean().truncate(before=sd)[symbol][0], label='EMA (26)', color='red')
        plt.plot(prices.truncate(before=sd)[symbol] / prices.truncate(before=sd)[symbol][0], label='Price',
                 color='blue')

        plt.legend()
        plt.grid()
        plt.savefig('./images/ema1226.png')
        # plt.show()
        plt.clf()

        plt.figure(figsize=(12, 9))
        plt.title('MACD Signal (12 and 26 days)')
        plt.xlabel('Dates')
        plt.xticks(rotation=25)
        plt.xlim([sd, ed])
        plt.ylabel('MACD Value')

        plt.plot(macd_r, label='MACD', color='green')
        plt.plot(macd_s, label='MACD Signal', color='red')

        plt.legend()
        plt.grid()
        plt.savefig('./images/macd_sig.png')
        # plt.show()
        plt.clf()

    return macd_r.to_frame(), macd_s.to_frame()

def goldenx(sd, ed, symbol, window_size=20, gen_plot=False):
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(50 * 2), ed))[[symbol]].ffill().bfill()
    normalized_prices = prices[symbol] / prices[symbol][0]

    gx_s = normalized_prices.rolling(window=window_size, center=False).mean()
    gx_l = normalized_prices.rolling(window=window_size+30, center=False).mean()

    if gen_plot:
        plt.figure(figsize=(12, 9))
        plt.title('Golden Cross (SMA 20 and 50) for JPM')
        plt.xlabel('Dates')
        plt.xticks(rotation=25)
        plt.xlim([sd, ed])
        plt.ylabel('Normalized Price')

        plt.plot(gx_s, label='SMA (20)', color='orange')
        plt.plot(gx_l, label='SMA (50)', color='green')
        plt.plot(prices, label='Price')

        plt.legend()
        plt.grid()
        plt.savefig('./images/goldenx.png')
        #plt.show()
        plt.clf()

    return gx_s.to_frame(), gx_l.to_frame()

if __name__ == "__main__":
	pass