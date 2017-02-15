# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 10:12:46 2017

@author: jkr
"""

import pandas as pd
import numpy as np
from threading import Thread


weights = {'ema_200':0.30,
           'ror_125':0.30,
           'ema_050':0.15,
           'ror_020':0.15,
           'rsi_014':0.05,
           'ppo_slope_003':0.05 }

def rsi(c):
    r        = pd.Series(c).pct_change()
    UP_sum   = r[r>0].sum()
    DOWN_sum = r[r<=0].sum()
    RS       = -UP_sum/(DOWN_sum + 1e-8)

    return 100.*( 1. - 1./(1+RS) )
    
def ppo_slope(c):
    #Percentage Price Oscillator (PPO): {(12-day EMA - 26-day EMA)/26-day EMA} x 100
    _ppo = (c.ewm(span=12).mean()/c.ewm(span=26).mean() - 1)*100.
    #Signal Line: 9-day EMA of PPO
    sig = _ppo.ewm(span=9).mean()
    #PPO Histogram: PPO - Signal Line
    hist  = _ppo - sig
    slope = hist.diff(3)/3.
    
    slope  = slope.clip(lower=-1, upper=1)
    slope += 1.
    slope *= 50

    return slope
           
def sctr(AC_vals, res_pl=None):
    s = {}
    AC = pd.Series(data=AC_vals)
    # SLOW
    pct_above_ema = (AC / AC.ewm(span=200).mean() - 1)*100.
    s['ema_200'] = pct_above_ema
    s['ror_125'] = AC.pct_change(125)*100.
    # MEDIUM
    pct_above_ema = (AC / AC.ewm(span=50).mean() - 1)*100.
    s['ema_050'] = pct_above_ema
    s['ror_020'] = AC.pct_change(20)*100.
    # FAST
    s['rsi_014']          = AC*np.nan
    s['rsi_014'].iloc[-1] = rsi(AC.iloc[-15:].values)
    s['ppo_slope_003'] = ppo_slope(AC)
    # results
    
    s['sctr'] = 0
    
    for k, v in weights.iteritems():
        s[k]*=v
        s['sctr'] += s[k]
    
    df = pd.DataFrame().from_dict(s)
    df.dropna(axis=0, inplace=True)

    sigs = df.iloc[-1]
    
    if res_pl is not None:
        res_pl['sigs']= sigs
    else:
        return sigs



from util import fetches

def rank_from_list(date, ticker_list, stock_data=[]):
    N_days = 210

    if len(stock_data)==0:
        stock_data  = []
        for db, tick in ticker_list:
            data = fetches.get_csv(tick, db, date)
            if date in data.index:
                stock_data += [ (data, tick) ]
            elif len(data.index)>0:
                print 'Date {:%Y-%m-%d} not found in dataframe for {:s} [{:%Y-%m-%d} - {:%Y-%m-%d}]'.format(date, tick, data.index[0], data.index[-1])
            else:
                print 'Date {:%Y-%m-%d} not found in dataframe for {:s} which has no data'.format(date, tick)

    date = stock_data[0][0].index[stock_data[0][0].index <= date][-1]
    
    partial_data = []
    for stock, tick in stock_data:
        has_data  = len(stock.loc[:date].ix[-N_days:])==N_days
        is_recent = date in stock.index
        if has_data and is_recent:
            partial_data += [ (stock.loc[:date].iloc[-N_days:], tick) ]

    print 'Using {:.0%} of tickers...'.format(len(partial_data)*1.0/len(ticker_list))
    
    job_list = []
    pl_list  = []
    
    for stock, tick in partial_data:
        res_pl = {'tick':tick, 'date':date}
        k = [k for k in ['Adj. Close','Adjusted Close'] if k in stock.columns][0]
        if len(k)==0:
            print stock.columns
#        thread = Thread(target = sctr, args=(stock[k].values, res_pl))
#        job_list.append(thread)
        sigs          = sctr(stock[k].values)
        res_pl = {'tick':tick, 'date':date, 'sigs':sigs}
        pl_list.append(res_pl)
    
#    for j in job_list:
#        j.start()
#    # Ensure all of the threads have finished
#    for i, j in enumerate(job_list):
#        j.join()
    
    return sorted([pl for pl in pl_list if len(pl['sigs'])>0], key=lambda d: -d['sigs']['sctr']), stock_data

if __name__=='__main__':
    import datetime
    import matplotlib.pyplot as plt
    date = datetime.datetime(2017,1,10)
    ticker_file  = '/home/jkr/Downloads/SP500.csv'
    ticker_df    = pd.read_csv(ticker_file)
    ticker_list  = [ code.split('/') for code in ticker_df.premium_code.values ]
#    ticker_list  = [ ('YAHOO', tick) for tick in ticker_df.ticker ]

    rank, stockdata = rank_from_list(date, ticker_list)
    plt.clf()

    print ' '*20+'{:%d/%m %Y}\n'.format(date)
    for i,t in enumerate(rank[:9]):

        db, tick = ticker_df[ticker_df.ticker==t['tick']].premium_code.values[0].split('/')
        data = fetches.get_csv(tick, db, date)
        data = data.loc[:date]
        sigs = sctr(data['Adj. Close'].iloc[-300:], res_pl=None)

        descr = ticker_df[ticker_df.ticker==t['tick']].name.values[0]
        print "{rank:3d} {tick:10s} {score:8.2f}  {descr:s} ({score_here:.2f})".format(rank=i+1, 
                                                                    tick=t['tick'], 
                                                                    score=t['sigs']['sctr'], 
                                                                    descr=descr,
                                                                    score_here=sigs['sctr'])

        if i==0:
            ax_0 = plt.subplot(3,3,i+1)
            ax = ax_0
        else:
            ax = plt.subplot(3,3,i+1, sharex=ax_0, sharey=ax_0)

        price = data['Adj. Close'].iloc[-200:]
        price /= price[0]
        price -= 1.
        price.plot()
        ax.set_title(tick)
        ax.xaxis.set_major_formatter(plt.NullFormatter())
#        ax.yaxis.set_major_formatter(plt.NullFormatter())
        
        score = sctr(price, res_pl=None)














