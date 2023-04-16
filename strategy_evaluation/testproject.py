import datetime as dt
import random
import experiment1
import ManualStrategy

def author():
    return 'mchiang30'

def report():
    random.seed(42)

    ManualStrategy.report(symbol='JPM',
                sd_in=dt.datetime(2008, 1, 1),
                ed_in=dt.datetime(2009, 12, 31),
                sd_out=dt.datetime(2010, 1, 1),
                ed_out=dt.datetime(2011, 12, 31),
                sv=100000,
                commission=9.95,
                impact=0.005)

    experiment1.output(symbol='JPM',
                sd_in=dt.datetime(2008, 1, 1),
                ed_in=dt.datetime(2009, 12, 31),
                sd_out=dt.datetime(2010, 1, 1),
                ed_out=dt.datetime(2011, 12, 31),
                sv=100000,
                commission=9.95,
                impact=0.005,
                gen_plots=True,
                stats=True)

if __name__ == '__main__':
    report()