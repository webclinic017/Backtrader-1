from SimpleMovingAverage import SMAStrategy
import backtrader as bt
import pandas



# modify parameters
filepath = 'data/BID_ASK_EURUSD_Hourly.csv'
# end modify parameters

if __name__ == '__main__':
    # Create cerebro        
    cerebro = bt.Cerebro()
    
    # Load data from IB into cerebro
    # store = bt.stores.IBStore(host='127.0.0.1', port=4001, _debug=True)
    # store = bt.stores.IBStore(host='ec2-52-90-35-26.compute-1.amazonaws.com', port=4002, _debug=True)
    # data = store.getdata(dataname='ES-202006-GLOBEX-USD',
    #                      #sectype='',
    #                      #exch='',
    #                      #curr='',
    #                      #expiry='',
    #                      #strike='',
    #                      #right='',
    #                      historical=True,
    #                      timeframe=bt.TimeFrame.Minutes,
    #                      compression=30,
    #                      fromdate=datetime.datetime(2020, 4, 22),
    #                      todate=datetime.datetime(2020, 5, 23)
    # )

    df = pandas.read_csv(filepath, usecols = ['DateTime', 'Open_Bid', 'High_Bid', 'Low_Bid', 'Close_Bid', 'Open_Ask', 'High_Ask', 'Low_Ask', 'Close_Ask'])
    df.columns = [col_name.lower() for col_name in df.columns]
    df['datetime'] = pandas.to_datetime(df['datetime'])
    df.set_index('datetime')

    data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=2, low=3, close=4)
    # Add second data
    cerebro.adddata(data)              
    # Add minute data 
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=180)
       
    # Add strategy to cerebro
    cerebro.addstrategy(SMAStrategy)
   
    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot(style='candlestick', volume=False)