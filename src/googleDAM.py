'''
Created on 22nd May, 2014
author @ ardhani
'''


class GoogleDAM(object):

    def __init__(self, symbol):
        self.symbol = symbol
        try:
            file_handler = open(symbol+".csv")
            file_content = file_handler.read()
            file_handler.close()
            data = file_content.split('\n')
            data = data[:-1]
            self.date_       = []
            self.close      = []
            self.close_map  = []
            self.high       = []
            self.high_map   = []
            self.low        = []
            self.low_map    = []
            self.open_      = []
            self.open_map   = []
            self.volume     = []
            self.volume_map = []
            for each_row in data:
                row = each_row.split(',')
                self.date_.append(int(row[0]))
                self.close.append(float(row[1]))
                self.high.append(float(row[2]))
                self.low.append(float(row[3]))
                self.open_.append(float(row[4]))
                self.volume.append(int(row[5]))
                self.close_map.append({int(row[0]):float(row[1])})
                self.high_map.append({int(row[0]):float(row[2])})
                self.low_map.append({int(row[0]):float(row[3])})
                self.open_map.append({int(row[0]):float(row[4])})
                self.volume_map.append({int(row[0]):int(row[5])})
        except Exception, e:
             print(e)

    def getDateHighValMap(self):
        '''
        '''
        return self.high_map

    def getDateLowValMap(self):
        '''
        '''
        return self.low_map

    def getDateOpenValMap(self):
        '''
        '''
        return self.open_map

    def getDateVolumeValMap(self):
        '''
        '''
        return self.volume_map

    def getDateCloseValMap(self):
        '''
        '''
        return self.close_map

    def getCloseVal(self):
        '''
        '''
        return self.close
