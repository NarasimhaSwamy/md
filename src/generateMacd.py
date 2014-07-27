import sqlite3
import datetime, json

from stock_signals import generateMACDSignals

db = "../data/2014_06_27.db"

bse_handler = open("../resources/bom.csv","r")
bse = bse_handler.read().split("\n")[:-1]

nse_handler = open("../resources/nse.csv","r")
nse = nse_handler.read().split("\n")[:-1]

def generateMACDandStore(exchange, symbol):
    con = sqlite3.connect(db)
    cursor = con.cursor()
    query = "select DATE, close from %s_%s order by DATE asc"
    data_query = "select DATE, OPEN, HIGH, LOW, CLOSE, VOLUME  from %s_%s order by DATE asc"
    d  = cursor.execute(query % (exchange.lower(),symbol.replace("-","_")))    
    data = d.fetchall()
    all_data  = cursor.execute(data_query % (exchange.lower(),symbol.replace("-","_")))
    all_data = all_data.fetchall()
    if not data:
        return
    format_day_time = lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')
    new_values = [(format_day_time(x), y) for x,y in data]
    closeP = [y for x,y in new_values]
    results = generateMACDSignals('',closeP)
    a = list(results)
    dates = [x for x,y in new_values]
    a.append(dates)
    emas = a[0]
    emaf = a[1]
    macd = a[2]
    ema9 = a[3]
    signals = a[4]
    final_list = []
    
    for count in range(len(dates)):
        temp_list = list(all_data[count])
        temp_list[0] = int(temp_list[0])
        temp_list.append(macd[count]) 
        temp_list.append(ema9[count]) 
        temp_list.append(signals[count])
        final_list.append(temp_list)

    with open("../data/json_macd_"+exchange.lower()+"_"+symbol+".txt","w") as f:
    #print("==================================================================>")
      json.dump(final_list, f)
    print("==================================================================>>>>")
    #f.write(final_str)
    f.close()
    cursor.close()

for symbol in nse:
    generateMACDandStore('NSE', symbol)
    print("generated signal for %s of %s") %('NSE', symbol)

for symbol in bse:
    generateMACDandStore('BSE', symbol)
    print("generated signal for %s of %s") %('BSE', symbol)

