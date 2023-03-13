import pandas as pd
import datetime as dt
from util import get_data
import matplotlib.pyplot as plt

def author():
    return 'mchiang30'

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

    return bb_df

def exponential_moving_average(sd, ed, symbol, window_size, gen_plot = False):
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(window_size * 2), ed))[[symbol]].ffill().bfill()

    ema_df = prices.ewm(span=window_size, adjust=False).mean().truncate(before=sd)

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
        plt.plot(normalized_ema, label='{} days EMA'.format(window_size), color='red')

        plt.legend()
        plt.grid()
        plt.savefig('./images/ema.png')
        #plt.show()
        plt.clf()

    return normalized_ema

def momentum(sd, ed, symbol, window_size, gen_plot=False):
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(window_size * 2), ed))[[symbol]].ffill().bfill()
    normalized_prices = prices[symbol] / prices[symbol][0]

    momentum = pd.DataFrame(0, index=normalized_prices.index, columns=['Momentum'])
    momentum['Momentum'] = normalized_prices.diff(window_size) / normalized_prices.shift(window_size)

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
        #plt.show()
        plt.clf()

    return momentum

def macd(sd, ed, symbol, gen_plot=False):
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(26 * 2), ed))[[symbol]].ffill().bfill()

    macd_r = prices.ewm(span=12, adjust=False).mean() - prices.ewm(span=26, adjust=False).mean().truncate(before=sd)
    macd_s = prices.ewm(span=12, adjust=False).mean() - prices.ewm(span=26, adjust=False).mean().ewm(span=9, adjust=False).mean().truncate(before=sd)

    if gen_plot:
        plt.figure(figsize=(12, 9))
        plt.title('EMA (12 and 26 days)')
        plt.xlabel('Dates')
        plt.xticks(rotation=25)
        plt.xlim([sd, ed])
        plt.ylabel('Normalized Price')

        plt.plot(prices.ewm(span=12, adjust=False).mean().truncate(before=sd)[symbol] / prices.ewm(span=12, adjust=False).mean().truncate(before=sd)[symbol][0], label='EMA (12)', color='green')
        plt.plot(prices.ewm(span=26, adjust=False).mean().truncate(before=sd)[symbol] / prices.ewm(span=26, adjust=False).mean().truncate(before=sd)[symbol][0], label='EMA (26)', color='red')
        plt.plot(prices.truncate(before=sd)[symbol] / prices.truncate(before=sd)[symbol][0], label='Price', color='blue')

        plt.legend()
        plt.grid()
        plt.savefig('./images/ema1226.png')
        #plt.show()
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
        #plt.show()
        plt.clf()

    return macd_r, macd_s

def golden_cross(sd, ed, symbol, gen_plot=False):
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(50 * 2), ed))[[symbol]].ffill().bfill()
    normalized_prices = prices[symbol] / prices[symbol][0]

    sma20 = normalized_prices.rolling(window=20, center=False).mean()
    sma50 = normalized_prices.rolling(window=50, center=False).mean()

    if gen_plot:
        plt.figure(figsize=(12, 9))
        plt.title('Golden Cross (SMA 20 and 50) for JPM')
        plt.xlabel('Dates')
        plt.xticks(rotation=25)
        plt.xlim([sd, ed])
        plt.ylabel('Normalied Price')

        plt.plot(sma20, label='SMA (20)', color='orange')
        plt.plot(sma50, label='SMA (50)', color='green')
        plt.plot(normalized_prices, label='Price')

        plt.legend()
        plt.grid()
        plt.savefig('./images/goldenx.png')
        #plt.show()
        plt.clf()

'''
def commodity_channel_index(sd, ed, symbol, gen_plot=False):
    prices_high = get_data([symbol], pd.date_range(sd - dt.timedelta(20 * 2), ed), colname='High')[[symbol]].ffill().bfill()
    prices_low = get_data([symbol], pd.date_range(sd - dt.timedelta(20 * 2), ed), colname='Low')[[symbol]].ffill().bfill()
    prices_close = get_data([symbol], pd.date_range(sd - dt.timedelta(20 * 2), ed), colname='Close')[[symbol]].ffill().bfill()
    prices = get_data([symbol], pd.date_range(sd - dt.timedelta(20 * 2), ed))[[symbol]].ffill().bfill()

    adj_ratio = prices / prices_close
    prices_high *= adj_ratio
    prices_low *= adj_ratio

    typical_price = (prices + prices_high + prices_low) / 3
    normalized_tp = typical_price[symbol] / typical_price[symbol][0]

    normalized_prices = prices[symbol] / prices[symbol][0]

    cci = (typical_price - typical_price.rolling(window=20, center=False).mean()) / (0.015 * typical_price.mad())
    normalized_cci = (normalized_tp - normalized_tp.rolling(window=20, center=False).mean()) / (0.015 * normalized_tp.mad())

    if gen_plot:
        plt.figure(figsize=(12, 9))
        plt.title('CCI for JPM (using SMA 20)')
        plt.xlabel('Dates')
        plt.xticks(rotation=25)
        plt.xlim([sd, ed])
        plt.ylabel('CCI')

        plt.plot(cci, label='CCI')
        #plt.plot(normalized_cci, label='Normalized CCI')

        plt.legend()
        plt.grid()
        plt.savefig('./images/cci.png')
        #plt.show()
        plt.clf()

    return cci
'''

def output(sd, ed, symbol, gen_plot=False):
    bollinger_band(sd, ed, symbol, window_size=20, gen_plot=gen_plot)
    exponential_moving_average(sd, ed, symbol, window_size=20, gen_plot=gen_plot)
    momentum(sd, ed, symbol, window_size=10, gen_plot=gen_plot)
    macd(sd, ed, symbol, gen_plot=True)
    #commodity_channel_index(sd, ed, symbol, gen_plot=True)
    golden_cross(sd, ed, symbol, gen_plot=True)

if __name__ == '__main__':
    pass