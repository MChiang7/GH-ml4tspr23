import TheoreticallyOptimalStrategy
import indicators
import datetime as dt

def author():
    return 'mchiang30'

def test_code():
    tos = TheoreticallyOptimalStrategy.output(100000, dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'JPM', False, True)
    ind = indicators.output(dt.datetime(2008, 1, 1), dt.datetime(2009, 12, 31), 'JPM', True)

if __name__ == '__main__':
    test_code()