from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import yfinance as yf

import BLStrategy.BLMainStrategy as bs
import BLNetwork.BLMailTip as bm
import asyncio




if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(bs.BLBigFishStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '../datas/orcl-1995-2014.txt')
  

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,  
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values before this date
    todate=datetime.datetime(2000, 12, 31),
    # Do not pass values after this date
    reverse=False)
    
    #data = bt.feeds.PandasData(dataname=yf.download('AAPL', '2000-07-06', '2020-07-07', auto_adjust=True))

    #data = bt.feeds.PandasData(dataname=yf.download('AAPL', '2018-07-01', '2021-07-30', auto_adjust=False))
    
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(1000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    asyncio.run(bm.SendMail('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue()))

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()
