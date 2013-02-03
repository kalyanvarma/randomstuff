#To download Bhavcopy files from NSE website and populate the data into DB

import requests
import zipfile
#import StringIO
import os
import csv
import MySQLdb as mdb

#1. Download zip file and extract the csv file - Can be enhanced to read zip file into memory
filename = "cm03JAN2013bhav.csv"
url = "http://www.nseindia.com/content/historical/EQUITIES/2013/JAN/" + filename + ".zip"
response = requests.get(url)
with open(filename+".zip", "wb") as code:
    code.write(response.content)

zfile = zipfile.ZipFile(filename+".zip")
for name in zfile.namelist():
	fd = open(name,"w")
	fd.write(zfile.read(name))
	fd.close()

os.remove(filename+".zip")

#2. Open file and read contents
csvfile = open(filename, "r")
reader = csv.DictReader(csvfile)

con = mdb.connect('54.235.116.128', 'kalyan', 'kalyan1234', 'findulum')
counter = 0

for row in reader:
    symbol = row['SYMBOL']
    series = row['SERIES']
    openprice = float(row['OPEN'])*100
    closeprice = float(row['CLOSE'])*100
    highprice = float(row['HIGH'])*100
    lowprice = float(row['LOW'])*100
    lastprice = float(row['LAST'])*100
    prevclose = float(row['PREVCLOSE'])*100
    tottrdqty = float(row['TOTTRDQTY'])
    tottrdval = float(row['TOTTRDVAL'])*100
    date = row['TIMESTAMP']
    tottrades = float(row['TOTALTRADES'])
    isin = row['ISIN']
    counter = counter+1

    with con:
        cur = con.cursor()
        query = "INSERT INTO PricePoints VALUES(" +str(counter)+ ",STR_TO_DATE('" +date+ "', '%d-%M-%Y'),'" +symbol+ "','" +series+ "'," +str(openprice)+ "," +str(closeprice)+ "," +str(highprice)+ "," +str(lowprice)+ "," +str(lastprice)+ "," +str(prevclose)+ "," +str(tottrdqty)+ "," +str(tottrdval)+ "," +str(tottrades)+ ",'" +isin+ "')"
        print query
        cur.execute(query)


#4. Write contents to database table

#5. Close DB connection and file

print "Done"
