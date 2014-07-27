from googleDAM import GoogleDAM
from finFunc   import FinancialFunctions


def generateMACDSignals(symbol, closeP):
    finFunction = FinancialFunctions()
    ema_slow, ema_fast, macd = finFunction.MACD(closeP)
    ema9  = finFunction.expMovingAverage(macd, 9)
    return closeP, ema_slow, ema_fast, macd, ema9 
