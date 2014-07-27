'''
    /usr/bin/python
'''

import datetime
import sqlite3

_db_name = str(datetime.date.today()).replace("-","_")

bse_handler = open("../resources/bom.csv","r")
bse = bse_handler.read().split("\n")[:-1]

nse_handler = open("../resources/nse.csv","r")
nse = nse_handler.read().split("\n")[:-1]

conn =  sqlite3.connect("../data/"+_db_name+".db")
cursor = conn.cursor()

for nse_stock in nse:
    print(nse_stock)
    cursor.execute("create table if not exists nse_%s (DATE varchar(32) primary key,CLOSE float,HIGH float,LOW float,OPEN float,VOLUME float)" % nse_stock.replace("-","_"))

conn.commit()

for bse_stock in bse:
    cursor.execute("create table if not exists bse_%s (DATE varchar(32) primary key,CLOSE float,HIGH float,LOW float,OPEN float,VOLUME float)" % bse_stock.replace("-","_"))

conn.commit()
