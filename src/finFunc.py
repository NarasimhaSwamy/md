'''
created on May 23, 2014
author @ ardhani
'''
import numpy as np


class FinancialFunctions(object):

   def __init__(self):
       pass

   def RSI(self,closeP, n=14):
       deltas = np.diff(closeP)
       deltas.insert(0,0)
       seed = deltas[:n]
       up = seed[seed >=0 ].sum()/n
       down = -seed[seed<0].sum()/n
       rs = up/down
       rsi = np.zeros_like(closeP)
       rsi[:n+1] = 100. - 100./(1.+rs)
        
       for i in range(n+1, len(closeP)):
           delta = deltas[i-1]
           if delta > 0:
               upval = delta
               downval = 0
           else :
               downval = -delta
               upval = 0

           up = (up*(n-1)+upval)/n
           down = (down*(n-1)+downval)/n
           rs = up/down
           rsi[i] = 100. - 100./(1.+rs)

       return rsi

   def BollingerBands(self, close_price, n = 20):
        closeP = np.array(close_price)
        length = len(close_price)
        middleBand    = [0 for i in range(n-1)]
        stdDeviation  = [0 for i in range(n-1)]
        upperBand     = [0 for i in range(n-1)]
        lowerBand     = [0 for i in range(n-1)]
        bandWidth     = [0 for i in range(n-1)]
        for i in range(length - n +1 ):
            middleBand.append(np.average(close_price[i : n + i]))
            stdDeviation.append(np.std(close_price[i : n + i]))
            upperBand.append(middleBand[n-1 + i] + (stdDeviation[n-1 + i] * 2))
            lowerBand.append(middleBand[n-1 + i] - (stdDeviation[n-1 + i] * 2))
            bandWidth.append(upperBand[n-1 + i] - lowerBand[n-1 + i])
        return middleBand, stdDeviation, upperBand, lowerBand, bandWidth

   def expMovingAverage(self, values, window):
       '''
       '''
       weights = np.exp(np.linspace(-1., 0., window))
       weights /= weights.sum()
       a = np.convolve(values, weights, mode='full')[:len(values)]
       a[:window] = a[window]
       return a

   def MACD(self, x, slow=26, fast=12):
       '''
       macd line = 12EMA - 26 EMA
       signal line = 9EMA of macd line
       histogram = macd line -signal line
       '''
       #ema_slow = self.expMovingAverage(x,slow)
       #ema_slow = self.expMovingAverage(x,slow)
       ema_slow = self.moving_average(x,slow)
       ema_fast = self.moving_average(x,fast)
       macd = []
       for i in range(len(ema_slow)):
           val = ema_fast[i] - ema_slow[i]
           macd.append(val)
       return ema_slow, ema_fast, macd

   def moving_average(self, closeP_, n):
       ma = []
       average_limit = n
       sample_arr = closeP_[:n]
       
       for i in range(n):
           ma.append(0)
       if n == 9 :
           n = n + 25
           sample_arr = closeP_[25:n]
           ma = []
           for i in range(n):
               ma.append(0)
       ma[n-1] = sum(sample_arr)/average_limit
       for i in range(n, len(closeP_)):
           ma.append(((closeP_[i]*(2./(average_limit+1)))+(ma[i-1]*(1-(2./(average_limit+1))))))
       return ma

   def relative_strength_index(self, closeP,n=14):
       deltas = list(np.diff(closeP))
       deltas.insert(0,0)
       loss = []
       gain = []
       avg_loss = []
       avg_gain = []
       for i  in range(n):
           loss_value = 0
           gain_value = 0
           delta = deltas[i]
           if delta >=0:
               gain_value = delta
           else:
               loss_value = -delta
           loss.append(loss_value)
           gain.append(gain_value)
           avg_loss.append(0)
           avg_gain.append(0)
          
       delta = deltas[n]
       loss_val = 0 
       gain_val = 0
       if delta>=0:
           gain_val = delta
       else:
           loss_val = -delta
       loss.append(loss_val) 
       gain.append(gain_val)

       avg_gain_val = sum(gain)/n
       avg_loss_val = sum(loss)/n
       avg_loss.append(avg_loss_val)
       avg_gain.append(avg_gain_val)
       rs = avg_gain_val/avg_loss_val
       rsi = np.zeros_like(closeP)
       rs_ = np.zeros_like(closeP)
       rs_[n]  = rs
       rsi[:n+1] = 100. - 100./(1.+rs)
       for i in range(n+1, len(closeP)):
          delta = deltas[i]
          loss_val = 0
          gain_val = 0 
          if delta >=0:
              gain_val = delta
          else:
              loss_val = -delta 
          gain.append(gain_val) 
          loss.append(loss_val) 
          avg_loss.append(((avg_loss[i-1]*(n-1))+loss[i])/n)
          avg_gain.append(((avg_gain[i-1]*(n-1))+gain[i])/n)
          rs = avg_gain[i]/avg_loss[i]
          rs_[i] = rs
          rsi[i] = 100. - 100./(1.+rs)
       return deltas,gain, loss, avg_gain, avg_loss, rs_,rsi

