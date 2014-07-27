import sqlite3
import datetime, json
from stock_signals import generateMACDSignals, generateRSISignals


db = "../data/2014_06_26.db"

bse_handler = open("../resources/bom.csv","r")
bse = bse_handler.read().split("\n")[:-1]

nse_handler = open("../resources/nse.csv","r")
nse = nse_handler.read().split("\n")[:-1]

def generateRSIandStore(exchange, symbol):
    con = sqlite3.connect(db)
    cursor = con.cursor()
    query = "select DATE, close from %s_%s order by DATE asc"
    data_query = "select DATE, OPEN, HIGH, LOW, CLOSE, VOLUME  from %s_%s order by DATE asc"
    d  = cursor.execute(query % (exchange.lower(),symbol.replace("-","_")))
    data = d.fetchall()
    all_data = cursor.execute(data_query % (exchange.lower(),symbol.replace("-","_")))
    all_data = all_data.fetchall()
    if not data:
        return
    format_day_time = lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d')
    new_values = [(format_day_time(x), y) for x,y in data]
    closeP = [y for x,y in new_values]
    if not closeP:
        return
    deltas, gain, loss, avg_gain,avg_loss,rs,rsi = generateRSISignals(closeP)
    if len(rsi) == 0:
        return
    dates = [x for x,y in new_values]
    final_list = []
    #final_str = "DATE,CLOSE,DELTA,GAIN,LOSS, AVG GAIN, AVG LOSS, RS, RSI, Signal\n"
    first_row =  list(all_data[0])
    first_row[0] = int(first_row[0])
    first_row.append(rsi[0])
    first_row.append('')
    final_list.append(first_row)
    prevValue = rsi[0]
    for count in range(1, len(dates)):
        temp_list = list(all_data[count])
        temp_list[0] = int(temp_list[0])
        temp_list.append(rsi[count])
        #final_str = final_str+""+str(dates[count]) + "," +str(closeP[count])+","+str(deltas[count])+","+str(gain[count])+","+str(loss[count])+","+str(avg_gain[count])+","+str(avg_loss[count])+","+str(rs[count])+","+str(rsi[count])+","
        currentVale = rsi[count]

        if(prevValue < 70 and currentVale >= 70):
            temp_list.append('Sell')
        if prevValue > 30 and currentVale <= 30:
            temp_list.append("Buy")
        else:
            temp_list.append("")

        prevValue = currentVale
        final_list.append(temp_list)

    f = open("../data/json_rsi_"+exchange.lower()+"_"+symbol+".txt","w") 
    #f.write(final_str)
    json.dump(final_list, f)
    cursor.close()


for symbol in nse:
    generateRSIandStore('NSE',symbol)
    print("generated signal for %s of %s") %('NSE', symbol)

for symbol in bse:
    generateRSIandStore('BSE',symbol)
    print("generated signal for %s of %s") %('BSE', symbol)

