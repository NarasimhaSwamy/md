from googleDAM import GoogleDAM
from finFunc   import FinancialFunctions


def generateMACDSignals(symbol, closeP):
    finFunction = FinancialFunctions()
    ema_slow, ema_fast, macd = finFunction.MACD(closeP)
    ema9  = finFunction.moving_average(macd, 9)
    prevValue = macd[0] - ema9[0]
    signals = []
    signals.append('')
    for count in range(1, len(ema9)):
        currentValue = macd[count] - ema9[count]
        if(currentValue > prevValue and currentValue > 0 and prevValue < 0):
            signals.append('BUY')
        elif(currentValue < prevValue and currentValue < 0 and prevValue > 0):
            signals.append('Sell')
        else:
            signals.append('')
        prevValue = currentValue

    return ema_slow, ema_fast, macd, ema9, signals

def generateBollingerBands(closeP):
    finFunction = FinancialFunctions()
    return finFunction.BollingerBands(closeP)

def generateRSISignals(closeP):
    finFunction = FinancialFunctions()
    rsi = finFunction.relative_strength_index(closeP)
    return rsi
