import urllib2 

class GoogleFinance(object):

    def __init__(self, symbol, exchange):
        """
        Consutructor for GoogleFinance. 
        Here 'symbol' is optional.
        """
        self.symbol   = symbol
        self.exchange = exchange

    def __requestUrl__(self, symbol, exchange, interval, period):
        """
        Prepares the url required for fetching the data from google.
        """
        url = 'https://www.google.com/finance/getprices?q=%s&x=%s&i=%s&p=%s&f=d,c,v,o,h,l' %(symbol, exchange, interval, period)
        return url

    def getQuote(self, interval=61, period="1d"):
        """
        getQuote method fetches the quotes of a symbol for the given amount 
        of time with a given interval.
        """
        url = self.__requestUrl__(self.symbol, self.exchange, interval, period)
        try:
            data = urllib2.urlopen(url).read()
            data = data.split("\n")
            data = data[7:-1]
            if  data:
                for i  in range(len(data)):
                    data[i] = data[i][1:]
                return data
            else:
                return []
        except Exception, err:
            print(err)

    def writeQuoteToFile(self, symbol=None, interval=61, period="15m"):
        """
        """
        if self.symbol or symbol:
            if not self.symbol:
                self.symbol = symbol
        else:
            raise TypeError("symbol can't be null")

        lastIndex = self.__getLastIndex()
        data = self.getQuote(self.symbol, interval, period)
        file_handler = open(self.symbol+".csv", "a")
        for row in data:
            rowValues = row.split(',')
            index = int(rowValues[0])
            if index > lastIndex:
                file_handler.write(row+'\n')
        file_handler.close()
