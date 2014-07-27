import sqlite3
import datetime, json

from stock_signals import generateBollingerBands

db = "../data/2014_06_26.db"

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
    results = generateBollingerBands(closeP)
    a = list(results)
    dates = [x for x,y in new_values]
    final_str = "Date, OPEN, HIGH, LOW, CLOSE, VOLUME, Middle Band, Standard Deviations, Upper Band, Lower Band, Band Width\n"
    print(len(all_data))
    print(len(a[0]))
    for i in range(len(list(all_data))):
        temp_list = list(all_data[i])
        final_str = final_str + str(int(temp_list[0])) + ","+ str(temp_list[1]) + "," + str(temp_list[2]) + "," + str(temp_list[3]) + "," + str(temp_list[4]) + "," + str(temp_list[5]) + "," + str(a[0][i]) + "," + str(a[1][i]) + "," + str(a[2][i]) + "," + str(a[3][i]) + "," + str(a[4][i]) + "\n"
    f = open("../data/bb_"+exchange.lower()+"_"+symbol+".csv","w")
    f.write(final_str)
    f.close()
    cursor.close()

for symbol in nse:
    generateMACDandStore('NSE', symbol)
    print("generated signal for %s of %s") %('NSE', symbol)

for symbol in bse:
    generateMACDandStore('BSE', symbol)
    print("generated signal for %s of %s") %('BSE', symbol)

