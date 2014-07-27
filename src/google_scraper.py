'''
    /usr/bin/python
'''

import urllib2
import sqlite3
import datetime

from googleFinance import GoogleFinance

_db_name = str(datetime.date.today()).replace("-","_")

bse_handler = open("../resources/bom.csv","r")
bse = bse_handler.read().split("\n")[:-1]

nse_handler = open("../resources/nse.csv","r")
nse = nse_handler.read().split("\n")[:-1]




def store_data_to_db(exchange, symbol, db_name):
    google = GoogleFinance(symbol, exchange)
    data = google.getQuote()
    if not data:
        return
    conn =  sqlite3.connect("../data/"+_db_name+".db")
    print("storing data of %s:%s") %(exchange, symbol)
    cursor = conn.cursor()
    select_query = "select DATE from %s_%s order by DATE desc limit 1" % (exchange.lower(), symbol.replace("-","_"))
    d = cursor.execute(select_query)
    last_index = d.fetchone()
    if last_index:
        last_index = int(last_index[0])
        for row in data:
            rowValues = row.split(',')
            index = int(rowValues[0])
            if index >= last_index:
                index = data.index(row)
                data = data[index:]

    values = str(tuple(data[0].split(",")))
    for row in data[1:]:
        values = values + ","+str(tuple(row.split(",")))

    query = "insert into %s_%s values %s" % (exchange.lower(),symbol.replace("-","_"),values)
    cursor.execute(query)
    conn.commit()


for symbol in nse:
    store_data_to_db("NSE",symbol,"../data/"+_db_name+".db")

for symbol in bse:
    store_data_to_db("BSE",symbol,"../data/"+_db_name+".db")

